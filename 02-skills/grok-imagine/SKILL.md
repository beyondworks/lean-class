---
name: grok-imagine
description: Grok(xAI Aurora) 이미지/영상 생성 프롬프트 최적화 및 캐릭터 일관성 가이드. grok, xai, aurora, imagine 키워드에 트리거.
---

# Grok Imagine — 프롬프트 최적화 & 캐릭터 일관성 가이드

xAI Aurora 기반 이미지/영상 생성 시 반드시 참조하는 프롬프트 엔지니어링 레퍼런스.

---

## Session reference files


## 1. API 엔드포인트 & 파라미터

### 이미지

```
POST https://api.x.ai/v1/images/generations   # 새 이미지
POST https://api.x.ai/v1/images/edits          # 레퍼런스 기반 편집
```

| 파라미터 | 값 | 비고 |
|---|---|---|
| `model` | `grok-imagine-image-quality` | 공식 xAI Imagine 이미지 예시 모델명 |
| `aspect_ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `auto` 등 | 용도에 맞게 명시 |
| `resolution` | `1k` (기본), `2k` | 2k는 비용 증가 |
| `n` | 1–10 | 배치 생성 |
| `response_format` | `url`, `b64_json` | URL은 임시 — 즉시 다운로드 |

### 영상

```
POST /v1/videos/generations    # 생성 (비동기, 폴링 필요)
POST /v1/videos/edits          # 편집 (원본 duration/ratio 유지)
POST /v1/videos/extensions     # 확장 (이어붙이기)
GET  /v1/videos/{request_id}   # 상태 조회 (15초 간격 폴링)
```

| 파라미터 | 값 | 비고 |
|---|---|---|
| `model` | `grok-imagine-video` | 유일한 모델 |
| `duration` | 1–15초 (생성), 2–10초 (확장) | |
| `resolution` | `480p` (빠름), `720p` (고화질) | |
| `image` | URL 또는 base64 | 첫 프레임 고정 (image-to-video) |
| `reference_images` | URL 배열 | 스타일 참조 (첫 프레임 고정 없음) |

**`image` vs `reference_images`는 동시 사용 불가.**

---

## 2. 프롬프트 핵심 원칙

### Aurora는 자연어 서술 모델이다

- Midjourney식 키워드 나열 금지 → **문장으로 서술**
- 네거티브 프롬프트 효과 없음 → **양성 제약으로 대체**
  - `no blur` (X) → `sharp focus, crisp details` (O)
  - `no text` (X) → `clean background without any lettering` (O)
- 추상적 감정 금지 → **관찰 가능한 시각적 현상으로 변환**
  - `happy` (X) → `laughing with eyes closed, shoulders shaking` (O)
  - `cool city` (X) → `neon-lit alley at 3am, rain-slicked pavement reflecting purple signs` (O)

### 프롬프트 공식 (이미지)

```
[주체 + 구체적 세부사항]
+ [행동/자세]
+ [환경 + 구체적 시각 요소]
+ [조명 유형]
+ [카메라/렌즈 사양 또는 아트 스타일]
+ [무드/분위기]
+ [색상 팔레트]
```

### 프롬프트 공식 (영상) — 5-레이어

```
Layer 1 — Scene:   무엇이 일어나는가
Layer 2 — Camera:  카메라 무브먼트
Layer 3 — Style:   시각 스타일
Layer 4 — Motion:  움직임 강도/방향
Layer 5 — Audio:   소리 (미지정 시 기본 BGM 삽입됨)
```

**image-to-video에서는 이미 있는 것을 재서술하지 말고 변화와 움직임에 집중.**

---

## 3. 스타일 키워드 사전

### 포토리얼리스틱
```
shot on Canon EOS R5, 85mm lens, shallow depth of field
shot on Leica M10, 35mm Summilux f/1.4
editorial photography, National Geographic style
studio lighting, product photography
```

### 플랫 일러스트레이션
```
flat vector illustration, clean lines, minimal shading,
solid color fills, Dribbble style, 2D
```

### 애니메이션
```
Studio Ghibli style, soft watercolor backgrounds, warm palette
MAPPA style, high contrast, dynamic action lines
```

### 조명
```
golden hour                    # 따뜻한 자연광
dramatic chiaroscuro           # 강한 명암
volumetric god rays            # 빛줄기
rim lighting                   # 윤곽 빛
soft diffused light            # 부드러운 확산광
neon backlight                 # 네온 역광
```

### 카메라 앵글
```
close-up, medium shot, wide shot
over-the-shoulder, aerial, POV
low-angle, upward camera angle
```

### 영상 카메라 무브먼트
```
slow dolly in / dolly out
tracking shot
drone fly-through
handheld shaky camera
camera slowly orbiting
pan left / pan right
static tripod
```

### 색상 팔레트 제어
```
# 구체적으로 지정 (추상 금지)
"electric blue and hot pink" (O)  vs  "colorful" (X)
"warm amber and deep burgundy" (O) vs  "warm colors" (X)
"monochrome with single red accent"
"color palette: muted sage green, cream white, terracotta"
```

---

## 4. 캐릭터 일관성 기법 (핵심)

### 방법 1: /edits 엔드포인트 (가장 효과적)

원본 이미지를 `image` 파라미터로 넘기고 변형 프롬프트 작성.

```python
resp = requests.post(
    "https://api.x.ai/v1/images/edits",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "model": "grok-imagine-image-quality",
        "prompt": "Same character, now with a surprised expression, same style and colors",
        "image": {"url": f"data:image/png;base64,{b64}"},
        "n": 1,
        "response_format": "url"
    }
)
```

### 방법 2: 캐릭터 바이블 프롬프트

매 프롬프트 앞에 동일한 캐릭터 설명 블록 고정:

```
Character reference: [이름]
Physical traits: [나이, 체형, 피부톤, 머리]
Distinctive features: [특징적 외모 요소]
Outfit: [의상]
Style: [아트 스타일 앵커]
---
Scene: [이번 씬]
Action: [동작]
Environment: [배경]
Maintain character consistency
```

### 방법 3: 영상 프레임 체이닝

```
1. 키 프레임 이미지 생성 (/generations)
2. image-to-video로 첫 클립 생성 (/videos/generations + image)
3. 마지막 프레임 추출: ffmpeg -sseof -0.1 -i clip.mp4 -vsync 0 -q:v 1 last.jpg
4. 추출한 프레임을 다음 클립의 image로 사용
5. 또는 /videos/extensions로 직접 연장
```

### 방법 4: 영상에서 reference_images

```json
{
  "model": "grok-imagine-video",
  "prompt": "Show the character walking through a corridor",
  "reference_images": [
    {"url": "https://cdn.example.com/character.png", "type": "image_url"}
  ]
}
```

첫 프레임 고정 없이 스타일/캐릭터만 참조.

### 일관성 우선순위

| 순위 | 방법 | 일관성 | 용도 |
|---|---|---|---|
| 1 | /edits + 원본 이미지 | 최상 | 포즈/표정 변형 |
| 2 | 프레임 체이닝 | 상 | 영상 씬 연결 |
| 3 | reference_images | 중상 | 영상 스타일 참조 |
| 4 | 캐릭터 바이블 프롬프트 | 중 | 원본 없을 때 |
| 5 | /generations 프롬프트만 | 하 | 새 캐릭터 탐색 |

---

## 5. 피해야 할 실수

1. **한 프롬프트에 10개 이상 요소** → 3-4개 핵심에 집중
2. **모순된 스타일** → `photorealistic` + `cartoon` 동시 사용 금지
3. **브랜드명 단독** → `"Nike shoes"` 대신 구체적 묘사
4. **텍스트 렌더링** → 이미지 내 텍스트는 후처리 권장
5. **aspect_ratio 미지정** → 용도에 맞게 항상 명시
6. **영상 오디오 미지정** → 기본 BGM 삽입됨, 원치 않으면 명시
7. **URL 미다운로드** → 생성 URL은 임시, 즉시 저장 필수
8. **OpenAI SDK images.edit()** → xAI 비호환, 직접 HTTP 호출 사용

---

## 6. 비용 참고

| 항목 | 단가 |
|---|---|
| 이미지 (standard) | $0.02/장 |
| 이미지 (pro) | $0.07/장 |
| 영상 | $0.05/초 |

---

## 7. Python 코드 패턴

### 이미지 생성 + 즉시 다운로드

```python
import requests, os, json

