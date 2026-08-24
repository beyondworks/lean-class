---
name: palmier
description: Palmier Pro(macOS AI 네이티브 영상편집기)를 로컬 MCP 서버로 직접 조작해 컷 편집·전사 기반 편집·컬러·내보내기를 수행한다. 말더듬/필러 제거, 무음·늘어짐 압축, 파형 기반 자동 컷, 리타이밍, MP4/ProRes/FCPXML 내보내기. 트리거 — "팔미에", "Palmier", "컷 편집해줘", "말 더듬는 부분 잘라줘", "무음 제거", "영상 늘어지는 부분 조여줘", "웨비나 편집", "롱폼 타이트하게", "자막 붙여줘(타임라인)", "Resolve로 넘길 XML", "영상 1.05배속".
---

# Palmier Pro 편집 조작

## 0. 무엇을 해주나

Palmier Pro의 로컬 MCP 서버(툴 48개)를 셸에서 직접 호출해, 사람이 타임라인을 클릭하지 않고 컷 편집을 끝낸다. 특히 **롱폼(웨비나·강연·인터뷰)에서 무음·늘어짐·말더듬을 걷어내 20~30% 단축**하는 작업에 최적화돼 있다.

**핵심 신념: 전사 인덱스를 믿지 말고 프레임을 믿어라.** 이 도구의 인덱스 기반 편집(`remove_words`)은 실측에서 엉뚱한 단어를 잘랐다. 프레임 좌표로 내리는 `ripple_delete_ranges`만 결정적으로 동작한다.

## 1. 사전 조건 (없으면 아무것도 안 된다)

- macOS 26 Tahoe 이상 + Apple Silicon (그 외 환경은 앱 자체가 안 깔린다)
- `/Applications/PalmierPro.app` 설치 및 **실행 중**
- MCP 서버는 앱이 떠 있을 때만 `http://127.0.0.1:19789/mcp`에 LISTEN

확인:
```bash
pgrep -x PalmierPro >/dev/null && lsof -nP -iTCP:19789 | grep -q LISTEN && echo ready || open -a /Applications/PalmierPro.app
```

**프로젝트가 하나도 안 열려 있으면 모든 편집 툴이 `Editor not available`을 뱉는다.** `manage_project`로 열거나 만드는 게 첫 단계다.

## 2. 접속 — CLI 래퍼

`claude mcp add`는 재시작이 필요하므로 세션 중에는 쓰지 않는다. 대신 `scripts/pp`로 JSON-RPC를 직접 친다(서버는 요청마다 핸드셰이크를 새로 받는 stateless 구조라 이게 성립한다).

```bash
pp tools                    # 툴 이름 48개
pp spec <tool>              # 특정 툴 전체 스키마 + 설명
pp <tool> '<args json>'     # 호출
```

## 3. 표준 컷 편집 파이프라인

롱폼 하나를 받아 타이트하게 만드는 검증된 순서다.

```
① 프로젝트 생성 → ② 소재 임포트 → ③ 타임라인 배치
→ ④ 원본 전사(inspect_media) → ⑤ 파형 갭 추출(ffmpeg)
→ ⑥ 컷 구간 계산(scripts/cutplan.py) → ⑦ ripple_delete_ranges 1회
→ ⑧ 재전사 검증 → ⑨ export → ⑩ 리타이밍(선택)
```

```bash
pp manage_project '{"action":"create","name":"프로젝트명","fps":30,"aspectRatio":"16:9","quality":"1080p"}'
pp import_media '{"source":{"path":"/절대/경로.mp4"},"name":"원본"}'   # path는 복사 안 하고 참조
pp add_clips '{"entries":[{"mediaRef":"<mediaRef>","startFrame":0}]}'
pp inspect_media '{"mediaRef":"<mediaRef>","wordTimestamps":true,"language":"ko"}' > src.json
```

`import_media`의 `source`는 **객체**다(`{"path": ...}`). 문자열로 주면 `Missing required 'source' object`.

## 4. 컷 구간 계산 — 이 스킬의 핵심

`scripts/cutplan.py`가 두 소스를 합쳐 삭제할 프레임 구간을 만든다.

- **무음/늘어짐**: ffmpeg `silencedetect`로 뽑은 갭에서, 길이별로 남길 호흡을 차등해 나머지를 삭제
- **말더듬**: 원본 전사의 즉시 반복 단어쌍에서 앞 단어의 `[start, next.start]`를 통째로 삭제

검증된 기본값(한국어 강연 기준):

| 갭 길이 | 남길 호흡 |
|---|---|
| 0.18–0.30s | 0.14s |
| 0.30–0.50s | 0.16s |
| 0.50–0.80s | 0.19s |
| 0.80–1.50s | 0.26s |
| 1.50–3.00s | 0.36s |
| 3.00s+ | 0.50s |

`silencedetect` 파라미터는 **`-35dB` / `d=0.18` 고정**. 이유는 §6에.

