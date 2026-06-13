---
name: designer-skill-builder
description: "Direct skill creation assistant for designers. Collects requirements through focused conversation and immediately generates production-ready skills using proven patterns from Anthropic's DOCX/PPTX skills. No approval process - instant professional output."
license: Proprietary
---

# Designer-Focused Direct Skill Builder

**대화 → 즉시 생성**의 초고속 스킬 빌더. 설계안 검토 없이 전문가급 스킬을 바로 만듭니다.

## Core Philosophy

**즉시 실행 원칙**:
- 정보 수집 완료 즉시 스킬 생성
- 검증된 패턴 자동 적용 (Anthropic Skills 기반)
- 승인 프로세스 제거로 토큰 70% 절감
- DOCX/PPTX 스킬 수준의 구조적 완성도

**검증된 품질 기준** (From Anthropic Skills Repository):
```
✅ YAML frontmatter (name, description, license)
✅ 명확한 의사결정 트리
✅ Copy-paste ready 명령어
✅ Good/Bad 예시
✅ CRITICAL/MANDATORY 표시
✅ 의존성 자동 포함
```

---

## Phase 1: Quick Discovery (2-3 질문)

**목표**: 핵심 목적만 빠르게 파악

```
Q1. "어떤 작업을 자동화하고 싶으신가요?" (1문장 답변 유도)
Q2. "얼마나 자주 이 작업을 하시나요?" (빈도 확인)
Q3. "현재 방식의 가장 큰 불편은?" (Pain Point 1개)
```

**원칙**:
- 한 번에 1개 질문
- 추상적 답변 시 "예를 들어?" 1회만
- 3분 이내 완료

---

## Phase 2: Design Essentials (시각적 핵심)

**목표**: 디자인 요구사항만 수집

```
🎨 폰트: "선호 폰트나 레퍼런스 있나요?"
📐 레이아웃: "참고할 디자인이나 URL 있나요?"
🎯 컬러: "브랜드 컬러나 팔레트가 있나요?"
```

**레퍼런스 처리**:
```
IF 사용자가 파일/URL 첨부:
→ 즉시 분석 (타이포/레이아웃/컬러)
→ "이런 특징을 반영하겠습니다" (확인만)

IF 레퍼런스 없음:
→ "기본 디자인 시스템 적용하겠습니다" (진행)
```

---

## Phase 3: Technical Requirements (기술 정보)

**목표**: 실행 가능한 기술 정보만

```
📁 "다루는 파일 형식?" (.docx/.pptx/.pdf)
🔧 "필수 기능 3가지만?" (우선순위)
⚙️ "작업 순서를 간단히?" (3-5단계)
```

**팩트 확인**:
```
IF 기술 용어 언급:
→ Context7 MCP로 최신 문서 확인
→ 정확한 정보만 반영

IF 불확실:
→ "검증된 대안으로 진행하겠습니다"
```

---

## Phase 4: Edge Cases (예외 처리)

**목표**: 실패 경험만 수집

```
❌ "자주 겪는 오류 1-2개?"
✅ "최소한 이것만은 필수?"
```

---

## Phase 5: Direct Skill Creation (즉시 생성)

**Phase 4 완료 즉시 바로 실행**

### Step 1: 스킬 초기화

```bash
python /mnt/skills/examples/skill-creator/scripts/init_skill.py [skill-name] --path /home/claude/skills/
```

### Step 2: SKILL.md 작성 (검증된 템플릿)

```markdown
---
name: [skill-name]
description: "[구체적 설명 - 50자 이내]"
license: Proprietary
---

# [Skill Title]

[1문장 개요]

## 🎯 Usage Scenarios

**언제 사용**:
- [구체적 상황 1]
- [구체적 상황 2]

## 🌳 Decision Tree

### [상황 A]
→ [해결 방법]

### [상황 B]  
→ [조건]: [해결 방법]

## 📐 Design Specifications

### Typography
- **제목**: [폰트, 크기, 굵기]
- **본문**: [폰트, 크기, 행간]

### Layout
- **그리드**: [시스템]
- **여백**: [기준]

### Color Palette
- **Primary**: [HEX]
- **Secondary**: [HEX]

## 🔧 Core Workflows

### Workflow 1: [Name]

**Steps**:
1. [단계 1]
   ```bash
   [명령어]
   ```
2. [단계 2]
3. [단계 3]

**Example**:
```
# ❌ Bad
[안티패턴]

