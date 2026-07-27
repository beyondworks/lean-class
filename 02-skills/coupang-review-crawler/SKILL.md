---
name: coupang-review-crawler
description: Use when the user wants to crawl, scrape, or collect Coupang(쿠팡) product reviews (리뷰/상품평) — up to ~10,000 sequentially — and optionally group them by topic(주제별 그룹화) or extract marketing winning-material(위닝 소재) i.e. the reviewer's deficiency/complex (결핍·컴플렉스) that the product solves, ranked by repetition into 소구·후킹 포인트. Handles Coupang WAF blocking via insane-search. Triggers 쿠팡 리뷰 크롤링, 상품평 수집, 쿠팡 리뷰 분석, 리뷰 주제별 분류, 위닝 소재 추출, 결핍 추출, 소구포인트, 후킹 포인트, VOC 인사이트.
---

# Coupang Review Crawler

## Overview

쿠팡 상품평을 대량 수집하고 분석하는 3단계 도구(수집 → 주제 그룹화 → 위닝 소재 추출).
쿠팡은 WAF로 막혀 있어 **insane-search engine 이 필수**(직접 curl/WebFetch 는 403).
리뷰 AJAX 엔드포인트는 방어가 얕아 engine 의 TLS 지문 격자로 뚫린다.

두 분석 렌즈는 관점이 반대다 — **그룹화(group_reviews)** 는 제품 강점 중심(무엇이 좋은가),
**위닝 소재(extract_winning)** 는 고객 결핍 중심(무엇이 아팠는가 → 제품이 그걸 어떻게 푸는가).
광고 소재는 제품 자랑이 아니라 고객의 통증에서 후킹되므로, 마케팅용은 위닝 소재 렌즈를 쓴다.

**핵심 원리 (실측 기반, 추측 아님):** 쿠팡은 리뷰를 `(정렬 × 평점)` 창마다
**offset≈1500 에서 하드캡**한다. 그래서 단일 창으로는 표시 총량(3000~4000)과 무관하게
~1500건이 천장이다. 이를 넘으려면 **평점 버킷(1~5★)을 쪼개 각각 수집 후 union+중복제거** —
이 스킬의 크롤러가 그 파티션 전략을 자동 수행한다.

## When to Use

- "쿠팡 리뷰/상품평 크롤링해줘", "이 상품 리뷰 다 모아줘", "리뷰 분석해줘"
- 리뷰를 주제별(효과·가격·배송·향·자극 등)로 그룹화·요약해야 할 때
- **위닝 소재 뽑아줘 / 결핍·컴플렉스 추출 / 소구·후킹 포인트 / VOC 인사이트** — 마케팅 광고
  소재를 로우 리뷰에서 바로 뽑을 때 (결핍-우선 렌즈)
- WebFetch 가 쿠팡에서 403/빈 페이지를 줄 때

**전제:** insane-search 플러그인이 설치돼 있어야 함(engine 사용). 없으면 먼저 안내.

## 검증된 제약 (2026-07 실측)

| 항목 | 값 | 함의 |
|---|---|---|
| WAF 우회 | insane-search `engine.fetch()` | 직접 curl=403, engine 격자=OK |
| `size` (페이지당) | 최대 **30** | 50↑ 실패 |
| offset 캡 (`page×size`) | **≈1500 / 창** | 단일 창 천장 ~1500건 |
| `&ratings=1..5` 필터 | **작동** | 평점별 창 분리 → 캡 초과 수집 |
| `sortBy` | `ORDER_SCORE_ASC` 기본 | **다중 정렬 무의미**(아래) |
| 안정적 review id | **없음** | 중복제거는 content 해시(작성자+날짜+본문) |

## Quick Reference

