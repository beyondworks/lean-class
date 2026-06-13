---
name: virtual-influencer-script
description: 버추얼 인플루언서용 숏폼 시나리오 작성 (Reels/Shorts/TikTok 15s~60s). 후크-바디-CTA 구조 + IG 알고리즘 + 협찬 통합 + 공정위 가상인물 라벨 규제 준수. 씬별 샷·대사·자막·SFX·캐릭터시트/Kling 프롬프트 매핑까지 한 번에 산출. 트리거 — "릴스 시나리오", "숏츠 대본", "AI 인플루언서 콘텐츠 기획", "버추얼 인플루언서 영상", "먹방 대본", "협찬 영상 기획", "스토리텔링", "shorts script", "AI 영상 시나리오", "리얼리티/언박싱 시나리오".
---

# Virtual Influencer Script — 버추얼 인플루언서 숏폼 시나리오

## 0. 이 스킬은 무엇을 만들어주나

15~60초 짜리 릴스/숏츠/틱톡 시나리오 1편을 다음 산출물로 출력한다.

1. **컨셉 한 줄** (후크 헤드라인)
2. **타임라인 표** (시간·샷타입·액션·대사·자막·SFX·BGM)
3. **씬별 캐릭터시트 프롬프트** (`ducktape-character-sheet` 호환 형식)
4. **씬별 Kling I2V 프롬프트** (`kling-image-to-video` 호환 형식)
5. **CapCut 자막 가이드** (폰트·색·외곽선·위치)
6. **CTA 카피 + 공정위 라벨 텍스트** (법규 준수)
7. **캡션 + 해시태그** (IG/TikTok 알고리즘 최적화)

## 1. 입력 수집 (없으면 5질문)

```
시나리오 빌더 시작 — 5가지 알려주세요:
1. 페르소나 (이름·나이·니치·시그니처 의상)
   예: "민지, 24세, 먹방, 핑크 트랙수트"
2. 콘텐츠 종류 (먹방 / OOTD / GRWM / 언박싱 / 리뷰 / 챌린지 / 협찬)
3. 협찬·어필리에이트 (브랜드명, 노출 강도, 가격/링크)
   "없음"도 가능
4. 길이 (15s / 30s / 45s / 60s) — 기본 30s 권장
5. 톤 (밝음/잔잔/ASMR/유머/도발/감성)
```

## 2. 후크 헤드라인 — 0~3초 안에 결판

- For meeting-minutes / Notion / Hermes automation content: stage the story in a real dark 8-person company meeting room, use Notion sample screens for laptop close-ups, show Hermes reading meeting notes and executing follow-up work, and keep human review as the trust anchor.
- When the user has supplied reaction/performance analysis data, read it before writing the script: do not write generic explanatory narration; use a cold hook, viewer-outcome language, concrete proof, trimmed B-roll for redundant scenes, and a keyword CTA.
- For virtual influencer/Kling reels with Korean dialogue or narration: do not rely on Kling native voices, generate all spoken lines with the approved Voicebox clone, extend video duration instead of cutting the voice, and send individual MP3s on mobile Telegram. If endings like `다/까/요` sound clipped, tail padding alone is insufficient; use the carrier-tail regeneration/trim workflow and verify with Whisper + waveform silence before delivery.

### 2.1 Start-frame-first video planning

- For company-life office vlogs involving the CEO, AI-agent employees, correction scenes, hidden iPhone filming, or hallucination/guessing satire: the CEO is the human operator, employees are personified AI agents, the humor comes from AI failure modes (hallucination, unverified claims, guessing), and the filming grammar should feel like real shaky/occluded iPhone footage rather than scripted drama. If the user is still refining story, write scenario/dialogue first and do not jump to image prompts.

한국 IG 알고리즘에서 검증된 6 패턴:

| 패턴 | 예시 | 적합 니치 |
|---|---|---|
| **정체 공개** | "이거 사실 AI예요" | 모든 (메타) |
| **충격적 가격** | "12,000원으로 이게 가능?" | 먹방, 쇼핑 |
| **반박** | "이거 진짜 다이어트에 좋다는데..." | 헬스, 뷰티 |
| **이상한 조합** | "치킨에 우유 찍어먹기" | 먹방 |
| **숫자 약속** | "30초 안에 끝나요" | 튜토리얼, 리뷰 |
| **시간/장소 hook** | "퇴근길에 발견한..." | 라이프스타일 |

