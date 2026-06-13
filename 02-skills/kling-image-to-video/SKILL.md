---
name: kling-image-to-video
description: 정지 이미지 → Kling AI 영상 생성을 위한 프롬프트 최적화. 인물 일관성·텍스트 깨짐 방지·오디오 안정·대사와 입모양 싱크·End-frame 스티칭까지. Kling 1.6 Pro/2.5 Turbo/2.6 Pro/3.0/O3 버전별 매핑. 트리거 — "Kling 프롬프트", "이미지를 영상으로", "image-to-video", "I2V", "캐릭터 애니메이션", "정지 사진 영상화", "립싱크 영상", "AI 영상 프롬프트", "클링", "AI 인플루언서 영상 만들기".
---

# Kling Image-to-Video Prompt Optimizer

## 0. 무엇을 해주나

캐릭터 시트(=정지 이미지)에서 자연스러운 2~10초 영상 클립을 만들기 위한 Kling 프롬프트를 산출한다. 인물 일관성·텍스트·오디오 일관성·립싱크 호환까지 4축 최적화.

대상 모델: **Kling 1.6 Pro Elements** (가성비 최선) / **Kling 2.6 Pro Motion Control** (모션 캡처) / **Kling 3.0 Multi-Shot** (한 배치 5컷) / **O3 Omni** (A/V 동시 생성).
([상세 비교](~/Agents/Image-gen/research/02-kling-image-to-video.md))

## 1. 입력 수집 (없으면 4질문)

```
Kling 프롬프트 빌더 시작 — 4가지 알려주세요:
1. 입력 이미지 종류 (베이스 정면 / 액션 컷 / 풀바디 / 브랜드 로고 포함)
2. 원하는 액션 (먹기 / 마시기 / 걷기 / 토킹 / 보여주기 / 표정 변화 / 카메라 무브)
3. 클립 길이 (3s / 5s / 7s / 10s) — 기본 5s 권장
4. 추가 옵션 (립싱크 필요? / 오디오 포함? / 텍스트/로고 픽셀 락 필요?)
```

## 2. 5대 황금 원칙 (이 5개 어기면 무조건 망함)

1. **외형 묘사 금지** — 이미지에 이미 있는 얼굴·의상·배경은 절대 재서술하지 마라. **모션만 20~40 단어**로
2. **1 클립 = 1 액션 + 1 카메라 무브** — 2개 이상 욱여넣으면 워핑 폭발
3. **약한 동사** — subtle / slow / micro / gentle / barely / just. 공격적 동사(dances wildly, jumps, swings) = 신체 구조 붕괴
4. **언어 선택** — Kling은 영어가 30~40% 더 정확. 한국어로 던지려면 프롬프트창의 `T` 버튼 자동 영어 변환 거치기
5. **negative 구체적으로** — "bad anatomy" 같은 모호 표현 0 효과. `no face morphing, no finger duplication, no hair color change, no identity change`처럼 구체적으로

## 3. 버전별 결정 가이드 (2026.05)

| 작업 | 추천 버전 | 5s 비용 | 이유 |
|---|---|---|---|
| AI 인플루언서 일반 클립 | **Kling 1.6 Pro Elements** | 35 credits ≈ $0.25 | 가성비 최고, 1-4 reference image 슬롯 |
| 모션 브러시 (머리만/옷만 움직임) | **Kling 1.5 Master** | — | 1.6+에서 모션 브러시 제거됨 (fallback) |
| 6축 카메라 + 모션 캡처 | **Kling 2.6 Pro Motion Control** | 420 credits | 참조 영상 동작 복제 |
| 5컷 동일 인물 1배치 | **Kling 3.0 Multi-Shot** | — | 한 generation으로 멀티샷 |
| 영상+오디오 동시 | **Kling 2.6 Pro w/ audio** / **O3 Omni** | 50 credits / — | 립싱크 별도 처리 불필요 |
| 무료 테스트 | **Kling Standard 720p** | 10 credits, 66 free/day | 워터마크 있음 |

## 4. 인물 일관성 — 5~10 클립이 모두 같은 사람으로 보이게 하기

가장 큰 도전. 6 전략을 stack해야 한다:

### 전략 A. **Multi-Image Elements (1.6+ 핵심)**
- Kling 웹에서 AI Video → Elements → 1~4장 jpg/png 업로드
- 같은 인물의 다양한 각도가 best (정면·측면·뒤·디테일)
- 의상도 별도 슬롯에 → "핑크 트레이닝복" 같은 의상 픽셀 락
- 캐릭터 시트의 표정 클로즈업 컷을 **Element #1**로 (얼굴 인지력 최대화)

