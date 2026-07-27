# ima2 CLI × Photoreal — 즉시 실행 명령어 (요약)

> 전체 레시피: [$HOME/Agents/Image-gen/research/09-ducktape-photoreal-cli-recipes.md]($HOME/Agents/Image-gen/research/09-ducktape-photoreal-cli-recipes.md)
>
> 본 요약은 사용자가 "ima2로", "CLI로", "터미널로 photoreal" 요청 시 빠르게 호출.

## 환경 (확정)

- CLI: `/opt/homebrew/bin/ima2` v1.1.11
- 서버: `http://127.0.0.1:3333` (launchd `io.ima2.server` 자동 실행)
- 기본 모델: `gpt-5.5` · reasoning `high`
- 출력: `~/.ima2/generated`
- OAuth (API key 불필요)

## Photoreal 권장 옵션 매 호출

```
-q high -s 1024x1536 --mode direct --no-web-search
```

`--reasoning-effort high`는 서버 default이므로 생략 가능. 시리즈 운영 시 일관성을 위해 명시 권장.

## 단일 씬 (1-ref)

```bash
HOME=$HOME ima2 gen "$(cat <PROMPT_FILE>)" \
  --ref <ABS_PATH_TO_IDENTITY_ANCHOR.png> \
  -q high -s 1024x1536 --mode direct --no-web-search \
  -o <ABS_PATH_OUT.png>
```

## 광고 컷 (3-ref, identity + product + scene)

```bash
HOME=$HOME ima2 gen "$(cat <PROMPT_FILE>)" \
  --ref <ANCHOR.png> \
  --ref <PRODUCT_WITH_KOREAN_TEXT.png> \
  --ref <SCENE_REF.jpg> \
  -q high -s 1024x1536 --mode direct --no-web-search \
  -n 4 -d <OUT_DIR>
```

프롬프트 본문에 `Image 1: identity / Image 2: product (pixel-locked Korean verbatim) / Image 3: scene` 역할 라벨링 필수.

## 8-view 시트 (multimode)

```bash
HOME=$HOME ima2 multimode "$(cat <PROMPT_FILE>)" \
  --ref <ANCHOR.png> \
  --max-images 8 \
  -q high -s 1024x1024 --mode direct --no-web-search \
  -d <CANON_DIR> --show-partial
```

## 9-expression 시트 (5+4 분할)

```bash
# 1차: neutral / soft smile / laugh / wink / pout
HOME=$HOME ima2 multimode "$(cat expr-1.txt)" --ref <ANCHOR> --max-images 5 -q high -s 1024x1024 --mode direct --no-web-search -d <DIR/expr-1>
# 2차: surprised / focused / shy / smirk
HOME=$HOME ima2 multimode "$(cat expr-2.txt)" --ref <ANCHOR> --max-images 4 -q high -s 1024x1024 --mode direct --no-web-search -d <DIR/expr-2>
```

## 6-outfit 풀바디

```bash
HOME=$HOME ima2 multimode "$(cat outfits.txt)" \
  --ref <ANCHOR> --ref <8VIEW_FRONT> \
  --max-images 6 -q high -s 1024x1536 --mode direct --no-web-search \
  -d <DIR/outfits>
```

## Edit (씬만 교체, 인물 보존)

```bash
HOME=$HOME ima2 edit <FILE.png> \
  --prompt "Keep the exact same person, face, hair, outfit. Change ONLY: <SCENE/BG/PROP>. Preserve all imperfection (pores, sebum, flyaway hair). No identity change." \
  -q high --mode direct \
  -o <OUT.png>
```

`edit`은 face drift 위험이 `gen --ref`보다 크다. 얼굴이 변하면 즉시 `gen --ref` 전환.

## 검증·관리

```bash
HOME=$HOME ima2 ping                 # health
HOME=$HOME ima2 defaults --json      # gpt-5.5 / high 확인
HOME=$HOME ima2 ps                   # 활성 작업
HOME=$HOME ima2 ls -n 10             # 최근 10개
HOME=$HOME ima2 metadata <FILE.png>  # 프롬프트·모델 메타
HOME=$HOME ima2 cancel <REQ_ID>      # 멈춘 작업 취소
HOME=$HOME ima2 inflight rm <REQ_ID> # 강제 제거
```

서버 무응답 시:
```bash
launchctl kickstart -k gui/$(id -u)/io.ima2.server
sleep 3 && HOME=$HOME ima2 ping
```

## 5-슬롯 프롬프트 작성 → ima2 입력

1. [SKILL.md §3 6대 템플릿](../SKILL.md) 또는 [09 마스터 §3]($HOME/Agents/Image-gen/research/09-ducktape-photoreal-mastery.md)에서 베이스 선택
2. [photoreal-mastery.md §6 Imperfection 5요소](photoreal-mastery.md) verbatim 박기
3. 5-튜플 DNA prefix (디테일 2-3개) + EXACT face 자연어 강제
4. `prompts/<scene-name>.txt`로 저장
5. `$(cat <file>)` 방식으로 ima2 호출

## 자연어 → 명령 매핑 (Hermes/Claude 에이전트 호출 시)

| 사용자 의도 | 호출 |
|---|---|
| "베이스 컷 4장" | `gen ... -n 4 -d canon/baseline` |
| "[장소]에서 자연스러운 1장" | `gen --ref anchor.png ... -o scenes/...` |
| "광고 컷 [제품]" | `gen --ref anchor --ref product --ref scene ... -n 4 -d ads/` |
| "8-view 시트" | `multimode --ref anchor --max-images 8 -d canon/8view` |
| "배경만 [X]로 교체" | `edit <file> --prompt "Keep exact person..."` |
| "최근 결과 보여줘" | `ls -n 10` |
| "활성 작업?" | `ps` |

## 핵심 룰

1. 매 호출에 `--ref <anchor>` 필수 (identity drift 차단)
2. `-q high` + `--mode direct` 필수 (마이크로 디테일 보존)
3. `-s 1024x1536` 세로 / `1536x1024` 가로 (인물 비례)
4. 5장 ref 한계 — 4ref 이상이면 `multimode` 검토
5. 3-5컷마다 anchor 교체 (drift reset)
6. 컷 ArcFace cosine ≥ 0.5 통과 후 다음 진행 ([09-D §6.1]($HOME/Agents/Image-gen/research/09-photoreal-research-D-identity-preservation.md))