```bash
ffmpeg -i src.wav -af "silencedetect=n=-35dB:d=0.18" -f null - 2>&1 \
  | grep -E "silence_start|silence_end" > gaps.raw
python3 scripts/cutplan.py gaps.raw src.json cuts.json
pp ripple_delete_ranges "$(python3 -c "import json;print(json.dumps({'trackIndex':1,'units':'frames','ranges':json.load(open('cuts.json'))}))")"
```

**모든 구간을 한 호출에 넘긴다.** 툴이 내부에서 병합·좌우 시프트를 처리하므로 1,300개를 한꺼번에 줘도 정확하다(실측 확인). 나눠 부르면 좌표가 밀린다.

## 5. 검증 — 안 하면 완료가 아니다

컷 후 반드시 재전사해서 발화가 살아 있는지 대조한다. 길이만 보고 끝내면 문장이 깨진 걸 놓친다.

```bash
pp get_transcript '{"language":"ko"}' > after.json
```

대조 항목:
- **발화 보존**: 컷 지점 앞뒤 어구가 그대로 있는가 (원본 전사에서 뽑은 문구로 `in` 검사)
- **말더듬 잔여**: 즉시 반복이 몇 건 남았는가
- **발화 밀도**: 분당 단어수 (한국어 강연 정상 범위 100~110)

## 6. 실측으로 확인한 함정 (전부 이 도구를 쓰다 당한 것)

### `remove_words`는 쓰지 마라
인덱스 기반 단어 삭제인데, **한 호출에 여러 인덱스를 주면 제거될 때마다 인덱스가 밀려 엉뚱한 단어가 잘린다.** 12개를 지정했더니 3개 앞 단어들('추가해주고', '자동으로', '노드')이 날아갔다. 한 건씩 잘라도 마찬가지였다 — 루프 20회에서 같은 지점을 6~7번 반복해서 자르며 정상 단어 24개를 파먹고 정작 반복은 남았다. 공식 설명에는 "실행 후 인덱스가 밀린다"만 있고 호출 내부에서 밀린다는 말은 없다.

**대안**: 원본 전사(`inspect_media`)의 단어 `[text, start, end]`에서 프레임을 계산해 `ripple_delete_ranges`로 삭제. 20건 중 19건이 한 번에 처리됐다.

### `remove_silence`는 "늘어짐"을 못 잡는다
무음만 자른다. 말이 느리게 이어지는 구간은 speech로 판정돼 그대로 남는다. 0.7초 → 0.35초로 두 번 돌려도 문제 구간이 **7.20초에서 미동도 안 했다.** 늘어짐은 파형 기반으로 직접 잘라야 한다.

또 임포트 직후 호출하면 `No dead air`가 나온다 — 온디바이스 speech 분석이 백그라운드로 도는 중이다. 1~2분 기다렸다 재시도.

### `silencedetect` 임계는 −35dB를 넘기지 마라
−30dB로 올리면 **약한 발음(어미·자음)까지 무음으로 오판**해 단어가 통째로 사라진다. 실측에서 "디자이너로 커리어를 **시작했는데** 사업도"의 '시작했는데'가 날아갔다. −30dB는 이 소재의 평균 레벨(−20.7dB)에 너무 가깝다.

`d`도 0.15까지 내리면 **단어 내부의 파열음 폐쇄 구간**을 갭으로 잡는다. 0.18 이상 유지.

### STT 단어 경계를 보호 구간으로 쓰지 마라
이 전사 엔진은 단어 끝을 다음 단어 시작에 붙여놔서(단어 간 갭이 5,829개 중 292개뿐) **침묵이 단어에 포함된다.** 단어 구간을 보호막으로 씌우면 자를 게 거의 없어진다 — 실측에서 47분 목표가 59분으로 후퇴했다.

### `speed`를 다중 클립에 걸지 마라
`set_clip_properties`의 speed는 클립 길이를 재조정할 뿐 **ripple이 아니다.** 컷이 많은 타임라인(클립 1,000개+)에 걸면 클립마다 짧아지며 사이에 갭이 생긴다. 배속은 **렌더 후 ffmpeg에서** 건다(§7).

### ffmpeg 필터 로그는 `-v error`로 죽는다
`silencedetect`, `volumedetect`, `astats`는 전부 **info 레벨**로 출력한다. `-v error`를 붙이면 결과가 안 보이고 "0건"으로 오독하게 된다. 로그 레벨을 낮추지 말 것.

### 한국어 강조 반복을 자르지 마라
"하나씩 하나씩", "빨리 빨리", "점점 점점"은 말더듬이 아니라 강조다. 자르면 오히려 어색해진다. 문장 경계의 동어 반복("…관리하고 매출. 매출 월별…")도 자르면 문장이 깨진다. `cutplan.py`의 `KEEP` 세트로 제외하고, 애매하면 앞뒤 8단어 문맥을 출력해 사람이 판단한다.

## 7. 내보내기와 리타이밍