```bash
DIR=~/.claude/skills/coupang-review-crawler

# 1) 크롤 — URL 또는 'productId:itemId:vendorItemId'
python3 $DIR/crawl_reviews.py "<쿠팡상품URL>" --max 10000 --out reviews.json
#   --ratings 5,4,3,2,1  평점버킷 순서(기본). 'none'=필터없이 1창(~1500 상한)
#   --sorts  ORDER_SCORE_ASC,DATE_DESC  창 다각화(같은 버킷 더 긁기)
#   --size 30  --offset-cap 1500  --sleep 0.5

# 2) 주제별 그룹화 (제품 강점 중심 — 무엇이 좋은가)
python3 $DIR/group_reviews.py reviews.json --out grouped --xlsx
#   --topics custom.json  주제사전 교체(주제명→키워드 배열)
#   --xlsx  주제별 탭 엑셀(요약 시트 + 주제마다 시트 1개, 리뷰 전문). openpyxl 필요
#   → grouped.md (리포트) + grouped.json (구조화) [+ grouped.xlsx]

# 3) 위닝 소재 추출 (결핍-우선 — 고객의 공통 문제 중심, 마케팅용)
python3 $DIR/extract_winning.py reviews.json --out winning --xlsx
#   기본으로 별점-only(본문없음)+체험단·협찬 리뷰 제외 → 진짜 고객 VOC 만 분석
#   --keep-promo  체험단·협찬 리뷰 유지(기본은 제외)
#   --deficits custom.json  상황 사전 교체({상황:{"kind":"trait|outcome","kw":[...]}})
#   --top 6  소구/후킹 도출 상위 상황 수   --quotes 20  상황당 부합 원문 최대 수(기본 20)
#     원문 자체가 광고 카피 재료 → 상황 부합 원문을 많이 실어 VOC 반영도를 높인다
#   → winning.md (공통문제 그룹 빈도표 + 결핍→해결 원문 + 후킹 재료) + winning.json [+ winning.xlsx]
#   리포트 머리에 필터 집계(전체/별점only/체험단/분석) 명시
```

- 스크립트는 curl_cffi 가 있는 파이썬으로 **자동 re-exec**, insane-search engine 을 **자동 탐색**.
- 긴 실행은 `run_in_background=true` 로 띄우고 `.partial` 체크포인트로 중간 유실 방지.

## 워크플로

1. **URL 파싱** — 상품 URL 에서 productId/itemId/vendorItemId 자동 추출.
2. **파티션 크롤** — ratings 버킷을 순회하며 각 창을 size=30 으로 offset 캡까지. 전역 dedup.
   max 도달 시 조기 종료. 창 실패는 3회 백오프 재시도.
3. **정직한 요약** — 요청 max 를 못 채우면 "쿠팡 캡 때문"임을 명시(부재를 성공으로 위장 금지).
4. **그룹화** — 렉시콘 다중라벨 분류 + 창발 키워드(사전 밖 빈출어) + 쿠팡 설문 집계.
   감성은 평점으로(≥4 긍정 / ≤2 부정). LLM 이 위에 의미 클러스터링을 더 얹을 수 있음.
5. **위닝 소재 추출** — 아래 "위닝 소재 렌즈" 참조. 결핍을 빈도순으로 뽑아 소구/후킹 재료로.

## 위닝 소재 렌즈 (결핍-우선 — 마케팅)

로우 리뷰에서 **리뷰어의 결핍(고객의 문제·컴플렉스)** 을 먼저 뽑고, 비슷한 **상황(문제)**끼리
한 그룹으로 묶어 건수로 센다. 그 공통 문제가 반복될수록(건수↑) 소구·후킹 우선순위가 높다
(빈도 = 소구 강도). 뷰티면 외모·컴플렉스 고민 → 제품 해결 리뷰가 핵심.

**전처리(기본 ON)**: **체험단·협찬 리뷰(제공받아 작성·무료제공 등)와 본문 없는 별점-only 리뷰를
제외**하고 진짜 고객 VOC 만 분석한다(광고 편향 제거). `--keep-promo` 로 유지 가능. 리포트 머리에
필터 집계(전체→별점only 제외→체험단 제외→분석 N)를 반드시 명시.

**상황 그룹핑**: 사전의 각 키 = 고객이 공통으로 겪는 '상황'. 유사 표현을 한 상황으로 병합한다
(예: "힘없이 내려가는"·"처지는"·"뻐신 직모"는 모두 '속눈썹이 힘없이 처짐' 한 그룹). 결핍을 두
종류로 나눠 다르게 다루는 게 정밀도의 핵심이다:

- **TRAIT** = 고객이 **원래 가진 조건·컴플렉스**(직모·짧은 속눈썹·숱없음·눈두덩 먹힘·건성 등).
  언급 자체가 결핍이다(문장이 긍정이어도 "나는 직모인데"는 결핍 컨텍스트). **위닝 소재의 핵심** —
  "직모라 포기하고 살았는데 이건…" 같은 서사가 여기서 나온다.