후크 작성 규칙:
- 6~12 음절. 화면 상단 굵은 텍스트로
- 의문문 또는 미완결 ("...")로 다음 클립 강제 시청 유도
- 페르소나 1인칭으로 발화
- 성과/반응 분석 데이터를 제공한 주제는 먼저 분석 출처를 읽고, 첫 1~3초에 즉시 보상·반전·결과가 드러나게 쓴다. “툴 설명”보다 “시청자에게 남는 일/시간/돈/작업량 변화”를 우선한다.
- 업무 자동화 릴스에서 구구절절한 설명 문장은 실패 신호다. 각 대사는 hook / result / proof / trust / CTA 중 하나의 역할을 가져야 하며, 역할 없는 씬은 무대사 B-roll로 줄인다.

## 3. 30초 표준 구조 (가장 자주 쓰는 길이)

```
0-3s   HOOK         — 후크 헤드라인 화면 + 페르소나 정면 + 미세 모션
3-10s  SETUP        — 상황 제시 (장소, 무엇을 할 것인지)
10-22s BODY         — 메인 액션 2~3컷 (먹는 모션, 마시는 모션, 보여주기)
22-28s CLIMAX       — 리액션 (놀람·만족 표정 클로즈업)
28-30s CTA          — 다음 행동 유도 ("링크는 바이오에" / "팔로우 하면...")
```

15s: HOOK + BODY(1컷) + CLIMAX + CTA로 축약
60s: SETUP을 2단계로 분리, BODY 4~5컷, story arc 추가

### 3.1 Friend-shot / 출사 브이로그형 Reels 구조

"인스타 릴스에 많이 올라오는 장면 전환, 컷 편집, 중간 나레이션, 영상에서 말하는 느낌"을 원하면 5개 메인 이미지를 5개 긴 클립으로 늘리지 말고, **9–12개 편집 컷**으로 쪼갠다. 메인 컷 5장 + B-roll 3–4장 + 짧은 토킹 컷 1–2장을 기본으로 한다.

### 3.1.1 Office-vlog / AI-agent satire rule

For company-life Reels: the CEO/representative is the human operator, the employees are humanized AI agents, and the office scenes satirize hallucination, speculative answers, unverified confidence, silent automation failure, and "done" without artifacts. Do not write these as drama or broad comedy. The CEO is not a comedian or bully; he is humane, quick to recognize good work, and operationally strict. The virtual influencer should capture the moment like real iPhone office footage: hidden/obstructed angles, distant voices, autofocus hunting, camera shake, and minimal inner monologue.

- 메인 감정/액션 컷: 3–5초
- B-roll 컷: 0.5–2초
- 토킹 컷: 2–4초, 친구에게 말하는 짧은 한 문장
- 대부분의 정보는 VO 나레이션으로 처리하고, 입모양이 필요한 대사는 최소화
- iPhone friend-shot 컨셉이면 전문 카메라 무브보다 handheld sway, jump cut, whip-ish micro transition, footstep/camera strap/shutter SFX를 우선한다

### 3.2 Approved-still-first animatic workflow

If the user has already confirmed a still image/model frame, do not jump straight to expensive I2V. First create a short animatic from the approved still to validate story, subtitles, VO tone, and pacing.

### 3.3 No-overlay image/video mode

If the user says or implies no captions/text overlays, remove all on-screen text guidance from the production plan: no captions, subtitles, CTA text, AI labels, or typography specs inside generated images/videos. Keep dialogue/voiceover as spoken Korean audio only. For realism-first virtual influencer reels, prioritize Korean female voice, accurate lip-sync, restrained expression, mic below lips, and image/video realism over caption design.

- Save the confirmed still in an `approved/` folder.
- Derive 3–5 vertical 1080×1920 frames: main frame, product/desk detail, face close-up, space detail, ending frame.
- Add Korean captions and a small `AI Generated` label.
- Export a 20–30s MP4 as a **rough animatic / pre-Kling pass**.
- Tell the user clearly that this is not final motion yet; after approval, split it into 3–5s Kling clips.

## 4. 6개 검증된 시나리오 템플릿

상세는에. 여기는 1줄 요약.

