---
name: higgsfield-mcp-ops
description: Higgsfield MCP·Marketing Studio를 실제로 돌릴 때 걸리는 운용 함정과 게이트. 아바타가 조용히 바뀌는 문제, NSFW 오차단을 부르는 어휘, 한국어 대사 훼손, 상품 URL 임포트 실패, 크레딧·시간 예산. 트리거 — "힉스필드로 UGC 만들어줘", "마케팅 스튜디오", "제품 광고 영상", "아바타 지정", "NSFW로 막혔어", "왜 실패했지", "크레딧 얼마나 드나", "쿠팡/아마존 상품으로 광고", "한국어 대사 영상".
---

# Higgsfield 운용 (MCP · Marketing Studio)

제작 방법론이 아니라 **돈과 시간이 걸린 운용 지식**이다. "어떻게 잘 찍나"는 `ai-filmmaking-pipeline`,
여기는 "왜 실패했고 어떻게 피하나".

수록된 항목은 전부 실제 발주에서 당한 것이다. 벤더 공식 문서(`higgsfield-generate`의
troubleshooting)에는 없다 — 그쪽은 "API를 정확히 부르는 법", 여기는 "정확히 불렀는데도 틀어지는 지점".

## 발주 전 게이트 (순서 고정)

1. **워크스페이스가 선택돼 있나** — 미선택이면 생성이 통째로 막힌다. `list_workspaces` → `select_workspace`.
2. **로그인·크레딧** — 타임라인/생성 툴이 `canGenerate:false`를 주면 그 앞은 전부 헛수고다.
3. **아바타를 지정했나** — §1. 안 하면 서버가 **말없이 아무나 배정한다**.
4. **프롬프트에 §2의 금지 어휘가 없나** — 있으면 NSFW로 잘린다.
5. **대사가 한국어면 §3의 어휘 규칙을 지켰나**.

## 1. 아바타는 `avatar_ids`로만 지정된다 (가장 비싼 함정)

프롬프트 본문에 `<<<avatar:...>>>` 토큰을 써도 **무시된다.** 그리고 조용히 넘어가지 않는다 —
서버가 **임의의 프리셋 아바타를 자동 배정**한다. 실측: 마스카라 리뷰 UGC를 발주했더니 남성 프리셋이
배정돼 나왔다. 응답의 `warning` 필드에만 적히므로 놓치기 쉽다.

```jsonc
// 맞다
{ "model": "marketing_studio_video",
  "avatar_ids": ["<avatar uuid>"],       // ← 여기
  "product_ids": ["<product uuid>"] }

// 틀렸다 — 토큰은 파싱되지 않는다
{ "prompt": "<<<avatar:uuid>>> 이 사람이 …" }
```

타입을 단정해야 하면 `avatars: [{id, type: 'custom'|'preset'}]`.
발주 응답에서 **`avatar_ids`가 그대로 실려 있는지, `avatar_auto_picked`가 없는지** 반드시 확인한다.

아바타 목록은 `show_marketing_studio(action='list', type='avatar')` — 응답의 `gender` 필드로 거른 뒤,
**`preview_url`을 실제로 열어 확인**한다. 이름만으로 성별·인상을 추측하지 말 것(안경 착용 여부처럼
콘셉트를 깨는 요소가 이름엔 안 드러난다).

## 2. NSFW 오차단은 대개 '어휘' 탓이다

사람이 나오는 뷰티·의류·퍼스널케어 광고에서 자주 터진다. 실측: 같은 콘셉트로 3건 연속
`status: nsfw`. 아바타를 바꿔도 계속 걸렸고, **프롬프트 어휘를 바꾸니 통과**했다.

| 걸린 표현 | 바꾼 표현 |
|---|---|
| `bare skin`, `bare clean skin` | `natural skin`, `clean complexion` |
| `EXTREME MACRO`, `extreme close-up` | `tight shot`, `detail shot` |
| 의상 미지정(아바타 원본이 노출 있는 옷) | `wears a crew-neck top with a shirt layered over it, covering shoulders and neckline` |

