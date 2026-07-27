#!/usr/bin/env bash
# ==============================================================
#  06-rules 빌드 — 로컬 글로벌 규칙을 배포용 템플릿으로 변환
#
#  사용법:  bash scripts/build-rules.sh
#
#  하는 일:
#    ~/.claude/CLAUDE.md + ~/.claude/rules/*.md 를 읽어
#    개인 고유명(이름·경로·조직·에이전트명)을 placeholder 로 치환한 뒤
#    06-rules/ 에 쓴다.
#
#  왜 스크립트인가: 로컬 규칙은 계속 바뀐다. 손으로 옮기면 다음 갱신 때
#  또 손으로 해야 하고, 치환 누락이 생긴다. 빌드로 고정한다.
#
#  제외 규칙(개인 전용): EXCLUDE 배열 참고
# ==============================================================
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_MD="${HOME}/.claude/CLAUDE.md"
SRC_RULES="${HOME}/.claude/rules"
OUT="${ROOT}/06-rules"

# 개인 전용이라 배포하지 않는 규칙
EXCLUDE=(leanax-erp.md model-ab-test.md)

# 특정 유료·개인 도구가 있어야만 성립하는 규칙 → rules/optional/ 로 분리.
# 기본 설치에서 빠지므로, 없는 도구를 쓰라고 강제하는 사고를 막는다.

[ -f "$SRC_MD" ] || { echo "원본 없음: $SRC_MD"; exit 2; }

mkdir -p "$OUT/rules"

python3 - "$SRC_MD" "$SRC_RULES" "$OUT" "${EXCLUDE[@]}" <<'PY'
import os, re, sys

src_md, src_rules, out = sys.argv[1], sys.argv[2], sys.argv[3]
exclude = set(sys.argv[4:])

# --- 치환 표: 긴 것부터 먼저 (부분매칭 사고 방지) ---
SUBS = [
    # 경로 (긴 절대경로 → 짧은 것 순서)
    (r'/Users/[a-z0-9_.-]+/Documents/AI-Sessions-Vault', '{{VAULT_ROOT}}'),
    (r'~/Documents/AI-Sessions-Vault',                   '{{VAULT_ROOT}}'),
    (r'AI-Sessions-Vault',                               '{{VAULT_ROOT}}'),
    (r'/Users/[a-z0-9_.-]+/lean-projects',               '{{PROJECTS_ROOT}}'),
    (r'~/lean-projects',                                 '{{PROJECTS_ROOT}}'),
    (r'/Users/[a-z0-9_.-]+/Code',                        '{{CODE_ROOT}}'),
    (r'/Users/[a-z0-9_.-]+/leanAX[^\s`)]*',              '{{PROJECTS_ROOT}}/erp'),
    (r'/Users/[a-z0-9_.-]+',                             '$HOME'),

    # 인물 — 호칭형을 먼저 잡아야 "유건님"이 "{{OWNER_NAME}}님"이 되지 않는다
    (r'유건님',   '{{OWNER_TITLE}}'),
    (r'유건',     '{{OWNER_NAME}}'),
    (r'김효율',   '{{OWNER_NAME}}'),
    (r'효율님',   '{{OWNER_TITLE}}'),
    (r'시원',     '{{MODERATOR}}'),

    # 에이전트 이름 (직무 페르소나)
    (r'페퍼',   '{{AGENT_MODERATOR}}'),
    (r'슈리',   '{{AGENT_DEV}}'),
    (r'카맥',   '{{AGENT_CORE}}'),
    (r'에드나', '{{AGENT_DESIGN}}'),
    (r'비스트', '{{AGENT_MARKETING}}'),
    (r'월터',   '{{AGENT_CONTENT}}'),
    (r'요다',   '{{AGENT_EDU}}'),
    (r'울프',   '{{AGENT_SALES}}'),
    (r'다빈치', '{{AGENT_PLANNING}}'),
    (r'파인만', '{{AGENT_RESEARCH}}'),

    # 조직·계정
    (r'beyondworks\.br@gmail\.com', '{{OWNER_EMAIL}}'),
    (r'beyondworks',                '{{GITHUB_ORG}}'),
    (r'leankim',                    '{{OWNER_HANDLE}}'),
]

def scrub(text):
    for pat, rep in SUBS:
        text = re.sub(pat, rep, text)
    # 개인 히스토리(날짜 + 지시자) 제거 — 다른 오너에겐 사실이 아닌 문장이 된다
    text = re.sub(r'\(전역 — 20\d\d-\d\d-\d\d \{\{OWNER_[A-Z]+\}\} 지시\)', '(전역)', text)
    text = re.sub(r'^> 20\d\d-\d\d-\d\d \{\{OWNER_[A-Z]+\}\} 지시\.\s*', '> ', text, flags=re.M)
    text = re.sub(r'\s*\(\{\{OWNER_[A-Z]+\}\} (지시|요청|결정)( 20\d\d-\d\d-\d\d)?\)', '', text)
    text = re.sub(r'상시 — 20\d\d-\d\d-\d\d \{\{OWNER_[A-Z]+\}\} 지시', '상시', text)
    return text

# --- 파일별 후처리: 단순 치환으로 안 되는 구조적 개인정보 ---