### 전략 B. **얼굴 클로즈업 우선**
캐릭터 시트 중 **얼굴이 큰 컷**을 Element #1로. 얼굴 거리가 멀수록 모델이 디테일을 추정해야 해서 drift 폭증.

### 전략 C. **Half-body framing**
손·다리가 얼굴에서 멀수록 실패 확률 ↑. medium shot (가슴~허벅지 부분)이 가장 안전. 풀바디 + 액션이면 손가락 distortion 빈발.

### 전략 D. **End-Frame 체인** (긴 영상의 결정타)
클립 N의 마지막 프레임을 export → 클립 N+1의 start frame으로. 5컷 후에도 동일 얼굴 유지.
지원 버전: Kling 1.6 Pro / 2.1 Pro / 2.6 Pro / 3.0

### 전략 E. **Same seed + 동일 prompt prefix** (API)
2.1+ API에서 seed 고정. 캐릭터 description 부분을 prefix로 동일하게, 모션 부분만 변경.

### 전략 F. **Motion Control (2.6+)** — 참조 영상에서 동작만, 캐릭터는 고정
댄스·먹방·운동 같은 복잡 동작에서 5컷 모두 같은 인물 보장.

**기본 권장 조합**: 전략 A + B + C + D를 항상 stack. 협찬·중요 컷은 E도 추가.

## 5. 7가지 액션 템플릿 (verbatim 프롬프트)

### 5.1 미세 모션 — 가장 안전, 페이스 드리프트 최소

```
[KLING-SUBTLE · 정지 컷 살리기]
Subject blinks naturally and forms a slight smile, hair moves gently as 
if in a soft breeze, background remains static.
```

### 5.2 먹기 (mukbang)

```
[KLING-EAT-BITE · 한입]
Subject raises [food] to mouth, takes a small bite, lowers hand, chews 
twice with eyes closed in satisfaction. Camera holds static medium 
close-up. Background bokeh unchanged.
Negative: hand morph, finger duplication, food warping, jaw distortion.
```

```
[KLING-EAT-CHEW · 씹기·삼키기]
Subject chews slowly with closed mouth, jaw moves up and down twice, 
slight smile emerges after swallow, eyes blink once. Camera static. 
Hair gently sways in indoor airflow. Maintain original lighting.
Negative: motion blur, face distortion, lip wobble, identity change.
```

### 5.3 마시기 (음료)

```
[KLING-DRINK-CAN · 캔 sip]
Subject raises [can/cup] to lips, takes a small sip, throat swallows 
once, lowers can. Condensation droplet slides down can side. Camera 
static. Background unchanged. 5s.
Negative: can label distortion, throat warp, hand drift, finger count change.
```

### 5.4 토킹 헤드 (립싱크 base)

```
[KLING-TALK-BASE · 립싱크 직전 base 영상]
Subject's head makes small natural tilt right then return, eyes maintain 
camera contact, shoulders quiet. Mouth closed, no talking. Camera holds 
medium close-up static.
Negative: lip movement, mouth open, jaw shift, identity change.
```

⚠️ **중요**: 립싱크는 base 영상의 입이 이미 움직이면 sync 실패율 매우 높음. base는 "mouth closed, no talking" 명시.

### 5.5 워킹

```
[KLING-WALK · 카메라 옆 통과]
Subject walks from right edge of frame to left edge at relaxed pace 
3 steps, slight hair sway, neutral expression, looks briefly at camera 
mid-stride then back forward. Camera static eye-level. Background 
buildings unchanged.
Negative: leg duplication, foot warp, hair explosion, identity drift.
```

### 5.6 폰/제품 보여주기 (텍스트 픽셀 락 — 광고 필수)

```
[KLING-SHOW · 화면을 카메라에]
Subject lifts phone toward camera with screen facing lens, holds steady 
2 seconds, soft pleased smile, then lowers phone back to chest. Screen 
content unchanged (preserve label text). Camera static.
Negative: phone screen morph, text scramble, hand jitter, identity change.
```

### 5.7 카메라 무브 only

```
[KLING-PUSH-IN · 슬로우 push-in 후크]
Camera pushes in slowly toward subject's face 15% over 5 seconds. 
Subject's eyes blink twice, slight breath movement at shoulders, micro 
smile emerges at end. Background bokeh deepens. Lighting unchanged.
Negative: zoom artifact, edge warping, face distortion.
```

```
[KLING-HANDHELD · "AI 같지 않은" 자연스러움]
Subtle handheld camera shake, 2-3% organic sway, micro pan left then 
right by 3 degrees, subject stationary, soft breath movement. 
"Vlog authenticity" feel. Maintain composition.
Negative: shake aggressive, vertigo, jump cut, drift.
```

## 6. WaveSpeed 구조화 패턴 (먹방·음료 액션의 결정타)