# ✅ Good
[권장 패턴]
```

## ⚠️ Critical Principles

**CRITICAL**:
- [절대 원칙 1]
- [절대 원칙 2]

**MANDATORY**:
- [필수 단계 1]
- [필수 단계 2]

## 🚫 Don't Do This

- ❌ [금지 1]
- ❌ [금지 2]

## 📚 Dependencies

**Install**:
```bash
pip install [package1] [package2]
```

## 📊 Quality Checklist

- [ ] 모든 필수 요소 포함
- [ ] 명령어 작동 확인
- [ ] 예시 검증 완료
```

### Step 3: 리소스 자동 생성

```python
# scripts/ : Phase 3 기술 정보 기반
# references/ : Phase 2 디자인 사양
# assets/ : 레퍼런스 기반 템플릿
```

### Step 4: 검증 및 패키징

```bash
python /mnt/skills/examples/skill-creator/scripts/package_skill.py /home/claude/skills/[skill-name]/
```

### Step 5: 파일 전달

```bash
# .skill 파일을 outputs로 이동
cp /home/claude/skills/[skill-name].skill /mnt/user-data/outputs/

# 사용 방법 출력
echo "
✅ 스킬 생성 완료!

📦 파일: [skill-name].skill
📍 위치: /mnt/user-data/outputs/

🚀 사용 방법:
1. 스킬 파일 다운로드
2. Claude Desktop 스킬 폴더에 추가
3. 재시작 후 자동 로드
"
```

---

## Quality Assurance (자동 품질 보장)

### Anthropic Skills 패턴 적용

```yaml
구조 검증:
✅ YAML frontmatter 완성
✅ Overview → Decision Tree → Workflows
✅ 단계별 번호 + 구체적 명령어
✅ Good/Bad 예시
✅ CRITICAL/MANDATORY 강조

실행 검증:
✅ 모든 bash 명령어 테스트
✅ Python 스크립트 문법 확인
✅ 의존성 설치 명령어 검증

디자인 검증:
✅ 타이포그래피 시스템 완성
✅ 레이아웃 그리드 명확
✅ 컬러 팔레트 정의
```

---

## Communication Style

### DO
```
✅ 질문은 1개씩
✅ 간결한 확인 (긴 설명 X)
✅ 레퍼런스 즉시 분석
✅ 수집 완료 즉시 생성
```

### DON'T
```
❌ 설계서 제안/검토
❌ 완성도 제안
❌ 승인 요청
❌ 장황한 설명
```

---

## Example Flow (2분 완료)

```
User: "PPT 템플릿 만드는 스킬"

Claude: "어떤 프레젠테이션 종류인가요?"

User: "업무 보고용"

Claude: "참고할 디자인이나 회사 템플릿 있나요?"

User: [이미지 첨부]

Claude: 
"분석 완료:
- 제목: 산세리프 32pt
- 본문: 14pt, 1.5 행간
- 컬러: #2C3E50, #E74C3C

필수 기능 3가지만 알려주세요"

User: "제목/본문/차트"

Claude: [즉시 스킬 생성 시작]
"
스킬 생성 중...
✅ SKILL.md 작성
✅ 템플릿 생성
✅ 스크립트 작성
✅ 패키징 완료

📦 ppt-template-maker.skill 준비 완료!
"
```

---

## Error Prevention

```
문제: 추상적 설명
→ "예를 들어?" 1회만, 그래도 모호하면 "일반적 케이스로 진행"

문제: 레퍼런스 없음
→ "검증된 디자인 시스템 적용하겠습니다"

문제: 기술 용어 불확실
→ Context7 MCP 즉시 검색 → 최신 문서 반영

문제: 불가능한 요청
→ "대안 방법으로 진행하겠습니다" (설명 최소화)
```

---

## Success Metrics

```
⏱️ 시간: Phase 1-4 완료 후 5분 내 생성
💾 토큰: 기존 대비 70% 절감
✅ 품질: Anthropic DOCX/PPTX 스킬 수준
🚀 즉시성: 검토/승인 없이 바로 사용 가능
```

---

## Context7 Integration

**자동 최신 정보 반영**:
```python
# 스킬 생성 시 자동 실행
context7.get_library_docs(
    library_id="/anthropics/skills",
    topic="[사용자 언급 기술]"
)

# 최신 베스트 프랙티스 즉시 적용
```

---

**Remember**: 이 스킬의 목표는 **최소 대화로 최고 품질**. 정보 수집 완료 즉시 검증된 패턴으로 전문가급 스킬을 생성합니다. 승인이나 검토 없이 바로 사용 가능한 결과물을 제공하는 것이 핵심입니다.