GENERIC_REPO_SECTION = '''## 레포 경계 (여러 레포를 병행할 때 — 푸시 격리)

커밋·푸시 전 `git -C <repo> remote -v`로 목적지를 직접 확인한다. 내용이 레포를 넘으면 안 된다.

| 레포 | 담는 것 | 담지 않는 것 |
|---|---|---|
| _(앱 레포)_ | 그 앱 코드·빌드·패키징만 | 다른 앱 코드, 문서 볼트 |
| _(엔진·라이브러리 레포)_ | 공용 엔진만 | 그 엔진을 쓰는 앱 코드 |
| _(문서·지식 레포)_ | 문서·맥락·핸드오버만 | 코드 |

> **오너가 채울 곳**: 위 표에 본인 레포 이름·remote·로컬 경로를 적는다.
> 비워두면 이 규칙은 동작하지 않는다 — 레포가 하나뿐이면 이 절은 지워도 된다.

- 한 레포 내용을 다른 레포에 푸시 **금지** (코드→문서 레포, 앱A→앱B 교차 금지).
- `git add .` / `git add -A` **금지** — 항상 자기 파일만 명시적으로 add.
'''

# 도구 전제가 있는 규칙 → optional 로 빼고 배너를 붙인다
OPTIONAL = {
    'browser.md': (
        '> **선택 규칙 — 기본 비활성.** 이 규칙은 `aside` CLI(오너의 실제 로그인 크롬 세션을\n'
        '> 그대로 쓰는 브라우저 자동화 도구)가 설치된 환경에서만 성립한다. 미설치 상태로\n'
        '> 로드하면 존재하지 않는 도구를 쓰라고 강제하게 된다.\n'
        '>\n'
        '> **`aside`가 없다면**: 이 파일을 `~/.claude/rules/`로 옮기지 말고, 대신 Playwright MCP\n'
        '> 등 설치된 브라우저 도구를 쓴다. 도구 이름만 바꿔 같은 원칙(실제 렌더 관찰로 검증,\n'
        '> 요청받은 작업에만 사용)을 적용하면 된다.\n\n'
    ),
}

def postfix(fn, text):
    if fn == 'security.md':
        # 원본은 "이렇게 쓰지 말 것" 예시에 실제 키 조각을 그대로 박아뒀다.
        # 규칙 자체가 접두사 노출도 최소화하라고 하므로 예시를 완전 마스킹한다.
        text = re.sub(r'❌ DATABASE_URL=postgresql://\S*',
                      '❌ DATABASE_URL=postgresql://user:<실제_비밀번호>@<host>/<db>', text)
        text = re.sub(r'❌ re_[A-Za-z0-9_]{6,}', '❌ re_<실제_키_전체>', text)
        text = re.sub(r'❌ "예시로 \S+ 같은', '❌ "예시로 <실제_키> 같은', text)
        # 말미 사고 사례의 레포·서비스 실명 → 일반화
        text = re.sub(r'`\{\{GITHUB_ORG\}\}/[A-Za-z0-9._-]+`\s*레포의',
                      '어느 공개 레포의', text)
    if fn == 'git.md':
        text = re.sub(r'## 레포 경계.*?\Z', GENERIC_REPO_SECTION, text, flags=re.S)
    return text

# --- CLAUDE.md: FABLIZE 블록은 제거 (fablize setup.sh 가 자기 블록을 관리) ---
raw = open(src_md, encoding='utf-8').read()
raw = re.sub(r'<!-- FABLIZE:BEGIN.*?<!-- FABLIZE:END -->\n?', '', raw, flags=re.S)

# 개인 전용 섹션 제거: "## 모델 비교 테스트" 부터 다음 H2 직전까지
raw = re.sub(r'\n## 모델 비교 테스트.*?(?=\n## |\Z)', '\n', raw, flags=re.S)

# 개인 ERP 포인터 한 줄 제거
raw = '\n'.join(l for l in raw.split('\n') if 'leanax-erp' not in l)

open(os.path.join(out, 'CLAUDE.template.md'), 'w', encoding='utf-8').write(scrub(raw))
print('  CLAUDE.template.md')

# --- rules/*.md ---
kept = skipped = optional_n = 0
for fn in sorted(os.listdir(src_rules)):
    if not fn.endswith('.md'):
        continue
    if fn in exclude:
        print(f'  건너뜀(개인 전용): {fn}')
        skipped += 1
        continue
    body = postfix(fn, scrub(open(os.path.join(src_rules, fn), encoding='utf-8').read()))

    if fn in OPTIONAL:
        os.makedirs(os.path.join(out, 'rules', 'optional'), exist_ok=True)
        dest = os.path.join(out, 'rules', 'optional', fn)
        # 배너는 H1 바로 다음에 넣어 제목이 묻히지 않게 한다
        lines = body.split('\n')
        cut = 1 if lines and lines[0].startswith('# ') else 0
        body = '\n'.join(lines[:cut]) + '\n\n' + OPTIONAL[fn] + '\n'.join(lines[cut:])
        print(f'  선택 규칙으로 분리: {fn}')
        optional_n += 1
    else:
        dest = os.path.join(out, 'rules', fn)
        kept += 1
    open(dest, 'w', encoding='utf-8').write(body)

print(f'\n  기본 규칙 {kept}개 / 선택 규칙 {optional_n}개 / 제외 {skipped}개')
PY

echo
echo "빌드 완료 → $OUT"
echo "다음: bash scripts/scan-personal.sh 06-rules  (치환 누락 확인)"
