---
name: coupang-review-crawler
description: Use when the user wants to crawl, scrape, or collect Coupang(쿠팡) product reviews (리뷰/상품평) — up to ~10,000 sequentially — and optionally group/cluster them by topic(주제별 그룹화). Handles Coupang WAF blocking via insane-search. Triggers 쿠팡 리뷰 크롤링, 상품평 수집, 쿠팡 리뷰 분석, 리뷰 주제별 분류.
---

# Coupang Review Crawler

## Overview

쿠팡 상품평을 대량 수집하고 주제별로 묶는 2단계 도구. 쿠팡은 WAF로 막혀 있어
**insane-search engine 이 필수**(직접 curl/WebFetch 는 403). 리뷰 AJAX 엔드포인트는
방어가 얕아 engine 의 TLS 지문 격자로 뚫린다.

**핵심 원리 (실측 기반, 추측 아님):** 쿠팡은 리뷰를 `(정렬 × 평점)` 창마다
**offset≈1500 에서 하드캡**한다. 그래서 단일 창으로는 표시 총량(3000~4000)과 무관하게
~1500건이 천장이다. 이를 넘으려면 **평점 버킷(1~5★)을 쪼개 각각 수집 후 union+중복제거** —
이 스킬의 크롤러가 그 파티션 전략을 자동 수행한다.

## When to Use

- "쿠팡 리뷰/상품평 크롤링해줘", "이 상품 리뷰 다 모아줘", "리뷰 분석해줘"
- 리뷰를 주제별(효과·가격·배송·향·자극 등)로 그룹화·요약해야 할 때
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

# 2) 주제별 그룹화
python3 $DIR/group_reviews.py reviews.json --out grouped --xlsx
#   --topics custom.json  주제사전 교체(주제명→키워드 배열)
#   --xlsx  주제별 탭 엑셀(요약 시트 + 주제마다 시트 1개, 리뷰 전문). openpyxl 필요
#   → grouped.md (리포트) + grouped.json (구조화) [+ grouped.xlsx]
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

## 출력물

- `reviews.json` — 리뷰 배열(user/date/rating/headline/body/survey/helpful + _sort/_rating_filter)
- `grouped.md` — 주제별 요약표·긍부정 예시·설문집계·창발키워드
- `grouped.json` — 위의 구조화 버전(추가 분석용)
