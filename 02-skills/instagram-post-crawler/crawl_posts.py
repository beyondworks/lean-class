#!/usr/bin/env python3
"""
Instagram 공개 게시물 크롤러 — WAF/로그인월 우회는 insane-search 경유.

원칙 (정직·약관 존중):
  - **공개 게시물만.** 로그인 세션·쿠키 탈취·비공개 계정 우회 안 함.
  - best-effort. 인스타는 비로그인 접근을 자주 로그인월(로그인 페이지 HTML)로 막는다.
    막히면 억지로 "됐다" 하지 않고 어느 단계(403/로그인월/빈응답)에서 막혔는지 그대로 보고.

타깃 2종:
  --account <@handle>   공개 계정 프로필 피드
      엔드포인트: /api/v1/users/web_profile_info/?username=<handle>
      필수 헤더: x-ig-app-id: 936619743392459  (없으면 로그인월/403)
  --hashtag <태그> | --query <키워드>  공개 해시태그 게시물
      엔드포인트: /api/v1/tags/web_info/?tag_name=<tag>

접근 경로 (둘 다 insane-search 인프라):
  1) engine.fetch() — insane-search 공개 진입점(TLS 지문 격자 + Playwright 폴백).
     단 커스텀 헤더를 못 실어서 web_profile_info 는 헤더 부재로 자주 로그인월.
  2) engine.transport.POOL.request(extra_headers=...) — 같은 curl_cffi TLS 임퍼소네이션
     전송을 쓰되 x-ig-app-id 를 실어 보낸다(인스타 웹앱이 실제로 보내는 헤더 재현).
  → 1을 먼저(스펙), 실패 시 2를 impersonate 격자로 순회. 둘 다 insane-search 경유.

출력 posts.json: shortcode/url/caption/like_count/comment_count/timestamp/taken_at/
                 image_url/is_video/id/owner_username/source. dedup = shortcode.
"""
import argparse, glob, json, os, re, subprocess, sys, time

IG_APP_ID = "936619743392459"  # 인스타 웹앱 공개 app id (비밀 아님, 브라우저가 그대로 전송)


