---
name: instagram-post-crawler
description: Use when the user wants to crawl, scrape, or collect public Instagram(인스타그램) posts(게시물) — either a public account feed (--account @handle) or a hashtag (--hashtag) — and optionally group them by topic(주제별 그룹화). Public posts only, best-effort. Handles Instagram login-wall/bot-block via insane-search. Triggers 인스타 게시물 크롤링, 인스타 계정 수집, 해시태그 수집, 인스타 게시물 주제별 분류.
---

# Instagram Post Crawler

## Overview

인스타그램 **공개 게시물**을 수집하고 캡션을 주제별로 묶는 2단계 도구. 인스타는 비로그인
접근을 로그인월/봇차단으로 자주 막아 **insane-search engine 인프라가 필수**(직접 curl/WebFetch
는 로그인 페이지 HTML 또는 403). 공개 웹 XHR 엔드포인트를 insane-search 의 TLS 지문
임퍼소네이션 전송으로 호출한다.

**공개만·best-effort·정직 보고가 원칙.** 로그인 세션·쿠키 탈취·비공개 계정 우회는 하지
않는다. 막히면 억지로 "됐다" 하지 않고 어느 단계(로그인월/403/빈응답)에서 막혔는지 그대로
보고하고 대안(공개 oEmbed / Meta Graph 공식 경로)을 안내한다.

## 핵심 원리 (실측 기반, 2026-07)

인스타 공개 웹앱은 XHR 로 아래 JSON 엔드포인트를 호출하며, **`x-ig-app-id: 936619743392459`**
헤더가 있어야 응답한다(이 app id 는 비밀이 아니라 브라우저가 그대로 전송하는 공개 값).

| 타깃 | 엔드포인트 | 실측 상태 |
|---|---|---|
| 공개 계정 피드 | `/api/v1/users/web_profile_info/?username=<handle>` | **작동** (헤더 필요) |
| 해시태그 | `/api/v1/tags/web_info/?tag_name=<tag>` | **로그인월** (비로그인 차단됨) |

- `engine.fetch()` 는 커스텀 헤더를 못 실어 `{"status":"fail","message":"useragent mismatch"}`
  같은 200 오류 JSON 을 받는다 → 스크립트가 스키마 검증 실패로 감지하고 **POOL 헤더 경로로 폴백**.
- 실작동 경로 = `engine.transport.POOL.request(extra_headers={x-ig-app-id...})` — 같은 insane-search
  curl_cffi TLS 임퍼소네이션 전송에 필수 헤더를 실어 보낸다. impersonate 격자(chrome/safari/
  safari_ios)를 순회한다.

## When to Use

- "이 인스타 계정 게시물 모아줘", "@handle 피드 크롤링해줘"
- "#태그 게시물 수집" (단, 해시태그는 현재 로그인월로 자주 막힘 — 아래 제약 참조)
- 수집한 게시물 캡션을 주제별로 그룹화·요약해야 할 때

**전제:** insane-search 플러그인이 설치돼 있어야 함(engine + transport.POOL 사용). curl_cffi≥0.15.0
이 있는 파이썬이 있어야 하며, 없으면 스크립트가 자동 탐색·re-exec 하고 없으면 설치 안내.

## Quick Reference

```bash
DIR=~/.claude/skills/instagram-post-crawler

# 1) 크롤 — 공개 계정 피드
python3 $DIR/crawl_posts.py --account @어카운트핸들 --max 50 --out posts.json

# 1') 크롤 — 해시태그 (또는 --query 키워드; 현재 비로그인 차단이 잦음)
python3 $DIR/crawl_posts.py --hashtag 여행 --max 50 --out tag_posts.json

#   --impersonates chrome,safari,safari_ios  POOL TLS 임퍼소네이션 순회(기본)

# 2) 주제별 그룹화
python3 $DIR/group_posts.py posts.json --out grouped --xlsx
#   --topics custom.json  주제사전 교체(주제명→키워드 배열)
#   --xlsx  주제별 탭 엑셀(요약 시트 + 주제마다 시트 + 해시태그 시트). openpyxl 필요
#   → grouped.md (리포트) + grouped.json (구조화) [+ grouped.xlsx]
```

- 크롤러는 curl_cffi 가 있는 파이썬으로 **자동 re-exec**, insane-search engine/transport 를 **자동 탐색**.
- group_posts 는 `--xlsx` 지정 시 openpyxl 이 있는 파이썬으로 **자동 re-exec**.
- 성공 시 종료코드 0, **차단 시 종료코드 3**(에이전트가 실패를 인지하도록) + 단계별 사유 stderr 출력.

## 워크플로

1. **타깃 판별** — `--account`(핸들) 또는 `--hashtag`/`--query`(태그).
2. **insane-search 경유 fetch** — engine.fetch 먼저(스펙), api_fail/로그인월이면 POOL+헤더 격자로 폴백.
   응답 JSON 을 기대 스키마(계정=`data.user`, 태그=`data`)로 검증.
