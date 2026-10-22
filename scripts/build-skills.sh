#!/usr/bin/env bash
# ==============================================================
#  02-skills / 03-commands 빌드 — 로컬 스킬·커맨드를 배포용으로 동기화
#
#  사용법:  bash scripts/build-skills.sh
#
#  중요 — 심볼릭 링크는 담지 않는다:
#    ~/.claude/skills 의 상당수는 ~/.codex/skills 를 가리키는 symlink 다
#    (oh-my-claudecode / codex 가 설치한 것). 복사하면 대상 PC 에서
#    전부 깨진 링크가 된다. 이건 OMC 를 설치하면 딸려오므로 제외한다.
#
#  또한 제거하는 것:
#    · references/  — 원 소유자가 세션에서 축적한 노하우 (배포 대상 아님)
#    · 개인 절대경로 → placeholder 치환
# ==============================================================
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_SKILLS="${HOME}/.claude/skills"
SRC_CMDS="${HOME}/.claude/commands"

# 특정 제품·개인 인프라 전용이라 배포하지 않음
EXCLUDE_SKILLS=(
  argo-release argo-resident-deploy argo-ship-gate   # 특정 데스크톱 앱 전용
  intranet-style                                     # 특정 사내 인트라넷 전용
  aside-browser                                      # 개인 유료 브라우저 도구 전용
  wiki-autolink                                      # 개인 노트 버스(_bus) 전용
  leankim-voice                                      # 오너 개인 화법 코퍼스 — 이름을 치환해도 내용이 정체성 그 자체
  argo-security-surface-audit                        # 특정 데스크톱 앱 전용 (argo-* 계열)
  course-script                                      # 오너 페르소나 빙의 규칙 + 본인 확정본 코퍼스 + 고객사 실명
  # 2026-10-22 맥 two 합치기에서 새로 판정
  argo-pg-drill argo-messenger-release argo-messenger-ios-store  # 특정 데스크톱 앱 전용 (argo-* 계열)
  aimee-ship-gate                                    # 특정 데스크톱 앱 전용
  leankim-mail                                       # 오너 개인 화법으로 쓰는 메일 — leankim-voice 와 같은 판정
  macgyver-fix mac-clean                             # 오너 조직·오너 맥 전용 운영 절차
  ego-browser                                        # 앱이 설치·관리하는 스킬(앱 설치 시 딸려옴)
  obsidian-save obsidian-reference                   # 오너 볼트 규약 전용 — 패키지에 있는 기존 판을 그대로 둔다
  synced                                             # claude.ai 계정에서 동기화되는 플러그인 사본
  # 공개 전 사람 눈 검수(2026-10-22)에서 막힘이 나와 이번 판에서 뺀 것 — 정리 뒤 다음 판에 넣는다
  detail-page-studio                                 # 실제 경쟁사 분석 기록·실전 상품 기록·개인 세션 파일(.omc)
  saas-motion-film                                   # 예제가 실제 자사 제품·회사명, 글꼴 라이선스 미동봉
  team-build team-save team-load                     # 오너 팀 구성·기기 규칙이 일반 규칙처럼 들어 있음
  no-ai-slop                                         # 출처·라이선스 확인 전
)