원리: 필터가 **신체 근접·노출을 암시하는 형용사**에 반응한다. 대상이 눈·입술처럼 신체 부위라도
"tight shot of the eye area"처럼 **부위+거리**로 쓰면 통과한다.

**아바타가 아니라 어휘인지 가르는 법** — 다른 아바타로 1건 던져 같이 걸리면 어휘 문제다.
아바타를 계속 바꾸며 재발주하면 크레딧만 태운다.

`ai-filmmaking-pipeline` §10은 "사람 얼굴이 트리거"라고 하는데, 그건 이것과 별개의 층이다.
얼굴을 빼도 어휘가 남아 있으면 계속 걸린다.

## 3. 한국어 대사는 훼손된다 — 어휘를 단순하게

프롬프트에 넣은 한국어 대사가 처리 과정에서 깨져 나온다. 실측 사례:

```
얇아요  → 얇어요        속눈썹 → 속눈썰        뭉침 → 뚝침
```

받침이 겹치거나 자모 조합이 복잡한 단어에서 발생한다. 깨진 채로 발화되면 그대로 이상하게 들린다.

**대응**
- 발주 응답의 `params.prompt`에서 **대사를 눈으로 대조**한다. 이게 유일한 확인 지점이다.
- 깨졌으면 같은 뜻의 **평이한 어휘로 바꿔 재발주**한다("가늘어요", "한 올 한 올" 등은 통과했다).
- `prompt_language`가 `en`으로 잡히면 대사 자체가 영어로 나간다. 한국어 대사를 넣었다면
  프롬프트 첫 줄에 한국어 발화임을 명시하고 응답에서 확인한다.

실제 오디오가 한국어로 발음됐는지는 **재생해야 안다** — 에이전트는 확인할 수 없으니 미검증으로 보고한다.

## 4. 상품 URL 임포트는 WAF 사이트에서 실패한다

`show_marketing_studio(action='fetch', url=...)`는 Akamai·Cloudflare로 보호된 커머스에서
`status: failed / "Failed to extract product data"`로 끝난다(실측: 쿠팡).

**우회 — 이미지로 직접 만든다**

1. 상품 페이지에서 **갤러리 이미지**를 뽑는다. 주의: 페이지 하단 *추천 상품* 배너를 긁으면
   **엉뚱한 제품**이 등록된다. 실측으로 한 번 당했다. 뷰포트 상단(대략 `top < 900`)에 있고
   크기가 큰 이미지만 취한다.
2. 썸네일 URL의 크기 세그먼트를 키우면 원본이 나오는 CDN이 많다(`48x48ex` → `1000x1000ex`).
3. `media_upload` → 바이트 PUT → `media_confirm` → `show_marketing_studio(action='create', type='product')`.
   `medias[]`에는 `value`(media id)와 **`url`을 함께** 넣어야 한다 — 서버가 media_input UUID를
   URL로 되돌리지 못한다.
4. `description`에 **색·형태·소재를 문장으로** 적는다. 생성 모델이 제품을 재현하는 근거가 이 텍스트다.

차단 사이트 접근은 `insane-search` 스킬, 로그인이 필요한 곳은 사용자 실제 브라우저(`aside`)를 쓴다.

## 5. 브랜드 로고를 생성 모델에 맡기지 마라

로고가 든 장면을 반복 생성하면 **마크가 갈수록 변질된다** — 흉내 → 뭉개짐 → 엉뚱한 글자.
실측: 브랜드 심볼이 재생성을 거치며 알파벳 두 글자로 붕괴했다.

- 실제 로고 파일이 있으면 **레퍼런스 이미지로 물린다.** 그것만으로 정확도가 급등한다.
- 그래도 안 되면 **생성은 장면까지만, 로고는 픽셀 합성**으로 얹는다. 형태를 픽셀로 고정하고
  음영·원근·초점·색만 장면에서 계산해 곱하면, 로고가 틀어질 수 없으면서 합성 티도 안 난다.
- 제품 패키지의 **로마자**는 비교적 잘 나온다. 한글은 거의 확실히 깨진다 — §6.