| 템플릿 | 구조 | 적합 길이 | 핵심 |
|---|---|---|---|
| **MUKBANG-30** | 차안 후크 → 음식 들이밀기 → 한입 → 디핑 → 음료 → CTA | 30s | ASMR 크런치 SFX 필수 |
| **OOTD-15** | 거울셀카 → 의상 1번 → 컷 → 의상 2번 → 컷 → 의상 3번 → 출입문 워킹 | 15s | 점프컷, 동일 카메라 앵글 |
| **GRWM-45** | 민낯 → 클렌징 → 토너 → 메이크업 → 헤어 → 최종 룩 → CTA | 45s | 제품 라벨 verbatim 노출 |
| **UNBOX-30** | 박스 들고 들어옴 → 칼 컷 → 언박싱 → 첫 반응 → 제품 정면 → CTA | 30s | "이거 가격이..." 후크 |
| **REVIEW-60** | 후크 → 제품 소개 → 실사용 3컷 → 비교 → 결론 → 평점 자막 | 60s | 중간에 retention spike 필수 |
| **CHALLENGE-15** | 시작 자세 → 액션 → 실패/성공 → 리액션 | 15s | 트렌드 BGM 활용 |

## 5. 협찬 통합 패턴 (브랜드 부드럽게 끼우기)

참조 영상(쿠팡이츠 12,000원 + 펩시 제로)의 **이중 협찬 통합** 패턴:

```
프라이머리 브랜드 (배달앱/이커머스)
  ↓ 폰 화면으로 자연 노출 (앱 화면, 가격, "결제하기" 버튼)
  ↓ 페르소나 표정 "안 깨지는 거" 같은 자연 멘트
  ↓ 가격은 미끼 (가성비 어필) — 너무 비싸면 거부감

세컨더리 브랜드 (F&B / 소품)
  ↓ 자연스럽게 같이 노출 (페르소나가 마시는/들고있는 제품)
  ↓ 라벨이 카메라 정면을 향하는 1컷
```

협찬 노출 강도 3등급:
- **A (Hard sell)**: 박스 언박싱, 제품 정면, 가격, CTA에 브랜드명
- **B (Soft sell)**: 페르소나가 자연스럽게 사용, 라벨 한 번
- **C (Native)**: 배경 소품으로만 등장 (간접광고)

가격은 단가 결정 시 협조:
- A = 100% 표시 단가
- B = 60~80%
- C = 30~50%

## 6. 공정위 라벨 — 안 지키면 5배 징벌배상 (2026.1분기 시행)

**영상 자산 기본값:** 생성 이미지/영상 자체에는 자막, CTA 텍스트, `AI Generated` 라벨, 캡션 오버레이를 넣지 않는다. 사용자가 명시적으로 요청하거나 최종 게시용 컴플라이언스 레이어를 만드는 단계에서만 별도 후편집 레이어로 추가한다. 시나리오/프롬프트 단계에서는 화면 자체의 구도·연기·음성·입모양·소품으로 메시지를 전달한다.