3. **파싱** — 계정은 `edge_owner_to_timeline_media.edges[].node`, 태그는 재귀 미디어 노드 수집.
   스키마 드리프트 대비 폴백으로 JSON 전체를 재귀 순회해 `shortcode`/`code` 가진 노드도 흡수.
   dedup 은 shortcode 기준.
4. **정직한 보고** — 못 뚫으면 단계(login_wall/http_403/api_fail/empty)와 스니펫을 명시하고
   대안(oEmbed / Meta Graph)을 안내. 부재를 성공으로 위장하지 않는다.
5. **그룹화** — 렉시콘 다중라벨 분류 + 창발 키워드 + 해시태그 집계. 리뷰와 달리 평점이 없어
   감성 대신 **참여도(like+comment)**로 상/중/하를 가른다(임의 감성 부여 금지).

## 출력물

- `posts.json` — 게시물 배열. 필드: `shortcode, url, caption, like_count, comment_count,
  timestamp(ISO), taken_at(epoch), image_url, is_video, id, owner_username, source`.
- `grouped.md` — 주제별 요약표·대표 캡션·해시태그 빈도·창발 키워드
- `grouped.json` — 위의 구조화 버전(LLM 추가 분석용)
- `grouped.xlsx` (옵션) — 요약 시트 + 주제별 시트(게시물 전체) + 해시태그 시트

## 검증된 제약 (2026-07 실측, 정직)

| 항목 | 값 | 함의 |
|---|---|---|
| 계정 피드 | web_profile_info + x-ig-app-id | **작동** (실측: @natgeo 12건 수집, like/comment/caption/이미지 필드 정상) |
| 해시태그 | tags/web_info | **로그인월** (실측: HTTP 200 이지만 로그인 페이지 HTML 반환 → 0건, exit 3) |
| 1회 응답 한계 | 계정 첫 페이지 ~12건 | 비로그인은 페이지네이션 커서가 막혀 **첫 응답 분량만**. `--max` 는 상한일 뿐 |
| 헤더 | `x-ig-app-id` 필수 | 없으면 `{"status":"fail","useragent mismatch"}` |
| 전송 | insane-search POOL(curl_cffi TLS) | 직접 curl 은 TLS 지문으로 차단 가능 |

## 실제 수집량 기대치 (정직)

- **계정**: 비로그인 web_profile_info 는 프로필 + **최신 게시물 첫 묶음(~12건)**만 안정적으로 준다.
  더 깊은 페이지네이션(`end_cursor`)은 비로그인에서 자주 막힌다 → `--max` 를 크게 줘도 첫 응답
  분량이 상한. 전체 아카이브가 필요하면 공식 Graph API(토큰) 경로가 정공법.
- **해시태그**: 현재 비로그인 접근이 로그인월로 막혀 **0건이 정상적인 실측 결과**일 수 있다.
  크롤러가 `[blocked] login_wall` 로 정직하게 보고하고 exit 3 을 낸다.

## 막혔을 때 대안 (안내만 — 이번 구현 범위 밖)

- **공개 oEmbed** — 개별 게시물 URL 의 임베드 메타(제목·썸네일·작성자):
  `https://api.instagram.com/oembed?url=<POST_URL>` (게시물 목록 수집엔 부적합, 단건 메타용).
- **Meta Graph API 공식 경로** — Instagram Graph API / Basic Display API. 앱 심사·액세스 토큰이
  필요하지만 약관 내에서 안정적으로 게시물·인사이트를 준다. 반복 자동화에는 이 경로가 정답.

## Common Mistakes

- **x-ig-app-id 없이 호출** → `{"status":"fail","useragent mismatch"}`. 스크립트가 감지·폴백하나,
  직접 호출 시 반드시 이 헤더를 실어야 함.
- **engine.fetch 200 을 성공으로 오인** → 200 오류 JSON 을 준다. 스키마 검증(`data.user`/`data`)
  통과해야 성공. 스크립트가 강제.
- **해시태그 0건을 버그로 오인** → 현재 비로그인 로그인월이 원인(실측). 스크립트 stderr 의
  `[blocked]` 단계를 읽고 대안 경로로 안내.
- **비로그인으로 수천 건 기대** → 불가. 계정 첫 응답 ~12건이 비로그인 천장. 대량은 Graph API.
- **로그인 세션/쿠키로 우회 시도** → 금지. 공개 접근만, 약관 존중.
- **curl_cffi/openpyxl 없는 인터프리터** → 스크립트가 자동 re-exec. 없으면
  `pip install -U 'curl_cffi>=0.15.0' beautifulsoup4 pyyaml openpyxl` 안내.

## 의존성

- **insane-search** 플러그인 (engine + transport.POOL) — 필수.
- **curl_cffi ≥ 0.15.0** — TLS 임퍼소네이션 전송.
- **openpyxl** — `group_posts.py --xlsx` 사용 시만.
