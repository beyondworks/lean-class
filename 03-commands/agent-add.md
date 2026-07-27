---
description: 새 에이전트(팀원)를 추가하거나 명단을 본다 — 이름·역할 자유
argument-hint: "<슬러그(영문)> <한글이름> <역할>  — 예: lucy 루시 데이터  (인자 없으면 명단만 표시)"
---

팀 명단은 `{{PROJECTS_ROOT}}/_bus/roster.tsv` 한 파일이 단일 소스다.

## 명단 보기
```bash
bash {{PROJECTS_ROOT}}/_bus/bus.sh roster
```

## 추가 (`$ARGUMENTS` = 슬러그 한글이름 역할)
```bash
bash {{PROJECTS_ROOT}}/_bus/bus.sh roster add $ARGUMENTS
```
- 슬러그=영문 소문자(폴더·식별), 한글이름=호출명, 역할=직무.
- 실행되면: 명단 추가 + 폴더 생성 + `{{PROJECTS_ROOT}}/AI-Native/org/<슬러그>.md` 카드 자동 생성.
- 그다음 **카드(`org/<슬러그>.md`)에 페르소나 성격·North Star·직무를 채운다**(사용자에게 어떤 성격·역할로 만들지 1~2개만 물어 채워주면 좋다).

## 이름·역할 변경
- `{{PROJECTS_ROOT}}/_bus/roster.tsv` 의 해당 줄을 고친다(슬러그는 폴더명이라 가급적 유지). 변경 후 `bash {{PROJECTS_ROOT}}/_bus/bus.sh sync`.

> 카드 내용은 그 에이전트의 정체성이다. 비워두지 말고 채울 것.