**게시/협찬 단계에서 필요한 시각적 표시**는 별도 편집 레이어로 처리:
- 영상 어딘가에 텍스트로 `AI 생성 영상` 또는 `가상인물` (최소 0.5초 노출)
- 협찬은 본문 첫 줄에 `#광고` 또는 `#협찬` (#AD 무방하나 한글 #광고 권장)
- 위치·인식·명확·언어동일성 4원칙 — 첨자 작게 박는 거 금지

자동 삽입할 텍스트는 사용자가 최종 게시/컴플라이언스 레이어를 요청했을 때만 제안한다:
```
화면 모서리: "AI Generated"  (검정 외곽선 흰글자, 8~12pt)
캡션 첫줄:  "#AI #광고 (브랜드명)"
```

## 7. 캡션·해시태그 (IG 알고리즘 2026.05 기준)

캡션 구조:
```
[후크 한 줄, 본문보다 2배 크게]

[본문 2~4 문장, 페르소나 1인칭, 줄바꿈 적극]

[CTA 1 문장: "프로필 링크에서..." / "댓글로 알려주세요"]

[해시태그 5~8개]
#AI #광고 #먹방 #쿠팡이츠 #서울맛집 [니치 특화 1~2]
```

해시태그 룰:
- 5~8개가 sweet spot. 30개 도배는 알고리즘 감점
- 첫 줄에 `#AI #광고` 필수 (공정위 + IG AI Creator 라벨 동시 대응)
- 니치 해시태그는 follow 많은 것 1개 + 작은 거 2~3개 mix

## 8.1 No-overlay / realism preference

For virtual influencer reels, do not default to captions, CTA overlays, subtitles, or `AI Generated` labels inside generated frames/videos unless the user explicitly asks. The default storyboard should focus on shot purpose, blocking, camera, lighting, expression, motion, voice, and lip-sync. If disclosure/captions are needed later, handle them as a separate editing layer after image/video approval.

If a storyboard calls for multiple AI employees or persona variants, do not force the scene into a narrow personal desk room. Revise blocking like a cinematographer:
- presenter/talking shots: close-up or seated half-body;
- team/employee work shots: wider office B-roll without foreground presenter;
- day/night/morning variants: same camera angle and desk/laptop positions;
- if physical staging feels forced, change the room or split the shot before writing image prompts.

For meeting-minutes / Notion / Hermes automation content, the room should usually be a real company meeting scene rather than the virtual influencer's personal space: dark 8-person meeting room, PPT screen, open laptops, coffee/cables/notebooks, and restrained natural meeting gestures. Start with an approved meeting-room master plate before writing scene still prompts for Notion close-ups, Hermes task extraction, human review, and CTA shots.

For meeting-minutes, Notion, or Hermes workflow reels, stage the content in an actual company context when the story is about company work: e.g. a dark 8-person meeting room, PPT screen, open laptops, natural meeting gestures, and Notion meeting-note laptop close-ups. Use provided Notion screenshots/screen recordings as laptop UI references; if exact Korean UI text matters, composite it in post instead of relying on generated tiny text.

## 8. CapCut 자막 가이드 (한국 viral 스타일)

### 8.0 No-overlay override for realism-first reels

If the user says not to add captions/text overlays, or if the task is a realism-first virtual influencer image/video generation pass, do **not** add subtitles, CTA text, `AI Generated` corner labels, typography specs, or caption overlays into the generated image/video prompts. Keep spoken dialogue and audio/lip-sync planning, but design only the frame, acting, space, props, camera, lighting, and motion. Put any disclosure/CTA outside the generated image/video only if the user asks for publishing copy.

Default overlay sections below apply only when the user asks for edited social-video deliverables with captions/CapCut guidance.

| 요소 | 권장 |
|---|---|
| **폰트** | Pretendard Bold / Noto Sans KR Bold |
| **본문 색** | 흰색 #FFFFFF |
| **외곽선** | 검정 #000000, 2~3pt |
| **하이라이트** | 노란색 #FFE600 또는 핑크 #FF5C8A (단어 단위 강조) |
| **크기** | 화면 높이의 6~8% (1920×1080 기준 110~140pt) |
| **위치** | 화면 하단 1/3 또는 중앙 (인스타 데드존 회피: 하단 250px, 상단 220px) |
| **출현** | 자동 자막 + 단어 단위 pop-in 애니메이션 |
| **줄바꿈** | 한 줄 12~14자, 최대 2줄 |

후크 텍스트(상단 큰 글자)는 별도:
- 크기 화면 높이의 12~16%
- 색은 흰색 또는 핑크 (페르소나 시그니처 색)
- 외곽선 두껍게 4~6pt
- 첫 3초 페이드 인 → 5초까지 유지

## 9. 출력 포맷 (사용자에게 줄 최종 형태)

### Kling 프롬프트 전달 선호

Kling/이미지-투-비디오 프롬프트를 요청받으면 장황한 분석형 문서보다 **작업자가 그대로 복붙할 수 있는 씬별 블록**을 먼저 제공한다.

필수 순서:

```text
Scene 01
- Start Frame: 01 / filename.jpg
- End Frame: 02 / filename.jpg
- Duration: 5초 또는 3~15초 중 지정값
- Prompt: [풀 프롬프트]
- Negative Prompt: [풀 네거티브]
```

원칙:
- “어떤 이미지 넣고, 몇 초로 설정하고, 어떤 프롬프트를 붙여넣는지”가 즉시 보여야 한다.
- 운영 원리/실패 원인/편집 팁은 씬별 블록 뒤에 짧게 둔다.
- Kling 3.0 native audio 토글형 UI에서는 대사를 프롬프트 안에 따옴표로 넣되, a virtual influencer처럼 목소리 일관성이 중요한 릴스는 최종 음성 소스로 쓰지 않는다. 최종 편집에서는 Kling audio를 mute하고 Voicebox clone MP3를 씬별로 얹는다.
- 립싱크가 중요한 한국어 토킹 영상은 5초 전후, 한 씬 한 문장, 카메라/손/배경 움직임 최소화를 기본값으로 둔다.
- Voicebox 대사가 예정 클립 길이보다 길면 사용자 승인 없이 끝음을 자르지 말고 클립 길이를 늘리는 쪽을 우선한다. `다/까/요/록` 같은 문장 끝음이 잘리지 않도록 0.65초 이상 tail padding을 둔다.


```markdown
# [후크 헤드라인] — [길이] [니치]

## 컨셉
한 줄 요약

## 타임라인
| 시간 | 샷 | 캐릭터/액션 | 대사/자막 | 카메라 | SFX/BGM |
|---|---|---|---|---|---|
| 0-3s | MS | 페르소나 정면 후크 | "[헤드라인]" | static | hook BGM intro |
| 3-7s | CU | [액션] | "[대사]" | slight push-in | crunch |
| ... | ... | ... | ... | ... | ... |

## 씬별 캐릭터시트 프롬프트
(ducktape-character-sheet 스킬 호환)

### Scene 1 (0-3s)
```
[GPT Image 2 프롬프트, 5-튜플 DNA + reference attach 안내 포함]
```

### Scene 2 (3-7s)
...

## 씬별 Kling I2V 프롬프트
(kling-image-to-video 스킬 호환)

### Clip 1 (0-3s, 5s 클립)
```
[Kling 프롬프트, 20-40 단어, negative 포함]
```

### Clip 2 ...

## CapCut 설정
- 폰트: Pretendard Bold 120pt
- 본문 색: #FFFFFF + 검정 외곽선 2pt
- 후크 색: #FF5C8A + 외곽선 4pt
- 자막 위치: 하단 1/3
- BGM: [곡 추천 + 볼륨 30%]
- SFX: crunch (먹는 컷), pop (전환), woosh (CTA)

## CTA + 협찬 라벨
화면: "AI Generated" (우하단, 흰글자 검정 외곽선)
캡션 첫줄: #AI #광고 #[브랜드]
CTA 문구: "[자연 멘트]"

## 캡션 (인스타)
[후크 라인]

[본문 2~4줄]

[CTA]

#AI #광고 #[니치] #[브랜드] #[추가 4~5개]
```

## 10. 의사결정 체크리스트 (사용자에게 출력 전)

- [ ] 사용자가 제공한 반응 데이터/분석 리포트가 있으면 실제 파일을 읽고 반영했는가; 없으면 분석 기반이라고 주장하지 않았는가
- [ ] 첫 1초에 AI/자동화/결과 중 하나가 즉시 인지되는가
- [ ] 중복되거나 새 정보가 없는 대사는 B-roll/전환 컷으로 줄였는가
- [ ] 확정 이미지에 대본을 적용할 수 있는지 씬별로 검토했고, 신규 생성/후합성/프롬프트 수정 중 무엇이 필요한지 분류했는가
- [ ] 후크가 0~3초 안에 명확한 약속/궁금증을 만드는가
- [ ] 30초면 액션이 3~4개 이상, 15초면 1~2개로 압축됐는가
- [ ] CTA가 1줄 + 시각적으로 명확한가
- [ ] 협찬 노출이 페르소나 톤과 자연스럽게 융합됐는가
- [ ] 화면에 "AI Generated" 라벨이 들어가는가 (2026 법규)
- [ ] 캡션 첫 줄에 `#AI` + `#광고`(협찬 시) 있는가
- [ ] 자막 가이드가 한국 viral 표준(흰글자 검정 외곽선, Pretendard Bold)인가
- [ ] 씬별 프롬프트가 ducktape-character-sheet · kling-image-to-video와 호환되는가
- [ ] Kling 음성 작업이면 Kling native voice를 최종 소스로 쓰지 않고, Voicebox clone MP3를 모든 대사/나레이션에 적용했는가
- [ ] Each MP3 has passed end-syllable QA: if `다/까/요/록` sounds clipped, do not rely on silence padding; regenerate with carrier-tail workflow, trim before the carrier, append 0.9–1.0s silence, and verify by Whisper plus waveform/volume silence.
- [ ] 외부/모바일 Telegram 전달이면 오디오 ZIP만 보내지 말고 씬별 개별 MP3를 재생 가능하게 보냈는가

## 11. 더 깊이 — references/


## 12. 자매 스킬 체인

```
virtual-influencer-script (시나리오 산출)
   ↓ 씬별 캐릭터 프롬프트
ducktape-character-sheet (캐릭터/씬 이미지)
   ↓ 정지 이미지
kling-image-to-video (영상 클립)
   ↓
CapCut 편집 → IG Reels
```

스킬 호출 순서 사용자에게 안내: "시나리오 → 시트/씬 → 영상 → 편집". 한 번에 모두 진행하려면 단계별 결과 확인 후 다음 스킬 호출.
