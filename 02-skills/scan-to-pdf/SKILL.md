---
name: scan-to-pdf
description: 서류 사진에서 텍스트를 파싱하여 완벽하게 반듯한 PDF를 새로 생성
trigger: scan, 스캔, pdf 변환, 문서 스캔, document scan
---

# scan-to-pdf

서류 사진을 분석하여 텍스트를 추출하고, 처음부터 새로 깨끗한 PDF를 생성한다.
사진의 기울기/원근을 보정하는 것이 아니라, 데이터를 파싱해서 완전히 새 문서로 재구성.

## 워크플로우

### Step 1: 전처리
```bash
python3.11 ~/.claude/skills/scan-to-pdf/scan_to_pdf.py --preprocess /path/to/photo.jpg
```
→ `/tmp/scan_preprocessed.png` (보정된 이미지)
→ `/tmp/scan_main_seal.png` (인감 도장 - 있는 경우)
→ `/tmp/scan_seal.png` (직인/관인 - 있는 경우)

### Step 2: 데이터 추출
전처리된 이미지를 Read 도구로 열어서 **모든 내용을 빠짐없이** 읽는다.

**필수 확인 항목:**
- 제목, 본문 텍스트 전체
- 표가 있으면 모든 행/열 데이터
- 하단 안내문: **모든 번호 단락** (1번, 2번, 3번...) 빠짐없이
- 발급번호, 확인번호, 바코드 번호 등 부가 정보
- 페이지 번호 (예: -1/1-)
- 날짜, 기관명, 직위 등

읽은 데이터를 JSON 파일로 저장:
```bash
# /tmp/scan_data.json 작성 (Write 도구 사용)
```

### Step 3: PDF 생성
```bash
python3.11 ~/.claude/skills/scan-to-pdf/scan_to_pdf.py --generate /tmp/scan_data.json -o ~/Desktop/output.pdf
```

## 이미지 기반 모드 (fallback)
표가 아닌 문서나 단순 보정만 필요할 때:
```bash
python3.11 ~/.claude/skills/scan-to-pdf/scan_to_pdf.py /path/to/photo.jpg -o output.pdf
```

## 의존성
```bash
pip3 install opencv-python numpy deskew img2pdf Pillow reportlab
```

## JSON 데이터 형식
```json
{
  "title": "문서 제목",
  "header": ["열1", "열2", ...],
  "rows": [["값1", "값2", ...], ...],
  "main_seal_path": "/tmp/scan_main_seal.png",
  "main_seal_size_mm": 35,
  "footer_text": "본문 하단 텍스트 (증명 문구 등)",
  "date": "날짜",
  "company_info": [{"label": "기관명:", "value": "기관이름"}],
  "seal_path": "/tmp/scan_seal.png",
  "footer_notes": [
    "1. 첫 번째 안내 단락 전체 텍스트",
    "2. 두 번째 안내 단락 전체 텍스트"
  ],
  "issuance_info": [
    "발급번호: XXXX-XXXX-XXXX",
    "- 1/1 -"
  ]
}
```

### 필드 설명
- `title`: 문서 제목 (테두리 박스 안 큰 글씨)
- `header` / `rows`: 표 데이터 (표가 없으면 생략)
- `main_seal_path`: 인감 도장 이미지 경로 (중앙 배치, 1:1 비율)
- `main_seal_size_mm`: 인감 크기 mm (기본값 35)
- `footer_text`: 증명 문구 등 본문 텍스트
- `date`: 날짜
- `company_info`: 기관/회사 정보 (label + value 배열)
- `seal_path`: 직인/관인 이미지 경로 (1:1 비율 자동 보장)
- `footer_notes`: 하단 구분선 아래 번호 달린 안내 단락들 (배열)
- `issuance_info`: 발급번호, 페이지번호 등 부가 정보 (배열)
- rows에서 줄바꿈은 `\n` 사용

## 주의사항
- 전처리 후 반드시 이미지를 Read로 열어 **모든 텍스트를 빠짐없이** 확인
- 공식 문서이므로 숫자, 이름, 날짜 정확도가 중요
- 인감/직인은 원형 도장이므로 반드시 1:1 비율 유지 (코드에서 정사각형 크롭 자동 적용)
- 하단 안내문은 1번 단락만이 아니라 **모든 번호 단락**을 포함
- 발급번호, 확인번호, 페이지번호 등 문서 하단/우측의 부가 정보도 반드시 포함
