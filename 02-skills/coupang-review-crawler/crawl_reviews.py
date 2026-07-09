#!/usr/bin/env python3
"""
Coupang review crawler — WAF bypass via insane-search engine.

핵심 사실 (2026-07 실측, coupang.com/vp/product/reviews):
  - 상품 HTML 직접 접근은 WAF challenge로 막힘. 리뷰 AJAX 엔드포인트는 방어가 얕다.
    → insane-search engine.fetch() 의 TLS 지문 격자로 뚫는다 (직접 curl 은 403).
  - size(페이지당 건수) 최대 = 30. 50 이상은 실패.
  - offset(page*size) 하드 캡 ≈ 1500. 단일 (정렬,평점) 창으로는 표시 총량과 무관하게
    ~1500건이 천장 (page 150·size10=OK, page 180+=재시도해도 실패).
  - &ratings=1..5 필터가 실제 작동 → 평점별로 창을 쪼개면 각 창이 독립 1500 캡을 가져
    union+중복제거로 1500을 초과 수집 가능 (이게 10,000 목표에 접근하는 유일한 정공법).
  - HTML에 안정적 review id 없음 → 중복제거는 content 해시(작성자+날짜+본문)로.

전략: ratings [5,4,3,2,1] 각각을 size=30 으로 offset 캡까지 순차 수집 → 전체 dedup.
      부족하면 정렬(sorts) 을 늘려 같은 버킷 안에서 다른 창을 추가로 긁는다.
정직성: 요청 max 를 못 채우면 실제 수집량과 "쿠팡 캡 때문"임을 명시 보고한다.
"""
import argparse, glob, hashlib, json, os, re, subprocess, sys, time