손/어깨 hike가 먹방·음료 컷을 망친다. WaveSpeed 패턴이 가장 효과적:

```
[액션 요약]: [actor: <부위>] [action: <동작>] [timing: <초~초>] 
[constraint: <고정할 부위>] [negative: <금지>]
```

예시:
```
Cup lift without shoulder hike: [actor: right hand] [action: lift ceramic 
cup, sip, replace] [timing: 1.0-2.5s] [constraint: shoulder and neck 
quiet, minimal elbow] [negative: no camera move, no steam surge].
```

## 7. 텍스트 안 깨지는 법

Kling은 이미지 안의 텍스트(폰 화면, 라벨, 포스터, 자막)가 모션 중에 morph되는 경향. 대응:

1. **입력 이미지에 텍스트 픽셀 락**을 미리 (ducktape `[DUCT-02]` 패턴으로 GPT Image 2에서 verbatim 생성)
2. Kling 프롬프트에 명시: `Screen content unchanged. Preserve all text exactly. No text morph.`
3. Negative: `text scramble, text morph, label distortion, character shift`
4. 클립 길이를 **3s로 짧게** — 길수록 텍스트 안정성 저하
5. 카메라 무브를 static으로 — 무브하면 텍스트 perspective 시 거의 무조건 깨짐
6. 텍스트 노출 컷은 별도 클립으로 분리, 다른 컷과 stitch

## 8. 오디오 안 깨지는 법 (Kling 2.6 audio / O3 Omni)

native audio 생성 모델에서 오디오 품질 안정시키는 법:

1. **명확한 사운드 묘사** — "soft chewing sound, light crunch" 처럼
2. **단일 사운드 소스** — 여러 SFX를 한 클립에 욱여넣지 마라
3. **배경 정적 유지** — 모션 많으면 오디오도 같이 morph
4. **대사 길이 ≤ 2초** — 5초 클립에 대사는 2초까지가 안정
5. 오디오 안정성이 낮으면 → base 영상은 무음으로 생성 → 별도 TTS(ElevenLabs v3) + Hedra 립싱크가 더 안전

## 9. 립싱크 — 대사·입모양 일치

3가지 경로 중 선택:

### 샘플 영상 클론형 토킹 인플루언서 주의
- 샘플 영상과 거의 같은 말하기 영상을 만들 때도 Kling에는 먼저 **무언 base**를 만든다. 원본 샘플의 입 움직임을 직접 프롬프트로 과하게 묘사하지 말고, `mouth closed, no talking` base → lip-sync 순서로 간다.
- 샘플 영상은 초 단위로 `head tilt / blink / shoulder breath / hand motion / camera move / mouth state`를 분해하고, Kling 프롬프트는 각 클립당 **1 action + 1 camera move**만 넣는다.
- 실제 인물/모델 이미지 기반의 현실적 말하기 영상은 권한 확인 후 진행한다.

### 경로 A. **Kling 자체 립싱크** (단순)
1. Base 영상 생성: `mouth closed, no talking` 명시 (KLING-TALK-BASE)
2. Kling Lip-Sync 메뉴: 오디오 파일(≤10s, ≤100MB, MP3/WAV) 업로드 또는 TTS 텍스트 입력
3. 출력: 입만 덮어쓴 영상

### 경로 B. **Hedra Character-3** (Talking photo 최강)
- 정지 사진 + 오디오 → 자연스러운 토킹 헤드 영상 직접 생성
- Kling 자체 립싱크보다 인물 정체성 유지 우수
- $19/mo Creator로 ~30컷 가능

### 경로 C. **Sync.so + ElevenLabs v3** (프로 워크플로)
1. ElevenLabs v3 Multilingual로 한국어 TTS 생성 (PVC 음성 락)
2. Kling으로 base 영상 (mouth closed)
3. Sync.so API로 립싱크 합성
- $19/mo Creator로 한국어 감정 표현 우수

립싱크 실패 빈발 원인 + 대응:
| 원인 | 대응 |
|---|---|
| base에 이미 입 움직임 | "mouth closed, no talking" 강제 |
| 얼굴이 사이드/3/4 | 정면 클로즈업 base만 사용 |
| 720p 이하 base | 1080p 권장 |
| 한국어 액센트 시프트 | Hedra Character-3 사용 (다국어 강함) |
| 클립 > 10s | 10s로 자르고 분할 처리 |

## 10. End-Frame 스티칭으로 30초 릴 만들기

5초 클립 6개로 30초 릴을 만드는 표준 워크플로:

