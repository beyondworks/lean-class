# Photoreal Mastery — 실물 구분 불가 수준 인물 사진 (요약)

> 본 요약은 빠른 인보크 용도. 전체 통합 마스터 가이드: [$HOME/Agents/Image-gen/research/09-ducktape-photoreal-mastery.md]($HOME/Agents/Image-gen/research/09-ducktape-photoreal-mastery.md)
>
> 4개 도메인 병렬 리서치 결과(09-A 기술 / 09-B 커뮤니티 / 09-C 학술 / 09-D Identity)의 통합 핵심.

---

## 1. 포토리얼 5대 원칙 — 동시 충족 필수

1. **Imperfection First** — 결점을 먼저 박는다 (visible pores, asymmetry, sebum, flyaway hair, no plastic skin, no over-smoothing)
2. **비-프로 카메라 ID** — iPhone RAW / 1990s CCD / Kodak Portra 400이 광고 카메라보다 photoreal에 강력
3. **단일 광원 + 패턴 + 각도** — Rembrandt/Loop/Split/Butterfly/Broad + 정확한 각도/색온도 명시
4. **Identity Anchor 3중 강제** — Reference 첨부 + 5-튜플 DNA prefix + EXACT 자연어 반복
5. **Multi-ref 8축 lock** — Color/Light/Shadow/Edge/Perspective/Grain/Atmospheric/Hero 자연어로 모두 명시

## 2. 5-슬롯 프롬프트 빌더 (SKILL.md §1.1과 결합)

```
SLOT 1 · DNA Anchor (디테일 2-3개만, 8개+ 금지)
SLOT 2 · Camera Lock (카메라 ID + 렌즈 + 조리개 + 색과학)
SLOT 3 · Lighting (패턴 + 각도 + 색온도 + key:fill 비율)
SLOT 4 · Pose + Expression (FACS Duchenne / 손배치 Vogue rules / 시선)
SLOT 5 · Negative + Imperfection (자연어 nega 5요소)
```

## 3. 6 마스터 템플릿 시그니처 토큰

| 템플릿 | 핵심 시그니처 |
|---|---|
| A. Identity Anchor | Leica SL2 50mm f/1.4 + north window + Rembrandt + 9-head |
| B. 자연 캔디드 | Kodak Portra 400 + Contax T2 38mm + golden hour rim + mid-stride |
| C. 직사 플래시 CCD | 1990s CCD + direct flash + fluorescent overhead + 의도된 결점(red eye, oily) |
| D. 골든아워 풀바디 | Leica M11 35mm + raking sun 12° + brick bounce + 9-head full leg |
| E. 야간 네온 | Sony A7S III + ISO 6400 organic noise + mixed practical (pink/cyan/tungsten) |
| F. 광고 + 한글 텍스트 | 3-ref labeled + 8축 lock + 한글 verbatim + pixel-locked label |

## 4. 일관성 5단계 (Identity Preservation)

1. 5-튜플 DNA prefix (2-3 디테일, 매 컷 첫 줄)
2. EXACT 자연어 강제 (매 컷 본문, verbatim)
3. Reference 역할 라벨링 (Image 1: identity / Image 2: outfit / Image 3: scene)
4. Reset 트리거 (3-5컷마다 anchor 재첨부)
5. Master Identity Sheet 23 캐논 (8-view + 9-expression + 6-outfit)

## 5. AI Tell-tale 7대 zoom-100% 체크리스트

제출 전 다음 7곳 점검 — 1곳 깨지면 fake-looking 판별:

1. 손가락 5개 / 손톱 자연 비대칭
2. 양쪽 귀 대칭 / 귀걸이 일치
3. 양쪽 동공 catchlight 위치 일치
4. 의류 패턴 연속성 / 솔기·로고
5. 머리카락 strand 가닥 (plastic 덩어리 금지)
6. 안경 렌즈 굴절 / 프레임 대칭
7. 배경 텍스트 (가독 OR out-of-focus, 중간 깨짐 금지)

## 6. 즉시 적용 — Imperfection 5요소 verbatim

```
photoreal skin texture with visible pores and natural asymmetry, 
one or two faint blemishes, slight under-eye warmth, 
sebum highlight on T-zone, loose flyaway hair strands, 
no airbrushing, no plastic skin, no over-smoothing, 
no symmetrical perfection, no glamour gloss.
```

이 블록을 매 프롬프트에 verbatim 박으면 plastic-skin drift가 가장 효과적으로 차단된다.

## 7. 광고 컷 — 한글 텍스트 + 인물 photoreal 충돌 회피

```
Two-region attention split:
- Subject region: photoreal priority (visible pores, EXACT face from Image 1)
- Text region: pixel-locked priority (EXACT Korean "[VERBATIM]" from Image 2, no extra characters)
Spatial separation: text and face on different planes with distinct focus.
```

## 8. 깊이 더 — 4개 도메인 상세

- [09-A · GPT Image 2 기술 마스터리]($HOME/Agents/Image-gen/research/09-photoreal-research-A-gpt-image-tech.md) — API 정밀 사양, 50+ 검증 토큰, 디버깅
- [09-B · 커뮤니티 프롬프트 라이브러리]($HOME/Agents/Image-gen/research/09-photoreal-research-B-community-prompts.md) — X 16 + Threads 5 + Reddit 5 + 10대 카테고리 45+ verbatim 프롬프트
- [09-C · 사진/촬영 학술 → 프롬프트 사전]($HOME/Agents/Image-gen/research/09-photoreal-research-C-photography-methodology.md) — ASC Manual + Hunter + Storaro + Ekman FACS + Munsell + LogC, 220 토큰
- [09-D · Identity Preservation + Compositing]($HOME/Agents/Image-gen/research/09-photoreal-research-D-identity-preservation.md) — IP-Adapter·InstantID·PhotoMaker·PuLID 학술 + drift 곡선 + multi-ref 8축

## 9. 호출 흐름 — 본 스킬에서

1. **SKILL.md §1.1 페르소나 수집** → DNA 잠금
2. **본 photoreal-mastery.md §1 원칙** 적용 (특히 imperfection 5요소)
3. **SKILL.md §3 템플릿** 또는 본 §3 6 마스터 템플릿 중 매칭
4. **본 §5 7대 체크리스트** 통과 후 출력
5. **시리즈 운영이면**: [09 마스터 §10]($HOME/Agents/Image-gen/research/09-ducktape-photoreal-mastery.md) Step 1-5 워크플로
