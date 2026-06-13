#!/usr/bin/env python3
"""
CSS에서 색상 값을 추출하는 스크립트
"""

import re
import json
from collections import Counter
from typing import Dict, List, Tuple

# 색상 정규식 패턴
HEX_PATTERN = r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b'
RGB_PATTERN = r'rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)'
RGBA_PATTERN = r'rgba\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*([0-9.]+)\s*\)'
HSL_PATTERN = r'hsl\(\s*(\d{1,3})\s*,\s*(\d{1,3})%\s*,\s*(\d{1,3})%\s*\)'


def normalize_hex(hex_color: str) -> str:
    """HEX 색상을 6자리 소문자로 정규화"""
    hex_color = hex_color.lstrip('#').lower()
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    return f'#{hex_color}'


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """RGB를 HEX로 변환"""
    return f'#{r:02x}{g:02x}{b:02x}'


def hsl_to_hex(h: int, s: int, l: int) -> str:
    """HSL을 HEX로 변환"""
    s = s / 100
    l = l / 100
    
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)
    
    return rgb_to_hex(r, g, b)


def extract_colors(css_content: str) -> List[str]:
    """CSS에서 모든 색상 값 추출"""
    colors = []
    
    # HEX 색상
    for match in re.finditer(HEX_PATTERN, css_content):
        colors.append(normalize_hex(match.group(0)))
    
    # RGB 색상
    for match in re.finditer(RGB_PATTERN, css_content):
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        colors.append(rgb_to_hex(r, g, b))
    
    # RGBA 색상 (투명도 무시)
    for match in re.finditer(RGBA_PATTERN, css_content):
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        colors.append(rgb_to_hex(r, g, b))
    
    # HSL 색상
    for match in re.finditer(HSL_PATTERN, css_content):
        h, s, l = int(match.group(1)), int(match.group(2)), int(match.group(3))
        colors.append(hsl_to_hex(h, s, l))
    
    return colors


def analyze_colors(colors: List[str]) -> Dict:
    """색상 빈도 분석 및 분류"""
    counter = Counter(colors)
    
    # 빈도순 정렬
    sorted_colors = counter.most_common()
    
    # 색상 분류
    result = {
        "all": [{"color": c, "count": n} for c, n in sorted_colors],
        "primary": None,
        "secondary": None,
        "neutrals": [],
        "text": [],
        "background": []
    }
    
    for color, count in sorted_colors:
        # 회색 계열 분류
        if is_neutral(color):
            lightness = get_lightness(color)
            if lightness > 0.9:
                result["background"].append(color)
            elif lightness < 0.3:
                result["text"].append(color)
            else:
                result["neutrals"].append(color)
        else:
            # 첫 번째 유채색 → Primary
            if result["primary"] is None:
                result["primary"] = color
            # 두 번째 유채색 → Secondary
            elif result["secondary"] is None:
                result["secondary"] = color
    
    return result


def is_neutral(hex_color: str) -> bool:
    """회색 계열인지 판단"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # RGB 차이가 작으면 회색 계열
    return max(r, g, b) - min(r, g, b) < 30


def get_lightness(hex_color: str) -> float:
    """밝기 계산 (0-1)"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    
    return (max(r, g, b) + min(r, g, b)) / 2


def lighten(hex_color: str, amount: float = 0.2) -> str:
    """색상 밝게"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    r = min(255, int(r + (255 - r) * amount))
    g = min(255, int(g + (255 - g) * amount))
    b = min(255, int(b + (255 - b) * amount))
    
    return rgb_to_hex(r, g, b)


def darken(hex_color: str, amount: float = 0.2) -> str:
    """색상 어둡게"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    r = max(0, int(r * (1 - amount)))
    g = max(0, int(g * (1 - amount)))
    b = max(0, int(b * (1 - amount)))
    
    return rgb_to_hex(r, g, b)


def generate_color_tokens(analysis: Dict) -> Dict:
    """분석 결과로 토큰 생성"""
    primary = analysis.get("primary") or "#FF6B35"
    secondary = analysis.get("secondary") or "#004E89"
    
    # Neutral 스케일 생성
    neutral_scale = {
        "50": "#fafafa",
        "100": "#f5f5f5",
        "200": "#eeeeee",
        "300": "#e0e0e0",
        "400": "#bdbdbd",
        "500": "#9e9e9e",
        "600": "#757575",
        "700": "#616161",
        "800": "#424242",
        "900": "#212121"
    }
    
    # 실제 추출된 neutral이 있으면 매핑
    if analysis.get("neutrals"):
        for i, color in enumerate(analysis["neutrals"][:10]):
            keys = list(neutral_scale.keys())
            if i < len(keys):
                neutral_scale[keys[i]] = color
    
    tokens = {
        "primary": {
            "main": primary,
            "light": lighten(primary, 0.3),
            "dark": darken(primary, 0.2),
            "contrastText": "#ffffff"
        },
        "secondary": {
            "main": secondary,
            "light": lighten(secondary, 0.3),
            "dark": darken(secondary, 0.2),
            "contrastText": "#ffffff"
        },
        "neutral": neutral_scale,
        "text": {
            "primary": analysis.get("text", ["#212121"])[0] if analysis.get("text") else "#212121",
            "secondary": "#757575",
            "disabled": "#bdbdbd"
        },
        "background": {
            "default": analysis.get("background", ["#ffffff"])[0] if analysis.get("background") else "#ffffff",
            "paper": "#f5f5f5",
            "dark": "#212121"
        },
        "success": "#4caf50",
        "warning": "#ff9800",
        "error": "#f44336",
        "info": "#2196f3"
    }
    
    return tokens


def main():
    """메인 실행"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extract_colors.py <css_file_or_content>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # 파일 읽기 또는 직접 입력
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except FileNotFoundError:
        css_content = input_path
    
    # 색상 추출 및 분석
    colors = extract_colors(css_content)
    analysis = analyze_colors(colors)
    tokens = generate_color_tokens(analysis)
    
    # JSON 출력
    print(json.dumps(tokens, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