# 오너 개인 제외 목록은 exclude.local.txt(커밋 안 함)
EXCLUDE_LOCAL="${ROOT}/scripts/exclude.local.txt"
if [ -f "$EXCLUDE_LOCAL" ]; then
  while read -r -a names; do
    for n in "${names[@]}"; do
      [[ "$n" == \#* ]] && break
      EXCLUDE_SKILLS+=("$n")
    done
  done < "$EXCLUDE_LOCAL"
fi

# org-loop·볼트 등 개인 운영 인프라에 묶인 커맨드
EXCLUDE_CMDS=(
  board boot inbox delegate harvest start-loop skill-proposal
  loop-time looptime lt raw-press agent-add
  project-context-builder                            # 새 판에 오너 모델 선택 규칙이 들어감 — 기존 판 유지(2026-10-22)
)

# 스킬은 담되 그 안에서 뺄 파일 — 오너 개인 규칙·지적 기록이라 배포 대상이 아니다
EXCLUDE_FILES=(
  lean-polish/references/design-rulebook.md          # 오너 디자인 규칙집(규칙은 패키지에서 뺀다)
  lean-polish/references/cases.md                    # 오너가 실제로 지적한 사례 기록
)

# 담은 파일 안에서 고칠 문장 — 뺀 파일·스킬을 가리키거나 오너 환경에만 있는 내용(파일|정규식|바꿀 말, 한 줄에 하나)
PATCHES='
lean-polish/SKILL.md|규칙은 2026-10-20 \{\{OWNER_TITLE\}\}이 전자책 그림 작업에서 직접 지적한 것들을 모은 것이다\(사례는 `references/cases.md`\)\.|규칙은 실제 시각물 작업에서 반복해서 나온 지적을 모은 것이다.
lean-polish/SKILL.md|\n\*\*먼저 `references/design-rulebook.md`를 읽는다\.\*\*[^\n]*\n|\n
lean-polish/SKILL.md|\(lean-deck, detail-page-studio 등\)|(슬라이드·상세페이지 스킬 등)
lean-polish/SKILL.md|lean-deck·detail-page-studio·전자책 그림 작업|슬라이드·상세페이지·전자책 그림 작업
lean-polish/SKILL.md|\n\n\n|\n\n
lean-polish/SKILL.md|\n- `lean-deck`:[^\n]*|
lean-polish/SKILL.md|\n- `detail-page-studio`:[^\n]*|
lean-polish/references/svg-recipes.md|실제 생성기 전체는[^\n]*|아래 조각을 복사해 시작하면 된다.
'

# 링크라도 담는 원본 위치 — 오너가 직접 만든 스킬 원본을 모아 둔 곳(링크를 따라가 실제 파일을 복사)
OWNED_LINK_ROOT="${HOME}/Tools/skills"

python3 - "$ROOT" "$SRC_SKILLS" "$SRC_CMDS" \
  "$(IFS=,; echo "${EXCLUDE_SKILLS[*]}")" \
  "$(IFS=,; echo "${EXCLUDE_CMDS[*]}")" \
  "$(IFS=,; echo "${EXCLUDE_FILES[*]}")" "$OWNED_LINK_ROOT" "$PATCHES" <<'PY'
import os, re, shutil, sys

root, src_skills, src_cmds = sys.argv[1], sys.argv[2], sys.argv[3]
ex_skills = set(filter(None, sys.argv[4].split(',')))
ex_cmds   = set(filter(None, sys.argv[5].split(',')))
ex_files  = set(filter(None, sys.argv[6].split(',')))
owned_root = os.path.realpath(sys.argv[7])
patches = [l.split('|', 2) for l in sys.argv[8].strip().splitlines() if l.count('|') >= 2]

def apply_patches(skill_dir, name):
    for rel, pat, rep in patches:
        skill, _, sub = rel.partition('/')
        fp = os.path.join(skill_dir, sub)
        if skill != name or not os.path.isfile(fp):
            continue
        t = open(fp, encoding='utf-8').read()
        n = re.sub(pat, rep.replace('\\n', '\n'), t)
        if n == t:
            print(f'    ⚠ 고칠 문장을 못 찾음: {rel} — {pat[:40]}')
        else:
            open(fp, 'w', encoding='utf-8').write(n)

def owned_link(p):
    """오너 원본 폴더(~/Tools/skills)를 가리키는 링크는 담는다. 그 밖의 링크는 OMC·codex 제공분이라 뺀다."""
    target = os.path.realpath(p)
    return target == owned_root or target.startswith(owned_root + os.sep)

SUBS = [
    (r'/Users/[a-z0-9_.-]+/Documents/AI-Sessions-Vault', '{{VAULT_ROOT}}'),
    (r'~/Documents/AI-Sessions-Vault',                   '{{VAULT_ROOT}}'),
    (r'AI-Sessions-Vault',                               '{{VAULT_ROOT}}'),
    (r'/Users/[a-z0-9_.-]+/lean-projects',               '{{PROJECTS_ROOT}}'),
    (r'~/lean-projects',                                 '{{PROJECTS_ROOT}}'),
    (r'/Users/[a-z0-9_.-]+',                             '$HOME'),
    (r'유건님', '{{OWNER_TITLE}}'), (r'유건', '{{OWNER_NAME}}'),
    (r'김효율', '{{OWNER_NAME}}'), (r'효율님', '{{OWNER_TITLE}}'),
    (r'페퍼', '{{AGENT_MODERATOR}}'), (r'슈리', '{{AGENT_DEV}}'),
    (r'카맥', '{{AGENT_CORE}}'),     (r'에드나', '{{AGENT_DESIGN}}'),
    (r'비스트', '{{AGENT_MARKETING}}'), (r'월터', '{{AGENT_CONTENT}}'),
    (r'요다', '{{AGENT_EDU}}'),      (r'울프', '{{AGENT_SALES}}'),
    (r'파인만', '{{AGENT_RESEARCH}}'), (r'다빈치', '{{AGENT_PLANNING}}'),
    (r'오길비', '{{AGENT_CONTENT}}'), (r'맥가이버', '{{AGENT_CORE}}'),
    (r'효원', '{{AGENT_MODERATOR}}'), (r'보스웰', '{{AGENT_CONTENT}}'),
    # 공개 플랫폼 실명이라도 교육기관 실명 게이트에 걸리므로 일반 명사로
    (r'인프런·노마드코더·패스트캠퍼스', '국내 온라인 강의 플랫폼'),
    (r'beyondworks', '{{GITHUB_ORG}}'), (r'leankim', '{{OWNER_HANDLE}}'),
    # 사내 시스템 실명 → 일반 명사
    (r'LeanAX/control-room', '사내 운영 콘솔'),
    (r'LeanAX, company intranet, control-room', '사내 인트라넷·운영 콘솔'),
    (r'LeanAX', '사내 시스템'),
]
TEXT_EXT = {'.md', '.txt', '.sh', '.py', '.js', '.mjs', '.json', '.yaml', '.yml', '.toml'}

def scrub_file(path):
    if os.path.splitext(path)[1].lower() not in TEXT_EXT:
        return
    try:
        t = open(path, encoding='utf-8').read()
    except (UnicodeDecodeError, OSError):
        return
    o = t
    for pat, rep in SUBS:
        t = re.sub(pat, rep, t)
    # "실사용 후 오너 승인" 같은 원 소유자 워크플로 흔적 정리
    t = re.sub(r'\{\{OWNER_NAME\}\} 승인 후', '오너 승인 후', t)
    if t != o:
        open(path, 'w', encoding='utf-8').write(t)

# 세션 기록으로 판정하는 파일명 패턴 (원 소유자 노하우 → 배포 제외)
_REC = re.compile(
    r'(\d{4}-\d{2}-\d{2})'                       # 파일명에 날짜
    r'|(-|_)(log|status|handover|handoff|retro|session)s?\.'
    r'|^(learning-log|session-|handover-)',
    re.I)

def is_session_record(fname):
    return bool(_REC.search(fname))

def sync(src, dest, exclude, kind):
    os.makedirs(dest, exist_ok=True)
    copied = skipped_link = skipped_ex = refs = 0
    broken = []

    for name in sorted(os.listdir(src)):
        s = os.path.join(src, name)
        base = name[:-3] if name.endswith('.md') else name

        if os.path.islink(s) and not owned_link(s):   # OMC/codex 제공분
            skipped_link += 1; continue
        if os.path.islink(s):
            s = os.path.realpath(s)
        if base in exclude:
            skipped_ex += 1; continue
        if name.startswith('.') or name.endswith('.bak') or name.endswith('.md.bak'):
            continue

        # 알맹이가 깨진 스킬은 배포하지 않는다 — SKILL.md 가 없는 대상을 가리키는
        # 링크로만 남아 있는 경우. (커맨드 폴더는 SKILL.md 가 없는 게 정상이라 제외)
        if kind == '스킬' and os.path.isdir(s):
            if not any(os.path.exists(os.path.join(s, f))
                       for f in ('SKILL.md', 'README.md')):
                broken.append(name); continue

        d = os.path.join(dest, name)
        if os.path.isdir(s):
            if os.path.exists(d): shutil.rmtree(d)
            shutil.copytree(s, d, symlinks=False, ignore_dangling_symlinks=True,
                ignore=shutil.ignore_patterns(
                    '.git', 'node_modules', '__pycache__', '.DS_Store', '*.pyc',
                    # 실키가 든 로컬 파일은 절대 복사하지 않는다.
                    # (detail-page-team 에 실제 GEMINI 키가 들어 있었다 — 2026-07-27 검출)
                    '.env', '.env.*', '*.pem', '*.key', 'credentials.json',
                    'token.json', '.netrc'))
            # references/ 는 스킬마다 성격이 다르다.
            #   · 구동 자산(템플릿·컨버터·패턴 카탈로그) → 없으면 스킬이 깨진다. 유지
            #   · 세션 기록(날짜 붙은 로그·핸드오버·상태덤프) → 원 소유자 노하우. 제거
            # 전부 지우면 script-to-slides 처럼 assets 가 references 밑에 있는 스킬이
            # 조용히 망가진다(이전 배포판에서 실제로 그랬다).
            for dp, dns, _ in os.walk(d, topdown=True):
                for sub in list(dns):
                    if sub != 'references':
                        continue
                    rdir = os.path.join(dp, sub)
                    for rp, _, rfs in os.walk(rdir):
                        for rf in rfs:
                            if is_session_record(rf):
                                os.remove(os.path.join(rp, rf)); refs += 1
                    # 기록만 있던 폴더는 비면 지운다
                    for rp, rdns, rfs in os.walk(rdir, topdown=False):
                        if not os.listdir(rp):
                            os.rmdir(rp)
                    dns.remove(sub)
            for rel in ex_files:
                skill, _, sub = rel.partition('/')
                fp = os.path.join(d, sub)
                if skill == name and os.path.isfile(fp):
                    os.remove(fp)
                elif skill == name and os.path.isdir(fp):
                    shutil.rmtree(fp)
            for dp, _, fns in os.walk(d):
                for fn in fns: scrub_file(os.path.join(dp, fn))
            apply_patches(d, name)
        elif os.path.isfile(s):
            shutil.copy2(s, d); scrub_file(d)
        else:
            continue
        copied += 1

    print(f'  {kind}: {copied}개 동기화 · symlink {skipped_link}개 제외 '
          f'· 정책 제외 {skipped_ex}개 · 세션기록 {refs}건 제거')
    if broken:
        print(f'    ⚠ 로컬에서 이미 깨진 {kind} {len(broken)}개 제외: {", ".join(broken)}')

sync(src_skills, os.path.join(root, '02-skills'),   ex_skills, '스킬')
sync(src_cmds,   os.path.join(root, '03-commands'), ex_cmds,   '커맨드')
PY

echo
echo "다음: bash scripts/scan-personal.sh 02-skills"
