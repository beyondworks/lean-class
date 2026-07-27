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
)

# org-loop·볼트 등 개인 운영 인프라에 묶인 커맨드
EXCLUDE_CMDS=(
  board boot inbox delegate harvest start-loop skill-proposal
  loop-time looptime lt raw-press
)

python3 - "$ROOT" "$SRC_SKILLS" "$SRC_CMDS" \
  "$(IFS=,; echo "${EXCLUDE_SKILLS[*]}")" \
  "$(IFS=,; echo "${EXCLUDE_CMDS[*]}")" <<'PY'
import os, re, shutil, sys

root, src_skills, src_cmds = sys.argv[1], sys.argv[2], sys.argv[3]
ex_skills = set(filter(None, sys.argv[4].split(',')))
ex_cmds   = set(filter(None, sys.argv[5].split(',')))

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

        if os.path.islink(s):                 # OMC/codex 제공분
            skipped_link += 1; continue
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
            for dp, _, fns in os.walk(d):
                for fn in fns: scrub_file(os.path.join(dp, fn))
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