# ── insane-search engine 을 import 할 수 있는 파이썬으로 재실행 ──────────────
def _reexec_into_python_with_curl_cffi():
    try:
        import curl_cffi  # noqa
        return
    except Exception:
        pass
    if os.environ.get("_IPC_REEXEC"):
        return  # 무한 재실행 방지
    cands = []
    for pat in ("python3.13", "python3.12", "python3.11", "python3.10"):
        cands += glob.glob(f"/opt/homebrew/opt/python@*/bin/{pat}")
        cands += glob.glob(f"/usr/local/opt/python@*/bin/{pat}")
        cands += [f"/opt/homebrew/bin/{pat}", f"/usr/bin/{pat}"]
    for py in cands:
        if not os.path.exists(py):
            continue
        rc = subprocess.run([py, "-c", "import curl_cffi"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        if rc == 0:
            os.environ["_IPC_REEXEC"] = "1"
            os.execv(py, [py, os.path.abspath(__file__), *sys.argv[1:]])
    sys.stderr.write(
        "[fatal] curl_cffi 가 있는 파이썬을 못 찾음. 먼저 설치:\n"
        "  pip install -U 'curl_cffi>=0.15.0' beautifulsoup4 pyyaml\n")
    sys.exit(2)


def _locate_engine():
    """insane-search 플러그인 캐시에서 engine 디렉토리를 찾아 sys.path 에 추가."""
    pats = [
        os.path.expanduser("~/.claude/plugins/cache/*/insane-search/*/skills/insane-search"),
        os.path.expanduser("~/.claude/plugins/marketplaces/*/plugins/insane-search/skills/insane-search"),
        os.path.expanduser("~/.claude/skills/insane-search"),
    ]
    for p in pats:
        for d in sorted(glob.glob(p), reverse=True):  # 최신 버전 우선
            if os.path.isdir(os.path.join(d, "engine")):
                sys.path.insert(0, d)
                return d
    sys.stderr.write("[fatal] insane-search engine 을 찾을 수 없음. insane-search 플러그인 필요.\n")
    sys.exit(2)


# ── 요청 헤더 (인스타 웹앱이 XHR 로 실제 보내는 것 재현) ─────────────────────
def _ig_headers():
    return {
        "x-ig-app-id": IG_APP_ID,
        "x-requested-with": "XMLHttpRequest",
        "Accept": "*/*",
        "Referer": "https://www.instagram.com/",
        "Origin": "https://www.instagram.com",
    }


def _looks_like_login_wall(text: str) -> bool:
    if not text:
        return True
    head = text[:4000].lower()
    # HTML(로그인 페이지)이면 JSON 이 아님 → 로그인월/차단
    if head.lstrip().startswith("<!doctype") or head.lstrip().startswith("<html"):
        return True
    return ("loginform" in head or "\"require_login\"" in head
            or "please wait a few minutes" in head)


class FetchOutcome:
    def __init__(self, data=None, stage="", status=None, snippet="", route=""):
        self.data = data          # 파싱된 dict (성공) 또는 None
        self.stage = stage        # ok | login_wall | http_<code> | empty | not_json | error
        self.status = status
        self.snippet = snippet
        self.route = route        # engine.fetch | pool:<impersonate>


def _parse_valid(txt, is_valid):
    """txt → (obj, kind). kind: ok | api_fail | not_json.
    api_fail = 인스타 API 오류 payload({"status":"fail"} 등)이거나 기대 스키마 아님."""
    try:
        obj = json.loads(txt)
    except json.JSONDecodeError:
        return None, "not_json"
    if isinstance(obj, dict) and obj.get("status") == "fail":
        return obj, "api_fail"
    if is_valid and not is_valid(obj):
        return obj, "api_fail"
    return obj, "ok"


def ig_fetch(url, log, POOL=None, engine_fetch=None, is_valid=None,
             impersonates=("chrome", "safari", "safari_ios")):
    """인스타 공개 JSON 엔드포인트를 insane-search 경유로 호출. FetchOutcome 반환.

    is_valid(obj)->bool 로 기대 payload 인지 검증한다. engine.fetch 는 x-ig-app-id 를
    못 실어 {"status":"fail","message":"useragent mismatch"} 같은 200 오류 JSON 을 자주
    돌려주므로, 스키마 검증에 실패하면 POOL(헤더 포함) 경로로 폴백한다.
    """
    last = FetchOutcome(stage="error", snippet="no route attempted")

    # 경로 1) engine.fetch (스펙 우선). 커스텀 헤더 못 실음 → 대개 api_fail, 폴백 대상.
    if engine_fetch is not None:
        try:
            res = engine_fetch(url, timeout=25, enable_playwright=False)
            txt = getattr(res, "content", "") or ""
            if not getattr(res, "ok", False) or _looks_like_login_wall(txt):
                last = FetchOutcome(stage="login_wall", snippet=txt[:300], route="engine.fetch")
            else:
                obj, kind = _parse_valid(txt, is_valid)
                if kind == "ok":
                    return FetchOutcome(data=obj, stage="ok", status=200, route="engine.fetch")
                last = FetchOutcome(stage=kind, snippet=txt[:300], route="engine.fetch")
        except Exception as e:
            last = FetchOutcome(stage="error", snippet=f"engine.fetch: {e}", route="engine.fetch")
        log(f"    engine.fetch → {last.stage}")

    # 경로 2) POOL.request + x-ig-app-id (인스타 필수 헤더). impersonate 격자 순회.
    if POOL is not None:
        for imp in impersonates:
            try:
                resp, err = POOL.request(url, impersonate=imp,
                                         referer="https://www.instagram.com/",
                                         extra_headers=_ig_headers(), timeout=25)
            except Exception as e:
                last = FetchOutcome(stage="error", snippet=f"pool {imp}: {e}", route=f"pool:{imp}")
                log(f"    pool:{imp} → error {e}")
                continue
            if resp is None:
                last = FetchOutcome(stage="error", snippet=str(err), route=f"pool:{imp}")
                log(f"    pool:{imp} → {err}")
                continue
            status = getattr(resp, "status_code", None)
            txt = getattr(resp, "text", "") or ""
            if status != 200:
                last = FetchOutcome(stage=f"http_{status}", status=status,
                                    snippet=txt[:300], route=f"pool:{imp}")
                log(f"    pool:{imp} → HTTP {status}")
                continue
            if _looks_like_login_wall(txt):
                last = FetchOutcome(stage="login_wall", status=status,
                                    snippet=txt[:300], route=f"pool:{imp}")
                log(f"    pool:{imp} → login_wall")
                continue
            obj, kind = _parse_valid(txt, is_valid)
            if kind == "ok":
                return FetchOutcome(data=obj, stage="ok", status=200, route=f"pool:{imp}")
            last = FetchOutcome(stage=kind, status=status, snippet=txt[:300], route=f"pool:{imp}")
            log(f"    pool:{imp} → {kind}")
            time.sleep(0.4)
    return last


# ── 게시물 노드 → 표준 레코드 ───────────────────────────────────────────────
def _first(d, *keys, default=""):
    for k in keys:
        if isinstance(d, dict) and d.get(k) not in (None, ""):
            return d[k]
    return default


def _caption_from_node(node):
    # GraphQL(web_profile_info): edge_media_to_caption.edges[0].node.text
    cap = node.get("edge_media_to_caption")
    if isinstance(cap, dict):
        edges = cap.get("edges") or []
        if edges:
            return (edges[0].get("node") or {}).get("text", "")
    # v1(api): caption.text 또는 caption(str)
    c = node.get("caption")
    if isinstance(c, dict):
        return c.get("text", "")
    if isinstance(c, str):
        return c
    return ""


def _count(node, *keys):
    for k in keys:
        v = node.get(k)
        if isinstance(v, dict) and "count" in v:
            return v["count"]
        if isinstance(v, int):
            return v
    return None


def node_to_record(node, source, owner=""):
    shortcode = _first(node, "shortcode", "code")
    if not shortcode:
        return None
    ts = _first(node, "taken_at_timestamp", "taken_at", default=None)
    try:
        ts = int(ts) if ts not in (None, "") else None
    except (ValueError, TypeError):
        ts = None
    iso = ""
    if ts:
        import datetime
        iso = datetime.datetime.utcfromtimestamp(ts).isoformat() + "Z"
    like = _count(node, "edge_liked_by", "edge_media_preview_like", "like_count")
    if like is None:
        like = node.get("like_count")
    comment = _count(node, "edge_media_to_comment", "edge_media_to_parent_comment", "comment_count")
    if comment is None:
        comment = node.get("comment_count")
    img = _first(node, "display_url", "thumbnail_src", "thumbnail_url")
    if not img:
        # v1 image_versions2.candidates[0].url
        iv = node.get("image_versions2")
        if isinstance(iv, dict):
            cands = iv.get("candidates") or []
            if cands:
                img = cands[0].get("url", "")
    own = owner
    if not own:
        ou = node.get("owner") or node.get("user")
        if isinstance(ou, dict):
            own = ou.get("username", "")
    return {
        "shortcode": shortcode,
        "url": f"https://www.instagram.com/p/{shortcode}/",
        "caption": _caption_from_node(node),
        "like_count": like,
        "comment_count": comment,
        "timestamp": iso,
        "taken_at": ts,
        "image_url": img,
        "is_video": bool(node.get("is_video") or node.get("media_type") == 2),
        "id": _first(node, "id", "pk"),
        "owner_username": own,
        "source": source,
    }


def _walk_media_nodes(obj):
    """스키마 드리프트 대비: JSON 을 재귀 순회하며 'shortcode'/'code' 가진 미디어 dict 수집."""
    found = []
    def rec(o):
        if isinstance(o, dict):
            if ("shortcode" in o or "code" in o) and ("id" in o or "pk" in o):
                found.append(o)
            for v in o.values():
                rec(v)
        elif isinstance(o, list):
            for v in o:
                rec(v)
    rec(obj)
    return found


def parse_account(data, source):
    user = (((data or {}).get("data") or {}).get("user")) or {}
    owner = user.get("username", "")
    tl = user.get("edge_owner_to_timeline_media") or {}
    edges = tl.get("edges") or []
    recs = []
    for e in edges:
        node = e.get("node") if isinstance(e, dict) else None
        if node:
            r = node_to_record(node, source, owner)
            if r:
                recs.append(r)
    if not recs:  # 폴백: 재귀 수집
        for node in _walk_media_nodes(data):
            r = node_to_record(node, source, owner)
            if r:
                recs.append(r)
    meta = {"username": owner,
            "full_name": user.get("full_name", ""),
            "is_private": user.get("is_private"),
            "follower_count": (user.get("edge_followed_by") or {}).get("count"),
            "media_count": tl.get("count")}
    return recs, meta


def parse_hashtag(data, source):
    # web_info: data.top/recent.sections[].layout_content.medias[].media
    #           또는 (구) edge_hashtag_to_media.edges[].node
    recs = []
    for node in _walk_media_nodes(data):
        r = node_to_record(node, source)
        if r:
            recs.append(r)
    d = (data or {}).get("data") or {}
    meta = {"media_count": d.get("media_count"),
            "name": d.get("name")}
    return recs, meta


def dedup(records):
    seen, out = set(), []
    for r in records:
        k = r["shortcode"]
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser(description="Instagram 공개 게시물 크롤러 (insane-search 경유)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--account", help="공개 계정 핸들 (@handle 또는 handle)")
    g.add_argument("--hashtag", help="해시태그 (# 없이)")
    g.add_argument("--query", help="키워드 (해시태그로 취급)")
    ap.add_argument("--max", type=int, default=100, help="최대 수집 건수(비로그인 1회 응답 한계 있음)")
    ap.add_argument("--out", default="posts.json", help="출력 JSON 경로")
    ap.add_argument("--impersonates", default="chrome,safari,safari_ios",
                    help="POOL TLS 임퍼소네이션 순회 목록(콤마)")
    args = ap.parse_args()

    _reexec_into_python_with_curl_cffi()
    _locate_engine()
    from engine import fetch as engine_fetch
    from engine.transport import POOL

    def log(m):
        sys.stderr.write(m + "\n"); sys.stderr.flush()

    imps = tuple(s.strip() for s in args.impersonates.split(",") if s.strip())

    if args.account:
        handle = args.account.lstrip("@").strip("/").split("/")[-1]
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={handle}"
        source = f"account:@{handle}"
        log(f"[crawl] account @{handle}")
        valid = lambda o: bool(((o or {}).get("data") or {}).get("user"))
        oc = ig_fetch(url, log, POOL=POOL, engine_fetch=engine_fetch,
                      is_valid=valid, impersonates=imps)
        records, meta = ([], {})
        if oc.stage == "ok":
            records, meta = parse_account(oc.data, source)
    else:
        tag = (args.hashtag or args.query).lstrip("#").strip()
        url = f"https://www.instagram.com/api/v1/tags/web_info/?tag_name={tag}"
        source = f"hashtag:#{tag}"
        log(f"[crawl] hashtag #{tag}")
        valid = lambda o: isinstance((o or {}).get("data"), dict)
        oc = ig_fetch(url, log, POOL=POOL, engine_fetch=engine_fetch,
                      is_valid=valid, impersonates=imps)
        records, meta = ([], {})
        if oc.stage == "ok":
            records, meta = parse_hashtag(oc.data, source)

    records = dedup(records)[:args.max]

    summary = {
        "target": source,
        "collected": len(records),
        "requested_max": args.max,
        "fetch_stage": oc.stage,
        "fetch_route": oc.route,
        "http_status": oc.status,
        "target_meta": meta,
        "out": os.path.abspath(args.out),
    }

    if oc.stage == "ok":
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        log(f"[done] 수집 {len(records)}건 → {args.out}")
        if not records:
            log("[note] 응답은 성공(JSON)했으나 게시물 노드 0건 — 비공개/게시물 없음/스키마 변경 가능. "
                "raw 확인 필요.")
    else:
        # 정직한 실패 보고: 어느 단계에서 막혔는지 + 대안 안내
        log("")
        log(f"[blocked] 수집 실패 — 단계: {oc.stage} (route={oc.route}, http={oc.status})")
        log(f"[snippet] {oc.snippet[:200]!r}")
        log("[note] 인스타는 비로그인 공개 접근을 로그인월/403 으로 자주 막는다(best-effort 한계).")
        log("[alt] 대안(이번 구현 범위 밖, 안내만):")
        log("  - 공개 oEmbed(개별 게시물 URL 임베드 메타): https://api.instagram.com/oembed?url=<POST_URL>")
        log("  - 공식 경로: Meta Graph API (Instagram Graph / Basic Display) — 앱 심사·토큰 필요")

    print(json.dumps(summary, ensure_ascii=False))
    # 막힌 경우 비정상 종료로 상위(에이전트)가 실패를 인지하게 함
    sys.exit(0 if oc.stage == "ok" else 3)


if __name__ == "__main__":
    main()