```
1. 캐릭터 시트 정면(A), 측면(B), 의상 디테일(C) → Elements 슬롯에 업로드
2. 클립 1 (먹방 setup): start = A, end = A_변형(포크 들고 입 근처). 5s
3. 클립 2 (한입): 클립1 마지막 프레임 export → 클립2 start로. end = 입에 무는 컷. 5s
4. 클립 3 (음료): 동일 방식 체인. 5s
5. 클립 4 (폰 화면): 동일. 5s
6. 클립 5 (워킹): 외부 컷. 7s
7. 클립 6 (CTA): 정면 토킹 + 립싱크. 3s
8. CapCut에서 stitch + 자막 + 음악
```

**Pro tip**: "Prompt lightly: Kling can work great without the prompt. Add small details when you need exact camera or action control." — Higgsfield 공식.

## 11. 표준 negative prompt 세트

모든 캐릭터 클립에 기본으로 추가:

```
blur, distortion, watermark, text overlay, low quality, compression 
artifacts, flickering, inconsistent lighting, morphing faces, extra 
limbs, unnatural physics, warping fingers, extra fingers, deformed 
hands, identity drift, face stretch, hair color change, outfit color 
shift
```

립싱크 base 영상에는 추가:
```
lip movement, mouth open, jaw shift, teeth multiply
```

텍스트/로고 포함 클립에는 추가:
```
text scramble, text morph, label distortion, character shift, logo 
warping
```

## 12. 비용 최적화 — 30초 릴 최저가

| 시나리오 | 모델 | 클립 수 | 총 credits | API USD |
|---|---|---|---|---|
| 무료 테스트 (워터마크 OK) | Kling Standard 720p | 6 × 5s | 60 | $0 (무료 66cr/day) |
| 표준 (1080p, 인물 일관성) | Kling 1.6 Pro Elements | 6 × 5s | 210 | ~$1.50 |
| 프로 (모션 캡처) | Kling 2.6 Pro Motion Control | 6 × 5s | 2520 | ~$15 |
| 최고급 | Kling 3.0 Multi-Shot + O3 Omni audio | — | — | $30+ |

**권장 운영**: 정적 컷은 Standard, 동적·중요 컷은 Pro로 mix. 후처리 Topaz upscale로 모든 컷을 4K로 통일.

## 13. 출력 포맷 (사용자에게 줄 최종 형태)

```markdown
# Kling 프롬프트 — [액션 요약]

## 메타
- 모델: Kling [version]
- 길이: [N]s
- 입력: [이미지 종류]
- Elements 슬롯: [#1 = 정면 클로즈업, #2 = 의상 디테일, ...]

## 프롬프트
```
[20-40 단어 액션 + 카메라 + 배경 처리]
```

## Negative Prompt
```
[표준 세트 + 클립 특수 negative]
```

## 추가 설정
- Aspect Ratio: 9:16 (Reels) / 16:9 (YouTube) / 1:1 (캐러셀)
- Mode: Pro 1080p (인물 우선) / Standard 720p (테스트)
- Duration: 5s 권장 (3s = 짧고 안정, 10s = drift 위험)
- Camera Orientation Matches Image: ON (텍스트로 카메라 독립 조작 시)

## 립싱크 (필요 시)
- Base 영상 처리: [경로 A/B/C 중 선택 + 단계]
- 오디오: [TTS 도구 + 음성 ID]

## End-Frame 다음 클립 안내
이 클립의 last frame을 export → 다음 클립의 start frame으로 사용.
다음 클립 추천 액션: [예: KLING-DRINK-CAN]
```

## 14. 출력 전 체크리스트

- [ ] 외형 묘사가 없는가 (이미지가 이미 함)
- [ ] 액션 1개 + 카메라 무브 1개로 제한됐는가
- [ ] 동사가 subtle/slow/micro/gentle 톤다운됐는가
- [ ] negative가 구체적이고 표준 세트를 포함하는가
- [ ] 텍스트 포함 클립이면 "Screen content unchanged" + text negative 추가
- [ ] 립싱크 예정이면 base는 "mouth closed, no talking" 명시
- [ ] Elements 슬롯 배정 (얼굴 클로즈업 #1)이 명시됐는가
- [ ] 길이가 3~5s sweet spot인가 (10s는 명확한 이유 있을 때만)
- [ ] 영어 프롬프트인가 (한국어면 T 버튼 안내)

## 15. 더 깊이 — references/


상세 리서치: [~/Agents/Image-gen/research/02-kling-image-to-video.md](~/Agents/Image-gen/research/02-kling-image-to-video.md)

## 16. 자매 스킬

- 캐릭터 시트가 없다면 → 먼저 `ducktape-character-sheet` 스킬로 베이스 생성
- 시나리오부터 시작이면 → `virtual-influencer-script` 스킬로 씬 분해 → 그 다음 본 스킬
