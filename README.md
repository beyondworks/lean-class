# Claude AI Kit — AI 작업 환경 패키지

Claude Code에서 실제로 쓰는 **작업 환경 한 벌**을 새 PC에 그대로 세우는 패키지입니다.
스킬·플러그인·MCP뿐 아니라 **일하는 방식(글로벌 규칙·하네스)**까지 담았습니다.

**사람 이름이 하나도 들어 있지 않습니다.** 설치할 때 이 PC의 오너가 직접 정합니다.

---

## 설치

### 가장 쉬운 방법 — Claude Code에게 맡기기

> `https://github.com/beyondworks/lean-class.git 이 저장소 설치해줘`

clone부터 설치까지 알아서 합니다. (지시는 `AGENTS.md`에 있습니다)

### 직접 실행

```bash
git clone https://github.com/beyondworks/lean-class.git
bash lean-class/install.sh
```

설치기가 이름·호칭·경로를 물어봅니다. **엔터만 쳐도 됩니다** — 기본값이 들어가고 나중에 바꿀 수 있습니다.

```bash
bash install.sh --defaults              # 전부 기본값, 안 물어봄
bash install.sh --answers owner.conf    # 파일에서 읽음 (owner.example.conf 참고)
```

설치가 끝나면 **Claude Code 재시작** + **새 터미널**을 여세요.

---

## 무엇이 설치되나

| 단계 | 내용 |
|---|---|
| 1 | **스킬** → `~/.claude/skills/` |
| 2 | **커맨드·에이전트** → `~/.claude/commands/`, `agents/` |
| 3 | **글로벌 규칙** → `~/.claude/CLAUDE.md` + `rules/` (오너 정보로 치환) |
| 4 | **플러그인** 27개 일괄 설치 |
| 5 | **MCP** — 키 불필요한 것 자동 등록, 키 필요한 것은 안내 |
| 6 | **하네스(fablize)** — 원본 레포에서 받아와 운영 블록 주입 |
| 7 | **셸** — `cc` alias + PATH (프로파일에 source 한 줄) |

기존 파일은 **덮어쓰지 않고** `.bak-<타임스탬프>`로 백업합니다. `rm -rf` 없음.

### 3번과 6번이 이 패키지의 핵심입니다

스킬·플러그인은 "무엇을 할 수 있나"를 늘립니다. **규칙과 하네스는 "어떻게 일하나"를 바꿉니다.**

- **글로벌 규칙** — 시크릿 평문 금지, 기획=구현 정합성, 추측 금지, 검증 없는 완료 선언 금지, 교정받으면 lessons에 축적
- **하네스(fablize)** — 계획 나열 없이 착수 → 한 번에 완성 → 한 번 검증 → 짧은 노트로 보고

둘 다 안 깔아도 나머지는 동작합니다. 다만 체감 차이는 여기서 가장 큽니다.

---

## 구성

| 카테고리 | 개수 | 폴더 |
|---|---:|---|
| MCP 서버 | 14 | `00-mcp/` |
| 플러그인 | 27 | `01-plugins/` |
| 스킬 | 123 | `02-skills/` |
| 슬래시 커맨드 | 32 | `03-commands/` |
| 에이전트 | 24 | `04-agents/` |
| 글로벌 규칙 | 12 (+선택 1) | `06-rules/` |
| 하네스 | 1 | `07-fablize/` |
| 셸 설정 | — | `08-shell/` |

```
lean-class/
├── install.sh              ← 원샷 설치
├── owner.example.conf      ← 비대화형 설치용 답변 템플릿
├── 00-mcp/ … 08-shell/     ← 카테고리별 자산
└── scripts/
    ├── scan-personal.sh    ← 개인정보·시크릿 게이트
    ├── build-rules.sh      ← 규칙 재생성 (원 소유자용)
    └── build-skills.sh     ← 스킬·커맨드 재생성 (원 소유자용)
```

전체 목록은 [`PACKAGE_MANIFEST.md`](PACKAGE_MANIFEST.md)에 있습니다.

---

## 설치 후

- **MCP 키** — hyperbrowser·magic·testsprite·notion은 본인 키가 필요합니다 → `00-mcp/README.md`
- **호칭·에이전트 이름 변경** — `~/.claude/CLAUDE.md`를 직접 고치면 됩니다
- **`cc` alias 경고** — `claude --dangerously-skip-permissions`의 별칭입니다. 파일 쓰기·셸 실행 전에 묻지 않습니다. **신뢰하는 저장소에서만** 쓰고, 남의 코드에서는 그냥 `claude`를 쓰세요. 부담스러우면 `~/.claude/lean-class.sh`에서 그 줄을 지우면 됩니다.

## 안전·범위

- **시크릿 0** — API 키·토큰·DB 접속정보가 없습니다. MCP 키 자리는 전부 `<YOUR_...>`입니다.
- **개인정보 0** — 이름·이메일·개인 절대경로가 없습니다. `scripts/scan-personal.sh`가 커밋 전 게이트로 검사하며, 통과해야 배포합니다.
- **노하우 제외** — 원 소유자가 세션에서 축적한 `references/` 폴더는 전부 제거했습니다. 이 킷은 도구 셋이지 노하우 모음이 아닙니다.
- **로컬 의존 주의** — 일부 MCP·스킬은 별도 앱이나 자체 서버가 떠 있어야 동작합니다. 각 README의 "로컬 의존" 표기를 확인하세요.
- **fablize는 재배포하지 않습니다** — 제3자 저작물이라 설치 시 원본 레포에서 직접 받아옵니다.