```bash
pp export_project '{"mode":"video","codec":"H.264","resolution":"1080p","outputPath":"/절대/경로.mp4"}'
pp manage_exports '{"action":"list"}'      # progress 폴링
```

모드: `video`(H.264/H.265/ProRes) · `xml`(Premiere) · `fcpxml`(Resolve/FCP) · `palmier`(패키지).
트랜지션·마스킹·그래픽은 이 앱에 **아직 없다**(공식 FAQ). 필요하면 `fcpxml`로 넘겨 Resolve에서 마감한다.

배속은 렌더 후:
```bash
ffmpeg -i in.mp4 -filter_complex "[0:v]setpts=PTS/1.05[v];[0:a]atempo=1.05[a]" \
  -map "[v]" -map "[a]" -c:v h264_videotoolbox -b:v 6M -c:a aac -b:a 192k \
  -movflags +faststart out.mp4
```
`atempo`는 피치를 유지한다. 검증법 — 같은 발화 구간의 영점교차율을 비교해 배속 비율만큼 안 올라가면 보존된 것이다(실측: 1.05x에서 0.0428 → 0.0440, +2.7%로 리샘플이 아님).

VideoToolbox는 50분 1080p를 4분에 처리한다. 다만 고정 비트레이트라 **원본보다 파일이 커질 수 있다**(1.9Mbps 원본 → 6Mbps로 3배). 용량이 중요하면 3M으로 낮춘다.

## 7-1. 자막 — 한 줄씩 끊는다 ({{OWNER_TITLE}} 고정 요구)

**한 캡션이 화면에서 두 줄로 감기면 안 된다.** 이건 취향이 아니라 확정된 요구사항이다.

```bash
pp add_captions '{"language":"ko","maxWords":4,"maximumGapSeconds":0.25}'
```

`maxWords`가 캡션당 단어 수를 자른다. 다만 **단어 수만으로는 한 줄을 보장하지 못한다** — 한국어는
단어 길이 편차가 크다. 실측(웨비나 5,249단어): 글자수 평균 2.9 · 중앙값 3 · 90분위 5 · 최대 9자.

| 한 줄 목표 | maxWords | 평균 길이 | 긴 단어가 몰릴 때 |
|---|---|---|---|
| 14자 | 3 | 11자 | 17자 |
| 16~18자 | **4** | 15자 | 23자 |
| 20자 | 5 | 19자 | 29자 |

**기본값은 `maxWords: 4`**(1080p 하단 자막에서 한 줄로 떨어지는 대역). 자막 폰트를 키웠거나 세로
영상이면 3으로 내린다.

생성 후 **반드시 실제 캡션 텍스트 길이를 검증한다.** 표에서 보듯 긴 단어가 몰리면 목표치를 넘긴다.

```bash
pp get_timeline '{"captionDetail":true}' > /tmp/cap.json
python3 -c "
import json; d=json.load(open('/tmp/cap.json'))
bad=[]
for t in d.get('tracks',[]):
    for c in t.get('clips',[]):
        s=(c.get('content') or c.get('text') or '').strip()
        if len(s) > 18: bad.append((len(s), s))
print(f'초과 {len(bad)}건'); [print(' ', n, repr(s)) for n,s in sorted(bad, reverse=True)[:15]]"
```

초과분이 있으면 `maxWords`를 1 낮춰 다시 생성하거나, 해당 그룹만 `update_text`로 손본다.
스타일은 **요청받지 않았으면 건드리지 않는다** — `style`·`animation`·`transform`을 다 생략하면
앱 기본(흰 Helvetica, 하단 3분할)이 나온다. 폰트·색·외곽선을 임의로 지어내지 말 것.

자막은 **컷 편집이 완전히 끝난 뒤**에 붙인다. `add_captions`는 타임라인의 현재 음성을 전사하므로,
자막을 먼저 붙이면 이후 컷마다 캡션이 어긋난다.

## 8. 실측 성과 기준

한국어 웨비나 66분 53초 기준:

| 처리 | 결과 |
|---|---|
| 파형 갭 압축(1,291구간) + 말더듬 19건 | 50분 50초 (−24.0%) |
| + 1.05x 리타이밍 | 48분 25초 (−27.6%) |
| 말더듬 잔여 | 20건 → 2건 |
| 발화 보존 검증 | 10/10 |

무음이 전체의 34.6%(1,389초)였다. 롱폼은 대체로 이 대역이니, **−25% 안팎이 안전하게 나오는 목표치**다. 그 이상 쪼이려는 시도는 §6의 함정으로 되돌아온다.

## 9. 삭제 금지

`undo` 툴이 있지만 되돌리는 단위가 액션 1개다. 대량 편집을 되돌릴 땐 **새 타임라인을 만들어 원본부터 다시 쌓는 편이 확실하다**(계산이 결정적이라 재현된다). 사용자의 기존 타임라인·프로젝트·파일은 지우지 않는다 — 정리는 사용자가 앱에서 한다.