API_KEY = os.getenv("XAI_API_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def grok_generate_image(prompt, aspect_ratio="9:16", resolution="1k", n=1):
    resp = requests.post(
        "https://api.x.ai/v1/images/generations",
        headers=HEADERS,
        json={"model": "grok-imagine-image-quality", "prompt": prompt,
              "n": n, "aspect_ratio": aspect_ratio,
              "resolution": resolution, "response_format": "url"}
    )
    data = resp.json()
    urls = [d["url"] for d in data["data"]]
    # 즉시 다운로드 (URL은 임시)
    images = []
    for i, url in enumerate(urls):
        img = requests.get(url).content
        path = f"output_{i}.jpeg"
        with open(path, "wb") as f:
            f.write(img)
        images.append(path)
    return images
```

### 레퍼런스 기반 편집 (캐릭터 일관성)

```python
import base64

def grok_edit_image(ref_image_path, prompt, aspect_ratio=None):
    with open(ref_image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    body = {
        "model": "grok-imagine-image-quality",
        "prompt": prompt,
        "image": {"url": f"data:image/png;base64,{b64}"},
        "n": 1, "response_format": "url"
    }
    if aspect_ratio:
        body["aspect_ratio"] = aspect_ratio

    resp = requests.post("https://api.x.ai/v1/images/edits", headers=HEADERS, json=body)
    url = resp.json()["data"][0]["url"]
    img = requests.get(url).content
    out = "edited_output.jpeg"
    with open(out, "wb") as f:
        f.write(img)
    return out
```

### 영상 생성 (비동기 폴링)

```python
import time

def grok_generate_video(prompt, image_path=None, duration=5, resolution="720p", aspect_ratio="9:16"):
    body = {
        "model": "grok-imagine-video",
        "prompt": prompt,
        "duration": duration,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution
    }
    if image_path:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        body["image"] = f"data:image/png;base64,{b64}"

    resp = requests.post("https://api.x.ai/v1/videos/generations", headers=HEADERS, json=body)
    request_id = resp.json()["request_id"]

    while True:
        status = requests.get(
            f"https://api.x.ai/v1/videos/{request_id}", headers=HEADERS
        ).json()
        if status.get("video", {}).get("url"):
            url = status["video"]["url"]
            video = requests.get(url).content
            out = "output_video.mp4"
            with open(out, "wb") as f:
                f.write(video)
            return out
        time.sleep(15)
```