- **OUTCOME** = 증상(번짐·뭉침·처짐·금방지워짐). 제품이 유발도 해결도 하므로 **부정어에 민감**
  ("번짐 없음"=강점 / "번져서 창피"=결핍). extract_winning 은 OUTCOME 을 **같은 문장에 통증
  프레임(고민·창피·매번·평소…했거든요·ㅠㅠ)이 있고 부정어가 없을 때만** 결핍으로 센다(정밀도 우선).

**결핍→해결 페어링은 같은 문장 안 아크만** 잡는다(문장 넘는 매칭은 오도라 안 한다). 스크립트는
결핍 원문을 정밀 격리·빈도집계하는 역할이고, **최종 후킹 카피는 LLM(카피라이터)이 그 원문 위에
쓴다** — 자동 후킹 문구는 재료일 뿐 완성 소재가 아니다.

## 실제 수집량 기대치 (정직)

10,000 은 상한 요청값일 뿐이다. **실제 상한 = Σ min(각 평점버킷 실제수, ~1500)**.
- 리뷰가 5★에 쏠린 상품: 5★ 창 1500 + 나머지 버킷 실제수 → 보통 수천 건 미만.
- 평점이 고루 퍼진 상품: 5개 버킷 × 최대 1500 = 이론상 ~7500 까지 근접 가능.
크롤러가 끝에 `수집 N / 요청 M` 과 평점분포를 반드시 보고한다.

## Common Mistakes

- **직접 curl/WebFetch 로 시도** → 403. 반드시 engine.fetch (스크립트가 강제).
- **size>30 으로 가속 시도** → 실패. 30 이 상한.
- **단일 창으로 1500 초과 기대** → 불가. 평점 파티션이 유일한 정공법.
- **다중 정렬(`--sorts`)로 더 긁으려 시도** → 무의미·시간낭비. 같은 평점버킷에서 정렬만
  바꾸면 동일한 ~1500건이 재조회돼 dedup 으로 전부 버려진다(실측: 2번째 정렬 0건 추가,
  시간은 배로). 기본 단일 정렬 유지. 커버리지 배수는 오직 평점버킷(1~5★).
- **review id 로 dedup 시도** → id 없음. content 해시로.
- **미달 수집을 "전부"로 보고** → 금지. 쿠팡 캡 때문임을 명시.
- **python3.14 등 curl_cffi 없는 인터프리터** → 스크립트가 자동 re-exec 하나, 없으면
  `pip install -U 'curl_cffi>=0.15.0' beautifulsoup4 pyyaml` 안내.
- **위닝 소재: OUTCOME 증상을 키워드만으로 카운트** → 오도. "번짐 없음"(강점)을 "번짐"(결핍)으로
  세면 마케터가 없는 문제를 방어한다. 부정어+통증프레임 게이트 필수(스크립트가 강제).
- **위닝 소재 자동 후킹 문구를 완성 카피로 착각** → 재료일 뿐. 결핍 원문 위에 LLM 이 카피를 쓴다.
- **상황 키워드 부분문자열 오탐** → 짧은 kw 는 엉뚱한 단어에 걸린다(예 '쳐져'가 '뭉쳐져'에,
  '아래로'가 '아래로 번짐'에). 상황 사전 kw 는 충돌 없는 형태로(짧은 조각 지양), 매칭 문장은
  `_clean_clause` 로 상황 문구 주변만 잘라 광고 소재로 쓰기 좋게. 오탐은 건수를 부풀려 소구를 오도한다.
- **작은 표본(체험단 5★ 편중)에서 위닝 소재 기대** → 결핍(특히 저평점 통증)이 얇다. 위닝 소재는
  1~3★ 버킷을 포함한 큰 크롤에서 감정 강한 결핍이 잘 드러난다(emotion_score 순 정렬).

## 출력물

- `reviews.json` — 리뷰 배열(user/date/rating/headline/body/survey/helpful + _sort/_rating_filter)
- `grouped.md` / `grouped.json` — 주제별 요약표·긍부정 예시·설문집계·창발키워드 (강점 렌즈)
- `winning.md` — ① 결핍 빈도표(유형·평균★·대표원문) ② 결핍→해결 원문 ③ 소구/후킹 재료 ④ 창발 결핍
- `winning.json` — 위의 구조화(결핍별 count/kind/avg_rating/top_quotes) — LLM 카피 후속 가공용
- `--xlsx` — 결핍별 탭 엑셀(결핍 요약 시트 + 결핍마다 시트: 결핍/해결 원문·감정강도)