## 6. 화면에 한글을 넣지 마라

자막·간판·포장 문구 등 **한글 렌더링은 신뢰할 수 없다.** "깨지지 않게 해달라"는 요구를 만족시키는
확실한 방법은 **아예 등장시키지 않는 것**이다.

```
NO Korean lettering anywhere in frame. No signage, no captions, no subtitles,
no packaging text, no posters. Background surfaces stay plain.
If writing would otherwise appear on a surface, leave that surface empty.
```

자막이 필요하면 **렌더 후 로컬에서 얹는다**(영상 편집 도구 또는 ffmpeg `drawtext`).

## 7. 예산 — 시간과 크레딧

| 항목 | 실측 |
|---|---|
| Marketing Studio 영상 12초 | 발주~완료 **4~9분** (동시 여러 건이면 큐 대기 추가) |
| `duration` | 요청값이 모델 허용치로 **클램프**된다(10 요청 → 12로 나옴) |
| 실패(`nsfw`/사유 미제공) | **크레딧 환불** — 소액 실험을 두려워할 이유는 없다 |
| 이미지 2K 편집 1건 | 20~60초 |

`get_cost: true`로 사전 확인이 가능하다. 오래 걸리는 건 `jobs_wait`로 최대 15초씩 롱폴링하되,
`all_terminal:false`면 `poll_after_seconds`만큼 쉬고 다시 부른다.

## 8. 결과는 반드시 눈으로 검수한다

`status: completed`는 "렌더가 끝났다"일 뿐 "쓸 만하다"가 아니다. 다운로드 → 프레임 추출 → 확인.

```bash
ffprobe -v error -show_entries format=duration -show_entries stream=width,height \
  -of default=noprint_wrappers=1 out.mp4
for t in 1 3.5 6.5 9.5 11.5; do
  ffmpeg -y -v error -ss $t -i out.mp4 -frames:v 1 -vf scale=300:-1 /tmp/f_$t.png; done
ffmpeg -y -v error -i /tmp/f_1.png -i /tmp/f_3.5.png -i /tmp/f_6.5.png \
  -i /tmp/f_9.5.png -i /tmp/f_11.5.png -filter_complex hstack=inputs=5 /tmp/strip.png
ffmpeg -i out.mp4 -af volumedetect -f null - 2>&1 | grep mean_volume
```

`volumedetect`·`silencedetect`는 **info 레벨로 출력된다** — `-v error`를 붙이면 결과가 안 보여
"이상 없음"으로 오독한다.

**체크리스트**: 손에 든 물건이 프레임마다 손에 붙어 있나(공중 부양) · 제품 색·형태가 원본과 같나 ·
로고가 읽히나 · 화면에 한글이 없나 · 배경 로케이션이 타깃 시장과 맞나 · 오디오가 무음이 아닌가.

## 9. 실패했을 때 정직하게 가른다

| 증상 | 원인 | 다음 수 |
|---|---|---|
| `status: nsfw` | 어휘(대개) 또는 아바타 복장 | §2 표대로 치환 → 그래도면 아바타 교체 |
| 결과에 다른 사람이 나옴 | 아바타 미지정 → 자동 배정 | §1 `avatar_ids` |
| 대사가 어색·영어 | 한글 훼손 또는 `prompt_language` | §3 |
| 제품이 딴것 | 이미지 수집 오류 | §4-1 갤러리 재확인 |
| `failed`, 사유 없음 | 미확정 — 변수를 **하나만** 바꿔 재시도 | 두 개 동시에 바꾸면 원인을 영영 못 가린다 |

크레딧이 환불되므로 **변수 하나씩 바꾸는 실험이 최선의 진단**이다.

## 10. 하지 않는 것

- 사용자 라이브러리의 아바타·제품·생성물을 **삭제하지 않는다**. 정리는 사용자가 앱에서 한다.
- 결과를 확인하지 않고 "완료"라고 보고하지 않는다.
- 오디오 언어·발음처럼 **들어야 아는 것**을 들은 척하지 않는다 — 미검증으로 표기한다.