# ── insane-search engine 을 import 할 수 있는 파이썬으로 재실행 ──────────────
# curl_cffi 는 insane-search 가 특정 파이썬(예: 3.11)에 깔아둔다. 현재 인터프리터가
# 못 쓰면 curl_cffi 가 있는 파이썬을 찾아 그쪽으로 re-exec 한다.
def _reexec_into_python_with_curl_cffi():
    try:
        import curl_cffi  # noqa
        return
    except Exception:
        pass
    if os.environ.get("_CRC_REEXEC"):
        return  # 무한 재실행 방지
    cands = []
    for pat in ("python3.13", "python3.12", "python3.11", "python3.10"):
        cands += glob.glob(f"/opt/homebrew/opt/python@*/bin/{pat}")
        cands += glob.glob(f"/usr/local/opt/python@*/bin/{pat}")
        cands += [f"/opt/homebrew/bin/{pat}", f"/usr/bin/{pat}"]
    for py in cands:
        if not os.path.exists(py):
            continue
        # py 는 통제된 glob 결과(사용자 입력 아님). 그래도 shell 회피 위해 리스트 인자 사용.
        rc = subprocess.run([py, "-c", "import curl_cffi"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        if rc == 0:
            os.environ["_CRC_REEXEC"] = "1"
            os.execv(py, [py, os.path.abspath(__file__), *sys.argv[1:]])
    sys.stderr.write(
        "[fatal] curl_cffi 가 있는 파이썬을 못 찾음. 먼저 설치:\n"
        "  pip install -U 'curl_cffi>=0.15.0' beautifulsoup4 pyyaml\n")
    sys.exit(2)


def _locate_engine():
    """insane-search 플러그인 캐시에서 engine 디렉토리를 찾아 sys.path 에 추가."""
    pats = [
        os.path.expanduser("~/.claude/plugins/cache/*/insane-search/*/skills/insane-search"),
        os.path.expanduser("~/.claude/skills/insane-search"),
    ]
    for p in pats:
        for d in sorted(glob.glob(p), reverse=True):  # 최신 버전 우선
            if os.path.isdir(os.path.join(d, "engine")):
                sys.path.insert(0, d)
                return d
    sys.stderr.write("[fatal] insane-search engine 을 찾을 수 없음. insane-search 플러그인 필요.\n")
    sys.exit(2)


# ── 상품 식별자 파싱 ────────────────────────────────────────────────────────
def parse_ids(url_or_ids: str):
    """URL 또는 'pid:item:vendor' 에서 productId/itemId/vendorItemId 추출."""
    if re.fullmatch(r"\d+(:\d+){0,2}", url_or_ids):
        parts = url_or_ids.split(":")
        return (parts[0],
                parts[1] if len(parts) > 1 else "",
                parts[2] if len(parts) > 2 else "")
    pid = re.search(r"/products/(\d+)", url_or_ids)
    item = re.search(r"[?&]itemId=(\d+)", url_or_ids)
    vendor = re.search(r"[?&]vendorItemId=(\d+)", url_or_ids)
    if not pid:
        sys.stderr.write("[fatal] URL 에서 productId 를 못 찾음.\n")
        sys.exit(2)
    return (pid.group(1),
            item.group(1) if item else "",
            vendor.group(1) if vendor else "")


def review_url(pid, item, vendor, page, size, sort, rating=None):
    u = (f"https://www.coupang.com/vp/product/reviews?productId={pid}&page={page}"
         f"&size={size}&sortBy={sort}&ratingSummary=true&reviewTypeCount=0"
         f"&isImageOnlyReview=false&itemId={item}&vendorItemId={vendor}")
    if rating is not None:
        u += f"&ratings={rating}"
    return u


def _txt(el):
    return el.get_text(" ", strip=True) if el else ""


def parse_reviews(html, BeautifulSoup):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for a in soup.select("article.sdp-review__article__list"):
        star_el = a.select_one("[data-rating]")
        rating = star_el["data-rating"] if star_el and star_el.has_attr("data-rating") else ""
        out.append({
            "user": _txt(a.select_one(".sdp-review__article__list__info__user__name")),
            "date": _txt(a.select_one(".sdp-review__article__list__info__product-info__reg-date")),
            "rating": rating,
            "headline": _txt(a.select_one(".sdp-review__article__list__headline")),
            "body": _txt(a.select_one(".sdp-review__article__list__review__content")),
            "survey": " | ".join(_txt(s) for s in a.select(".sdp-review__article__list__survey__row")),
            "helpful": _txt(a.select_one(".sdp-review__article__list__help__count")),
        })
    return out


def rkey(r):
    return hashlib.md5(f"{r['user']}|{r['date']}|{r['body']}".encode("utf-8")).hexdigest()


def crawl_window(fetch, BeautifulSoup, ids, sort, rating, size, offset_cap,
                 seen, collected, target, sleep, log):
    """단일 (sort, rating) 창을 offset 캡까지 순차 수집. 새 리뷰 수 반환."""
    pid, item, vendor = ids
    added = 0
    page = 1
    empty_streak = 0
    max_page = max(1, offset_cap // size + 2)
    while page <= max_page and len(collected) < target:
        url = review_url(pid, item, vendor, page, size, sort, rating)
        res = None
        for attempt in range(3):  # 창 내부 재시도 (일시 WAF 대비)
            # enable_playwright=False: 리뷰 API 는 curl_cffi 경로로만 뚫린다.
            # 브라우저 폴백은 홈페이지 Access Denied 만 받고 40초 낭비 + 창 팝업만 띄우므로 끈다.
            # → 캡(offset~1500) 초과 페이지가 즉시 실패해 버킷 전환이 빨라진다.
            res = fetch(url, success_selectors=["article.sdp-review__article__list"],
                        timeout=25, enable_playwright=False)
            if res.ok:
                break
            time.sleep(1.2 * (attempt + 1))  # 백오프
        if not res or not res.ok:
            log(f"  [{sort} r{rating} p{page}] fetch 실패 → 이 창 종료")
            break
        revs = parse_reviews(res.content, BeautifulSoup)
        if not revs:
            empty_streak += 1
            if empty_streak >= 2:
                break
            page += 1
            continue
        empty_streak = 0
        new = 0
        for r in revs:
            k = rkey(r)
            if k in seen:
                continue
            seen.add(k)
            r["_sort"] = sort
            r["_rating_filter"] = rating
            collected.append(r)
            new += 1
            added += 1
        log(f"  [{sort} r{rating} p{page}] +{new} new (window {added}, total {len(collected)})")
        page += 1
        time.sleep(sleep)
    return added


def main():
    ap = argparse.ArgumentParser(description="Coupang 리뷰 크롤러 (insane-search 기반)")
    ap.add_argument("target", help="상품 URL 또는 'productId:itemId:vendorItemId'")
    ap.add_argument("--max", type=int, default=10000, help="최대 수집 건수 (기본 10000)")
    ap.add_argument("--out", default="coupang_reviews.json", help="출력 JSON 경로")
    ap.add_argument("--size", type=int, default=30, help="페이지당 건수 (쿠팡 상한 30)")
    ap.add_argument("--offset-cap", type=int, default=1500, help="창당 offset 캡 (쿠팡 ~1500)")
    ap.add_argument("--ratings", default="5,4,3,2,1", help="평점 버킷 순서 (콤마). 'none'=필터없이 1창")
    ap.add_argument("--sorts", default="ORDER_SCORE_ASC", help="정렬 목록 (콤마). 예 ORDER_SCORE_ASC,DATE_DESC")
    ap.add_argument("--sleep", type=float, default=0.5, help="페이지 간 대기(초)")
    args = ap.parse_args()

    _reexec_into_python_with_curl_cffi()
    _locate_engine()
    from engine import fetch
    from bs4 import BeautifulSoup

    ids = parse_ids(args.target)
    size = min(args.size, 30)
    sorts = [s.strip() for s in args.sorts.split(",") if s.strip()]
    if args.ratings.strip().lower() == "none":
        ratings = [None]
    else:
        ratings = [int(x) for x in args.ratings.split(",") if x.strip()]

    def log(m):
        sys.stderr.write(m + "\n"); sys.stderr.flush()

    log(f"[crawl] productId={ids[0]} itemId={ids[1]} vendorItemId={ids[2]} "
        f"max={args.max} size={size} ratings={ratings} sorts={sorts}")

    seen, collected = set(), []
    ckpt = args.out + ".partial"
    # rating 버킷 우선 순회 → 각 버킷을 여러 정렬로 (창 다각화). max 도달 시 조기 종료.
    for rating in ratings:
        if len(collected) >= args.max:
            break
        for sort in sorts:
            if len(collected) >= args.max:
                break
            got = crawl_window(fetch, BeautifulSoup, ids, sort, rating, size,
                               args.offset_cap, seen, collected, args.max, args.sleep, log)
            # 체크포인트 (긴 실행 중 유실 방지)
            with open(ckpt, "w", encoding="utf-8") as f:
                json.dump(collected, f, ensure_ascii=False)
            log(f"[bucket r{rating} sort={sort}] window added {got}, running total {len(collected)}")

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(collected, f, ensure_ascii=False, indent=2)
    if os.path.exists(ckpt):
        os.remove(ckpt)

    # 정직한 요약: 요청 대비 실제
    import collections as _c
    dist = dict(sorted(_c.Counter(r["rating"] for r in collected).items(), reverse=True))
    log("")
    log(f"[done] 수집 {len(collected)}건 / 요청 {args.max}건 → {args.out}")
    log(f"[dist] 평점분포 {dist}")
    if len(collected) < args.max:
        log(f"[note] 요청({args.max})보다 적음. 쿠팡이 (정렬×평점) 창마다 offset~{args.offset_cap}으로 "
            f"하드캡하기 때문 — 평점버킷을 모두 소진하면 이 상품의 공개 리뷰 상한에 도달한 것.")
    print(json.dumps({"collected": len(collected), "requested": args.max,
                      "out": os.path.abspath(args.out), "rating_dist": dist}, ensure_ascii=False))


if __name__ == "__main__":
    main()
