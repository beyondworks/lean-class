#!/usr/bin/env python3.11
"""
scan_to_pdf.py — 서류 사진에서 텍스트를 파싱하여 완벽한 PDF를 새로 생성

사용법:
  # 모드 1: 전처리 (이미지 보정 + 표 구조 감지 + 직인 추출)
  python3.11 scan_to_pdf.py --preprocess input.jpg

  # 모드 2: PDF 생성 (JSON 데이터 → reportlab PDF)
  python3.11 scan_to_pdf.py --generate data.json -o output.pdf

  # 기존 모드: 이미지 기반 PDF (하위 호환)
  python3.11 scan_to_pdf.py input.jpg -o output.pdf
  python3.11 scan_to_pdf.py img1.jpg img2.jpg -o out.pdf
"""

import argparse
import json
import os
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import img2pdf

A4_RATIO = 297 / 210  # ~1.4142


# ─── 전처리 함수들 (이미지 보정) ───


def apply_exif_orientation(pil_img: Image.Image) -> Image.Image:
    """EXIF 회전 정보를 실제 픽셀에 반영."""
    return ImageOps.exif_transpose(pil_img)


def order_points(pts: np.ndarray) -> np.ndarray:
    """4개 꼭짓점을 [좌상, 우상, 우하, 좌하] 순서로 정렬."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    d = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(d)]
    rect[3] = pts[np.argmax(d)]
    return rect


def expand_points(pts: np.ndarray, img_shape: tuple, margin_pct: float = 0.02) -> np.ndarray:
    """감지된 4점을 바깥으로 margin만큼 확장 (내용 잘림 방지)."""
    h, w = img_shape[:2]
    diag = np.sqrt(h**2 + w**2)
    margin = diag * margin_pct

    rect = order_points(pts.astype("float32"))
    center = rect.mean(axis=0)

    expanded = np.zeros_like(rect)
    for i, pt in enumerate(rect):
        direction = pt - center
        length = np.linalg.norm(direction)
        if length > 0:
            direction = direction / length
        expanded[i] = pt + direction * margin

    expanded[:, 0] = np.clip(expanded[:, 0], 0, w - 1)
    expanded[:, 1] = np.clip(expanded[:, 1], 0, h - 1)
    return expanded


def find_document_contour(image: np.ndarray):
    """이미지에서 가장 큰 사각형 윤곽(4점)을 감지. 실패 시 None 반환."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 20, 80)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    edged = cv2.dilate(edged, kernel, iterations=3)
    edged = cv2.erode(edged, kernel, iterations=1)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    img_area = image.shape[0] * image.shape[1]

    best = None
    best_area = 0
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            area = cv2.contourArea(approx)
            if area > img_area * 0.1 and area > best_area:
                best = approx.reshape(4, 2)
                best_area = area
    return best


def get_rotation_angle_from_contour(pts: np.ndarray) -> float:
    """4점 윤곽에서 문서의 미세 회전 각도(-15~+15도)를 추출."""
    rect = order_points(pts.astype("float32"))
    tl, tr, br, bl = rect
    dx = tr[0] - tl[0]
    dy = tr[1] - tl[1]
    angle = np.degrees(np.arctan2(dy, dx))
    if abs(angle) > 15:
        return 0.0
    return angle


def perspective_transform(image: np.ndarray, pts: np.ndarray) -> np.ndarray:
    """4점 원근 변환으로 직사각형으로 보정. A4 비율 유지."""
    rect = order_points(pts.astype("float32"))
    tl, tr, br, bl = rect

    width_top = np.linalg.norm(tr - tl)
    width_bot = np.linalg.norm(br - bl)
    max_w = int(max(width_top, width_bot))

    height_left = np.linalg.norm(bl - tl)
    height_right = np.linalg.norm(br - tr)
    max_h = int(max(height_left, height_right))

    if max_h >= max_w:
        target_h = int(max_w * A4_RATIO)
        if target_h > max_h:
            max_h = target_h
        else:
            max_w = int(max_h / A4_RATIO)
    else:
        target_w = int(max_h * A4_RATIO)
        if target_w > max_w:
            max_w = target_w
        else:
            max_h = int(max_w / A4_RATIO)

    dst = np.array([
        [0, 0], [max_w - 1, 0],
        [max_w - 1, max_h - 1], [0, max_h - 1],
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (max_w, max_h),
                               borderMode=cv2.BORDER_REPLICATE)


def rotate_full_image(image: np.ndarray, angle: float) -> np.ndarray:
    """전체 이미지를 주어진 각도로 회전. 캔버스 확장하여 잘림 방지."""
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    cos = abs(M[0, 0])
    sin = abs(M[0, 1])
    new_w = int(h * sin + w * cos)
    new_h = int(h * cos + w * sin)
    M[0, 2] += (new_w - w) / 2
    M[1, 2] += (new_h - h) / 2
    return cv2.warpAffine(image, M, (new_w, new_h),
                          borderMode=cv2.BORDER_REPLICATE)


def deskew(image: np.ndarray) -> np.ndarray:
    """미세 기울기 보정 (minAreaRect 기반)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    if len(coords) < 100:
        return image
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    if abs(angle) < 0.3:
        return image
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)


def _find_peaks(projection: np.ndarray, threshold: float, min_gap: int = 15) -> list[int]:
    """프로젝션 프로파일에서 피크 위치(선 위치) 추출."""
    positions = []
    in_peak = False
    peak_weighted = 0.0
    peak_sum = 0.0

    for i, val in enumerate(projection):
        if val > threshold:
            if not in_peak:
                in_peak = True
                peak_weighted = 0.0
                peak_sum = 0.0
            peak_sum += val
            peak_weighted += i * val
        else:
            if in_peak:
                center = int(round(peak_weighted / peak_sum))
                if not positions or center - positions[-1] > min_gap:
                    positions.append(center)
                in_peak = False

    if in_peak and peak_sum > 0:
        center = int(round(peak_weighted / peak_sum))
        if not positions or center - positions[-1] > min_gap:
            positions.append(center)

    return positions


def extract_document_colors(image: np.ndarray) -> np.ndarray:
    """검정(텍스트) + 빨강(직인) + 보라 + 파랑만 남기고 나머지를 흰색으로 치환."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # 종이 영역 감지
    paper_mask = ((v > 180) & (s < 40)).astype(np.uint8) * 255
    paper_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
    paper_mask = cv2.morphologyEx(paper_mask, cv2.MORPH_CLOSE, paper_kernel, iterations=3)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(paper_mask, connectivity=8)
    paper_region = np.ones(image.shape[:2], dtype=np.uint8) * 255
    if num_labels > 1:
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        paper_region = (labels == largest_label).astype(np.uint8) * 255
        shrink_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40))
        paper_region = cv2.erode(paper_region, shrink_kernel, iterations=1)

    # 적응형 이진화
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_masked = gray.copy()
    gray_masked[paper_region == 0] = 255
    blurred_region = cv2.GaussianBlur(paper_region.astype(np.float32), (101, 101), 0)
    blend = blurred_region / 255.0
    gray_masked = (gray.astype(np.float32) * blend + 255.0 * (1.0 - blend)).astype(np.uint8)

    text_mask = cv2.adaptiveThreshold(
        gray_masked, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, blockSize=51, C=15
    )

    # 색상 마스크
    red_mask1 = (h <= 10) & (s > 60) & (v > 60)
    red_mask2 = (h >= 160) & (s > 60) & (v > 60)
    red_mask = red_mask1 | red_mask2
    blue_mask = (h >= 100) & (h <= 130) & (s > 50) & (v > 50)
    purple_mask = (h >= 130) & (h <= 160) & (s > 50) & (v > 50)

    color_mask = (red_mask | blue_mask | purple_mask).astype(np.uint8) * 255
    color_mask = cv2.bitwise_and(color_mask, paper_region)

    # 모폴로지
    kernel_small = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, kernel_small, iterations=1)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_CLOSE, kernel_close, iterations=1)

    # 고립 블롭 제거
    combined = cv2.bitwise_or(text_mask, color_mask)
    connect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 200))
    connected = cv2.dilate(combined, connect_kernel, iterations=2)
    num_cc, cc_labels, cc_stats, _ = cv2.connectedComponentsWithStats(connected, connectivity=8)
    if num_cc > 2:
        img_h, img_w = image.shape[:2]
        inner_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 80))
        inner_paper = cv2.erode(paper_region, inner_kernel, iterations=1)

        areas = cc_stats[1:, cv2.CC_STAT_AREA]
        total_area = areas.sum()
        for i in range(1, num_cc):
            cc_area = cc_stats[i, cv2.CC_STAT_AREA]
            cc_x = int(cc_stats[i, cv2.CC_STAT_LEFT] + cc_stats[i, cv2.CC_STAT_WIDTH] / 2)
            cc_y = int(cc_stats[i, cv2.CC_STAT_TOP] + cc_stats[i, cv2.CC_STAT_HEIGHT] / 2)
            cc_x = min(cc_x, img_w - 1)
            cc_y = min(cc_y, img_h - 1)
            in_inner = inner_paper[cc_y, cc_x] > 0
            if not in_inner and cc_area < total_area * 0.10:
                cluster_mask = (cc_labels == i).astype(np.uint8) * 255
                text_mask = cv2.bitwise_and(text_mask, cv2.bitwise_not(cluster_mask))
                color_mask = cv2.bitwise_and(color_mask, cv2.bitwise_not(cluster_mask))

    result = np.full_like(image, 255)
    result[text_mask > 0] = [0, 0, 0]
    result[color_mask > 0] = image[color_mask > 0]
    return result


def hough_deskew(image: np.ndarray) -> np.ndarray:
    """Hough line으로 표의 가로선 각도를 찾아 정밀 회전 보정."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    h, w = image.shape[:2]
    min_line_length = w * 0.15
    lines = cv2.HoughLinesP(edges, 1, np.pi / 1800, threshold=100,
                             minLineLength=int(min_line_length), maxLineGap=20)
    if lines is None or len(lines) < 3:
        return image

    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 == x1:
            continue
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if abs(angle) < 20:
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            angles.append((angle, length))

    if len(angles) < 3:
        return image

    total_weight = sum(l for _, l in angles)
    avg_angle = sum(a * l for a, l in angles) / total_weight

    if abs(avg_angle) < 0.1:
        return image

    print(f"  [O] Hough 정밀 보정: {avg_angle:.2f}도 ({len(angles)}개 선 감지)")
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, avg_angle, 1.0)
    cos = abs(M[0, 0])
    sin = abs(M[0, 1])
    new_w = int(h * sin + w * cos)
    new_h = int(h * cos + w * sin)
    M[0, 2] += (new_w - w) / 2
    M[1, 2] += (new_h - h) / 2
    return cv2.warpAffine(image, M, (new_w, new_h),
                          borderMode=cv2.BORDER_CONSTANT,
                          borderValue=(255, 255, 255))


def detect_text_orientation(image: np.ndarray) -> int:
    """텍스트 방향을 감지하여 필요한 회전 각도(0, 90, 180, 270)를 반환."""
    h, w = image.shape[:2]
    margin_y, margin_x = int(h * 0.2), int(w * 0.2)
    center = image[margin_y:h - margin_y, margin_x:w - margin_x]

    gray = cv2.cvtColor(center, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    best_rotation = 0
    best_score = -1

    for rotation in [0, 90, 180, 270]:
        if rotation == 0:
            rotated = binary
        elif rotation == 90:
            rotated = cv2.rotate(binary, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif rotation == 180:
            rotated = cv2.rotate(binary, cv2.ROTATE_180)
        else:
            rotated = cv2.rotate(binary, cv2.ROTATE_90_CLOCKWISE)

        rh, rw = rotated.shape
        h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        h_lines = cv2.morphologyEx(rotated, cv2.MORPH_OPEN, h_kernel)
        h_total = cv2.countNonZero(h_lines)

        top_half = rotated[:rh // 2, :]
        bot_half = rotated[rh // 2:, :]
        top_density = cv2.countNonZero(top_half)
        bot_density = cv2.countNonZero(bot_half)

        balance = top_density / max(bot_density, 1)
        score = h_total * (1 + min(balance, 3) * 0.3)

        if score > best_score:
            best_score = score
            best_rotation = rotation

    return best_rotation


def ensure_correct_orientation(pil_img: Image.Image) -> Image.Image:
    """텍스트 방향 감지 후 올바른 방향으로 회전."""
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    rotation = detect_text_orientation(cv_img)

    if rotation != 0:
        pil_img = pil_img.rotate(rotation, expand=True)

    w, h = pil_img.size
    if w > h:
        pil_img = pil_img.rotate(90, expand=True)
    return pil_img


def enhance_document(pil_img: Image.Image) -> Image.Image:
    """문서 가독성 향상: 대비, 샤프닝, 밝기 조정."""
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Brightness(pil_img)
    pil_img = enhancer.enhance(1.1)
    pil_img = pil_img.filter(ImageFilter.SHARPEN)
    return pil_img


def auto_crop_content(pil_img: Image.Image, margin: int = 40) -> Image.Image:
    """내용이 있는 영역만 자동 크롭."""
    gray = np.array(pil_img.convert("L"))
    mask = gray < 250
    coords = np.column_stack(np.where(mask))
    if len(coords) < 100:
        return pil_img
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)

    w, h = pil_img.size
    x_min = max(0, x_min - margin)
    y_min = max(0, y_min - margin)
    x_max = min(w, x_max + margin)
    y_max = min(h, y_max + margin)

    return pil_img.crop((x_min, y_min, x_max, y_max))


def fit_to_a4(pil_img: Image.Image, dpi: int = 300) -> Image.Image:
    """이미지를 A4 크기 캔버스에 중앙 배치."""
    a4_w = int(210 / 25.4 * dpi)
    a4_h = int(297 / 25.4 * dpi)

    img_w, img_h = pil_img.size
    scale = min(a4_w / img_w, a4_h / img_h)
    if scale < 1:
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        pil_img = pil_img.resize((new_w, new_h), Image.LANCZOS)
    else:
        new_w, new_h = img_w, img_h

    canvas = Image.new("RGB", (a4_w, a4_h), (255, 255, 255))
    x = (a4_w - new_w) // 2
    y = (a4_h - new_h) // 2
    canvas.paste(pil_img, (x, y))
    return canvas


# ─── 표 구조 감지 ───


def detect_table_structure(image: np.ndarray) -> dict:
    """표의 행/열 경계를 감지하여 구조 정보를 반환."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    h, w = image.shape[:2]

    # 가로선 추출
    h_len = max(40, int(w * 0.05))
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (h_len, 1))
    h_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, h_kernel)

    # 세로선 추출
    v_len = max(40, int(h * 0.02))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, v_len))
    v_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, v_kernel)

    if cv2.countNonZero(h_lines) < 100 or cv2.countNonZero(v_lines) < 100:
        return {"rows": 0, "cols": 0, "detected": False}

    # Y축 프로젝션 -> 가로선 위치
    h_proj = np.sum(h_lines > 0, axis=1).astype(float)
    h_threshold = w * 0.03
    row_positions = _find_peaks(h_proj, h_threshold, min_gap=15)

    # X축 프로젝션 -> 세로선 위치
    v_proj = np.sum(v_lines > 0, axis=0).astype(float)
    v_threshold = h * 0.01
    col_positions = _find_peaks(v_proj, v_threshold, min_gap=15)

    if len(row_positions) < 2 or len(col_positions) < 2:
        return {"rows": 0, "cols": 0, "detected": False}

    n_rows = max(0, len(row_positions) - 1)
    n_cols = max(0, len(col_positions) - 1)

    return {
        "rows": n_rows,
        "cols": n_cols,
        "row_positions": row_positions,
        "col_positions": col_positions,
        "detected": True,
    }


# ─── 직인 추출 ───


def _crop_square(image: np.ndarray, x: int, y: int, cw: int, ch: int,
                  pad: int = 15) -> np.ndarray:
    """바운딩 박스를 정사각형으로 확장 크롭. 도장은 원형이므로 1:1 비율 유지."""
    h, w = image.shape[:2]
    size = max(cw, ch)
    cx = x + cw // 2
    cy = y + ch // 2
    half = size // 2 + pad

    sy1, sy2 = max(0, cy - half), min(h, cy + half)
    sx1, sx2 = max(0, cx - half), min(w, cx + half)
    seal_crop = image[sy1:sy2, sx1:sx2]

    crop_h, crop_w = seal_crop.shape[:2]
    target = max(crop_h, crop_w)
    square = np.full((target, target, 3), 255, dtype=np.uint8)
    y_off = (target - crop_h) // 2
    x_off = (target - crop_w) // 2
    square[y_off:y_off+crop_h, x_off:x_off+crop_w] = seal_crop
    return square


def _find_seal_contours(mask: np.ndarray, img_area: int,
                         min_ratio: float = 0.6, max_ratio: float = 1.6,
                         min_fill: float = 0.15) -> list[tuple]:
    """마스크에서 도장 후보 윤곽을 찾아 (area, x, y, w, h) 리스트 반환."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    for c in contours:
        x, y, cw, ch = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        bbox_area = cw * ch
        ratio = cw / max(ch, 1)
        fill_ratio = area / max(bbox_area, 1)
        # convex hull 기반 solidity 체크 (도장은 컴팩트)
        hull = cv2.convexHull(c)
        hull_area = cv2.contourArea(hull)
        solidity = area / max(hull_area, 1)
        if (min_ratio < ratio < max_ratio
                and bbox_area > img_area * 0.002
                and bbox_area < img_area * 0.12
                and fill_ratio > min_fill
                and solidity > 0.25):
            candidates.append((area, x, y, cw, ch))
    return candidates


def extract_all_seals(image: np.ndarray) -> tuple[str | None, str | None]:
    """이미지 전체에서 도장을 추출. 빨간색/어두운색 각각 독립 탐색.
    가장 큰 것 = 인감(/tmp/scan_main_seal.png), 두 번째 = 직인(/tmp/scan_seal.png).
    반환: (main_seal_path, seal_path)"""
    h, w = image.shape[:2]
    img_area = h * w
    close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))

    # === Pass 1: 빨간색 도장 ===
    b, g, r = cv2.split(image)
    red_pixels = (
        (r.astype(int) > 100)
        & (r.astype(int) > g.astype(int) + 20)
        & (r.astype(int) > b.astype(int) + 20)
    )
    red_mask = red_pixels.astype(np.uint8) * 255
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, close_kernel, iterations=2)
    red_candidates = _find_seal_contours(red_mask, img_area)

    # === Pass 2: 어두운 도장 (텍스트 적극 제거) ===
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, dark_mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    # 다중 스케일 가로 텍스트 제거
    for kw in [w // 4, w // 8, w // 16]:
        if kw > 30:
            h_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (kw, 1))
            text_h = cv2.morphologyEx(dark_mask, cv2.MORPH_OPEN, h_kern)
            # 세로로 약간 팽창하여 텍스트 줄 주변 잔여물도 제거
            dilate_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
            text_h = cv2.dilate(text_h, dilate_v, iterations=1)
            dark_mask = cv2.subtract(dark_mask, text_h)

    # 세로 텍스트 획 제거 (긴 세로선)
    for kh in [h // 8, h // 16]:
        if kh > 30:
            v_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kh))
            text_v = cv2.morphologyEx(dark_mask, cv2.MORPH_OPEN, v_kern)
            dark_mask = cv2.subtract(dark_mask, text_v)

    # 얇은 연결부 끊기 (opening) → 도장 내부 복원 (closing)
    open_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    dark_mask = cv2.morphologyEx(dark_mask, cv2.MORPH_OPEN, open_kernel)
    dark_mask = cv2.morphologyEx(dark_mask, cv2.MORPH_CLOSE, close_kernel, iterations=2)

    dark_candidates = _find_seal_contours(dark_mask, img_area, min_fill=0.20)

    # === 빨간 후보와 겹치는 어두운 후보 제거 ===
    filtered_dark = []
    for dc in dark_candidates:
        _, dx, dy, dw, dh = dc
        dcx, dcy = dx + dw // 2, dy + dh // 2
        overlaps = False
        for rc in red_candidates:
            _, rx, ry, rw, rh = rc
            if rx <= dcx <= rx + rw and ry <= dcy <= ry + rh:
                overlaps = True
                break
        if not overlaps:
            filtered_dark.append(dc)

    # === 크기순 병합 ===
    all_candidates = red_candidates + filtered_dark
    if not all_candidates:
        return None, None

    all_candidates.sort(key=lambda t: t[0], reverse=True)

    main_seal_path = None
    seal_path = None

    # 인감 (가장 큰 도장)
    area, x, y, cw, ch = all_candidates[0]
    square = _crop_square(image, x, y, cw, ch, pad=20)
    pil = Image.fromarray(cv2.cvtColor(square, cv2.COLOR_BGR2RGB))
    main_seal_path = "/tmp/scan_main_seal.png"
    pil.save(main_seal_path, dpi=(300, 300))
    print(f"  [O] 인감 추출: {main_seal_path} ({square.shape[0]}x{square.shape[1]}px)")

    # 직인 (두 번째로 큰 도장)
    if len(all_candidates) >= 2:
        area2, x2, y2, cw2, ch2 = all_candidates[1]
        square2 = _crop_square(image, x2, y2, cw2, ch2, pad=15)
        pil2 = Image.fromarray(cv2.cvtColor(square2, cv2.COLOR_BGR2RGB))
        seal_path = "/tmp/scan_seal.png"
        pil2.save(seal_path, dpi=(300, 300))
        print(f"  [O] 직인 추출: {seal_path} ({square2.shape[0]}x{square2.shape[1]}px)")

    return main_seal_path, seal_path


# ─── 이미지 기반 표 선 재생성 (기존 모드용) ───


def redraw_table_lines(image: np.ndarray) -> np.ndarray:
    """표의 선을 감지 -> 지우고 -> 완벽한 직선으로 다시 그림."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    h, w = image.shape[:2]

    h_len = max(40, int(w * 0.05))
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (h_len, 1))
    h_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, h_kernel)

    v_len = max(40, int(h * 0.02))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, v_len))
    v_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, v_kernel)

    if cv2.countNonZero(h_lines) < 100 or cv2.countNonZero(v_lines) < 100:
        return image

    h_proj = np.sum(h_lines > 0, axis=1).astype(float)
    h_threshold = w * 0.03
    row_positions = _find_peaks(h_proj, h_threshold, min_gap=15)

    v_proj = np.sum(v_lines > 0, axis=0).astype(float)
    v_threshold = h * 0.01
    col_positions = _find_peaks(v_proj, v_threshold, min_gap=15)

    if len(row_positions) < 2 or len(col_positions) < 2:
        return image

    y_min, y_max = row_positions[0], row_positions[-1]
    x_min, x_max = col_positions[0], col_positions[-1]

    # 짧은 커널로 물결치는 선 조각까지 포착
    h_len2 = max(15, int(w * 0.015))
    h_kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (h_len2, 1))
    h_lines_short = cv2.morphologyEx(binary, cv2.MORPH_OPEN, h_kernel2)

    v_len2 = max(15, int(h * 0.008))
    v_kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, v_len2))
    v_lines_short = cv2.morphologyEx(binary, cv2.MORPH_OPEN, v_kernel2)

    zone = 25
    h_filtered = np.zeros_like(h_lines_short)
    for y in row_positions:
        y_lo, y_hi = max(0, y - zone), min(h, y + zone)
        h_filtered[y_lo:y_hi, x_min:x_max] = h_lines_short[y_lo:y_hi, x_min:x_max]

    v_filtered = np.zeros_like(v_lines_short)
    for x in col_positions:
        x_lo, x_hi = max(0, x - zone), min(w, x + zone)
        v_filtered[y_min:y_max, x_lo:x_hi] = v_lines_short[y_min:y_max, x_lo:x_hi]

    all_detected = cv2.bitwise_or(
        cv2.bitwise_or(h_lines, v_lines),
        cv2.bitwise_or(h_filtered, v_filtered),
    )
    erase_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    erase_mask = cv2.dilate(all_detected, erase_kernel, iterations=2)
    image[erase_mask > 0] = [255, 255, 255]

    thicknesses = []
    for y_pos in row_positions:
        y_lo, y_hi = max(0, y_pos - 10), min(h, y_pos + 10)
        strip = h_lines[y_lo:y_hi, :]
        col_sums = np.sum(strip > 0, axis=0)
        valid = col_sums[col_sums > 0]
        if len(valid) > 0:
            thicknesses.extend(valid[:50].tolist())
    line_thickness = max(2, int(np.median(thicknesses))) if thicknesses else 2

    for y in row_positions:
        cv2.line(image, (x_min, y), (x_max, y), (0, 0, 0), line_thickness)
    for x in col_positions:
        cv2.line(image, (x, y_min), (x, y_max), (0, 0, 0), line_thickness)

    n_lines = len(row_positions) + len(col_positions)
    print(f"  [O] 표 선 재생성: {len(row_positions)}행 x {len(col_positions)}열 경계, "
          f"{line_thickness}px ({n_lines}개 직선)")
    return image


# ─── PDF 생성 (reportlab) ───


def generate_pdf_from_data(data: dict, output_path: str):
    """JSON 데이터로 깨끗한 PDF 생성."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Image as RLImage

    pdfmetrics.registerFont(TTFont('Korean', '/System/Library/Fonts/Supplemental/AppleGothic.ttf'))

    style_title = ParagraphStyle(
        'Title', fontName='Korean', fontSize=20, alignment=TA_CENTER,
        spaceBefore=15 * mm, spaceAfter=8 * mm, leading=28,
    )
    style_cell = ParagraphStyle(
        'Cell', fontName='Korean', fontSize=10, alignment=TA_CENTER, leading=14,
    )
    style_body = ParagraphStyle(
        'Body', fontName='Korean', fontSize=10, leading=16,
    )
    style_body_center = ParagraphStyle(
        'BodyCenter', fontName='Korean', fontSize=10, alignment=TA_CENTER, leading=16,
    )
    style_company = ParagraphStyle(
        'Company', fontName='Korean', fontSize=10, leading=16,
    )

    def make_cells(row_data):
        return [Paragraph(c.replace('\n', '<br/>'), style_cell) for c in row_data]

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=25 * mm, bottomMargin=20 * mm,
    )
    elements = []

    # Title
    if data.get('title'):
        elements.append(Paragraph(data['title'], style_title))

    # Subtitle (e.g. 법인등록번호)
    if data.get('subtitle'):
        style_subtitle = ParagraphStyle(
            'Subtitle', fontName='Korean', fontSize=10, alignment=TA_CENTER, leading=14,
        )
        elements.append(Paragraph(data['subtitle'], style_subtitle))
        elements.append(Spacer(1, 4 * mm))

    # Body lines → label:value 표 형태 정렬 (원본 구조)
    main_seal_path = data.get('main_seal_path', '/tmp/scan_main_seal.png')
    has_main_seal = main_seal_path and os.path.exists(main_seal_path)

    if data.get('body_lines'):
        label_value_rows = []
        plain_lines = []
        for line in data['body_lines']:
            if isinstance(line, dict):
                label_value_rows.append(line)
            else:
                plain_lines.append(line)

        # label:value 쌍 → 2열 테이블 (라벨 고정폭, 값 나머지)
        if label_value_rows:
            lv_data = []
            for lv in label_value_rows:
                lv_data.append([
                    Paragraph(lv['label'], style_body),
                    Paragraph(': ' + lv['value'], style_body),
                ])
            lv_table = Table(lv_data, colWidths=[32 * mm, doc.width - 32 * mm])
            lv_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            elements.append(lv_table)

        # 나머지 일반 텍스트 (번호, 이름 등) → 중앙 정렬
        if plain_lines:
            elements.append(Spacer(1, 3 * mm))
            for pl in plain_lines:
                elements.append(Paragraph(pl, style_body_center))

    # Main seal → 테두리 박스 안에 단독 중앙 배치 (원본 구조)
    if has_main_seal:
        seal_size = data.get('main_seal_size_mm', 35) * mm
        seal_img = RLImage(main_seal_path, width=seal_size, height=seal_size)
        elements.append(Spacer(1, 6 * mm))
        seal_table = Table(
            [[seal_img]],
            colWidths=[seal_size + 12 * mm],
            rowHeights=[seal_size + 12 * mm],
        )
        seal_table.setStyle(TableStyle([
            ('BOX', (0, 0), (0, 0), 0.8, colors.black),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
        ]))
        seal_table.hAlign = 'CENTER'
        elements.append(seal_table)
        elements.append(Spacer(1, 6 * mm))

    # Table (body_lines 없을 때만 - 표 기반 문서용)
    if not data.get('body_lines'):
        table_data = []
        if data.get('header'):
            table_data.append(make_cells(data['header']))
        for row in data.get('rows', []):
            table_data.append(make_cells(row))

        if table_data:
            n_cols = len(table_data[0])
            if n_cols == 2:
                col_widths = [35 * mm, doc.width - 35 * mm]
            elif n_cols <= 7:
                col_widths_mm = [10, 30, 28, 22, 25, 27, 18][:n_cols]
                col_widths = [w * mm for w in col_widths_mm]
            else:
                col_widths = [doc.width / n_cols] * n_cols

            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            style_cmds = [
                ('GRID', (0, 0), (-1, -1), 0.8, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.95, 0.95, 0.95)),
                ('FONTNAME', (0, 0), (-1, -1), 'Korean'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ]
            if data.get('rows') and any('총' in cell for cell in data['rows'][-1]):
                style_cmds.append(('SPAN', (1, len(table_data) - 1), (3, len(table_data) - 1)))
            table.setStyle(TableStyle(style_cmds))
            elements.append(table)

    # Footer text
    if data.get('footer_text'):
        elements.append(Spacer(1, 8 * mm))
        elements.append(Paragraph(data['footer_text'].replace('\n', '<br/>'), style_body_center))

    # Date
    if data.get('date'):
        elements.append(Spacer(1, 8 * mm))
        elements.append(Paragraph(data['date'], style_body_center))

    # Company info + seal
    if data.get('company_info'):
        elements.append(Spacer(1, 10 * mm))
        seal_path = data.get('seal_path', '/tmp/scan_seal.png')
        has_seal = seal_path and os.path.exists(seal_path)

        info_rows = []
        for i, info in enumerate(data['company_info']):
            row = [
                Paragraph(info['label'], style_company),
                Paragraph(info['value'], style_company),
            ]
            if i == 0 and has_seal:
                row.append(RLImage(seal_path, width=18 * mm, height=18 * mm))
            else:
                row.append('')
            info_rows.append(row)

        info_table = Table(info_rows, colWidths=[22 * mm, 58 * mm, 22 * mm])
        info_style = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]
        if has_seal and len(info_rows) > 1:
            info_style.append(('SPAN', (2, 0), (2, len(info_rows) - 1)))
        info_table.setStyle(TableStyle(info_style))

        outer = Table([[None, info_table]], colWidths=[doc.width - 102 * mm, 102 * mm])
        outer.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
        elements.append(outer)

    # Footer notes (하단 안내 단락 - 구분선 포함)
    if data.get('footer_notes'):
        style_note = ParagraphStyle(
            'Note', fontName='Korean', fontSize=8, leading=11,
        )
        elements.append(Spacer(1, 6 * mm))
        from reportlab.platypus import HRFlowable
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.black))
        for note in data['footer_notes']:
            elements.append(Spacer(1, 2 * mm))
            elements.append(Paragraph(note.replace('\n', '<br/>'), style_note))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.black))

    # Issuance info (발급번호, 페이지 등 - 우측 정렬)
    if data.get('issuance_info'):
        style_issue = ParagraphStyle(
            'Issue', fontName='Korean', fontSize=8, alignment=TA_CENTER, leading=12,
        )
        elements.append(Spacer(1, 6 * mm))
        for info in data['issuance_info']:
            elements.append(Paragraph(info, style_issue))

    doc.build(elements)
    print(f"PDF 생성 완료: {output_path}")


# ─── 이미지 기반 처리 파이프라인 (기존 모드) ───


def process_image(
    input_path: str,
    do_perspective: bool = True,
    do_enhance: bool = True,
    dpi: int = 300,
) -> Image.Image:
    """단일 이미지 처리 파이프라인 (기존 이미지 기반 모드)."""
    pil_raw = Image.open(input_path)
    pil_raw = apply_exif_orientation(pil_raw)
    pil_raw = pil_raw.convert("RGB")
    image = cv2.cvtColor(np.array(pil_raw), cv2.COLOR_RGB2BGR)

    print(f"  이미지 크기: {image.shape[1]}x{image.shape[0]}")

    if do_perspective:
        pts = find_document_contour(image)
        if pts is not None:
            contour_area = cv2.contourArea(pts.astype(np.float32))
            img_area = image.shape[0] * image.shape[1]
            area_ratio = contour_area / img_area
        else:
            area_ratio = 0

        if pts is not None and area_ratio > 0.4:
            pts_expanded = expand_points(pts, image.shape, margin_pct=0.02)
            image = perspective_transform(image, pts_expanded)
            print(f"  [O] 원근 보정 (canny, {area_ratio*100:.0f}%): {Path(input_path).name}")
        elif pts is not None:
            angle = get_rotation_angle_from_contour(pts)
            if abs(angle) > 0.5:
                image = rotate_full_image(image, angle)
                print(f"  [O] 회전 보정 {angle:.1f}도: {Path(input_path).name}")
            else:
                print(f"  [-] 회전 불필요 ({angle:.1f}도): {Path(input_path).name}")
        else:
            print(f"  [-] 문서 윤곽 미감지, 보정 건너뜀: {Path(input_path).name}")

    image = deskew(image)
    image = extract_document_colors(image)
    image = hough_deskew(image)
    image = redraw_table_lines(image)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    pil_img = ensure_correct_orientation(pil_img)
    pil_img = auto_crop_content(pil_img, margin=60)

    if do_enhance:
        pil_img = enhance_document(pil_img)

    pil_img = fit_to_a4(pil_img, dpi=dpi)
    return pil_img


def images_to_pdf(images: list[Image.Image], output_path: str, dpi: int = 300):
    """PIL 이미지 리스트를 단일 PDF로 합침."""
    tmp_files = []
    try:
        for i, img in enumerate(images):
            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            img.save(tmp.name, "JPEG", quality=95, dpi=(dpi, dpi))
            tmp_files.append(tmp.name)

        layout = img2pdf.get_layout_fun((img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297)))
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(tmp_files, layout_fun=layout))
    finally:
        for tmp in tmp_files:
            os.unlink(tmp)


# ─── 전처리 모드 ───


def _try_find_and_transform(image: np.ndarray) -> tuple[np.ndarray, bool]:
    """문서 윤곽 감지 → 원근/회전 보정 시도. (보정된 이미지, 성공 여부) 반환."""
    pts = find_document_contour(image)
    if pts is None:
        return image, False

    h, w = image.shape[:2]
    contour_area = cv2.contourArea(pts.astype(np.float32))
    area_ratio = contour_area / (h * w)

    if area_ratio > 0.4:
        pts_expanded = expand_points(pts, image.shape, margin_pct=0.02)
        image = perspective_transform(image, pts_expanded)
        print(f"  [O] 원근 보정 ({area_ratio*100:.0f}%)")
        return image, True

    angle = get_rotation_angle_from_contour(pts)
    if abs(angle) > 0.5:
        image = rotate_full_image(image, angle)
        print(f"  [O] 회전 보정 {angle:.1f}도")
        return image, True

    return image, False


def preprocess_image(input_path: str):
    """이미지 전처리: 보정 + 표 구조 감지 + 직인 추출."""
    pil_raw = Image.open(input_path)
    pil_raw = apply_exif_orientation(pil_raw)
    pil_raw = pil_raw.convert("RGB")
    image = cv2.cvtColor(np.array(pil_raw), cv2.COLOR_RGB2BGR)

    h, w = image.shape[:2]
    print(f"원본 이미지 크기: {w}x{h}")

    # 1차: 문서 윤곽 감지 + 보정
    image, found = _try_find_and_transform(image)

    if not found:
        # 텍스트 방향 감지 → 회전 후 재시도
        rotation = detect_text_orientation(image)
        if rotation != 0:
            print(f"  [O] 텍스트 방향 보정 {rotation}도")
            if rotation == 90:
                image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif rotation == 180:
                image = cv2.rotate(image, cv2.ROTATE_180)
            elif rotation == 270:
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            image, found = _try_find_and_transform(image)

        # 가로 이미지면 세로로 회전
        rh, rw = image.shape[:2]
        if rw > rh:
            print("  [O] 가로→세로 회전")
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            if not found:
                image, found = _try_find_and_transform(image)

        if not found:
            print("  [-] 문서 윤곽 미감지 (fallback 모드)")

    # deskew
    image = deskew(image)

    if found:
        # 문서 영역이 확보된 경우만 색상 필터링 + Hough 적용
        image = extract_document_colors(image)
        image = hough_deskew(image)
    else:
        # 윤곽 미감지: 색상 필터링/Hough 건너뜀 (배경 포함 이미지에선 파괴적)
        # Claude 비전이 원본에서 직접 읽는 것이 더 정확
        print("  [-] 배경 포함 → 색상 필터링/Hough 건너뜀")

    # 전처리 결과 저장
    preprocessed_path = "/tmp/scan_preprocessed.png"
    pil_result = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    pil_result = ensure_correct_orientation(pil_result)
    pil_result = auto_crop_content(pil_result, margin=60)

    # 다시 cv2로 변환하여 표 구조 감지 + 직인 추출
    image_final = cv2.cvtColor(np.array(pil_result), cv2.COLOR_RGB2BGR)
    pil_result.save(preprocessed_path)
    print(f"\n전처리 이미지 저장: {preprocessed_path}")

    h2, w2 = image_final.shape[:2]
    print(f"전처리 이미지 크기: {w2}x{h2}")

    # 표 구조 감지
    table_info = detect_table_structure(image_final)
    if table_info["detected"]:
        print(f"표 구조 감지: {table_info['rows']}행 x {table_info['cols']}열")
    else:
        print("표 구조 미감지")

    # 도장 추출 (전체 이미지에서 크기순: 인감 > 직인)
    main_seal_path, seal_path = extract_all_seals(image_final)
    if not main_seal_path:
        print("인감 미감지")
    if not seal_path:
        print("직인 미감지")

    print("\n=== 전처리 완료 ===")
    print(f"  전처리 이미지: {preprocessed_path}")
    if main_seal_path:
        print(f"  인감 이미지: {main_seal_path}")
    if seal_path:
        print(f"  직인 이미지: {seal_path}")
    print("\n다음 단계: Read 도구로 전처리 이미지를 열어 모든 텍스트를 빠짐없이 읽고 JSON으로 저장하세요.")
    print("주의: 하단 안내문(모든 번호 단락), 발급번호, 페이지번호까지 반드시 포함.")


# ─── main ───


def main():
    parser = argparse.ArgumentParser(
        description="서류 사진에서 텍스트를 파싱하여 완벽한 PDF를 새로 생성"
    )

    # 모드 선택
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--preprocess", metavar="IMAGE",
                            help="전처리 모드: 이미지 보정 + 표 구조 감지 + 직인 추출")
    mode_group.add_argument("--generate", metavar="JSON",
                            help="PDF 생성 모드: JSON 데이터로 reportlab PDF 생성")

    # 기존 모드 (하위 호환)
    parser.add_argument("inputs", nargs="*", help="입력 이미지 파일(들) - 기존 이미지 기반 모드")
    parser.add_argument("-o", "--output", help="출력 PDF 경로")
    parser.add_argument("--dpi", type=int, default=300, help="출력 DPI (기본: 300)")
    parser.add_argument("--no-perspective", action="store_true", help="원근 보정 건너뛰기")
    parser.add_argument("--no-enhance", action="store_true", help="화질 개선 건너뛰기")

    args = parser.parse_args()

    # 모드 1: 전처리
    if args.preprocess:
        preprocess_image(args.preprocess)
        return

    # 모드 2: PDF 생성
    if args.generate:
        if not args.output:
            args.output = str(Path(args.generate).with_suffix(".pdf"))
        with open(args.generate, "r", encoding="utf-8") as f:
            data = json.load(f)
        generate_pdf_from_data(data, args.output)
        return

    # 기존 모드: 이미지 기반 PDF
    if not args.inputs:
        parser.print_help()
        return

    if args.output:
        output_path = args.output
    else:
        base = Path(args.inputs[0]).stem
        output_path = str(Path(args.inputs[0]).parent / f"{base}_scanned.pdf")

    print(f"처리할 파일: {len(args.inputs)}개")
    print(f"출력: {output_path}")
    print()

    processed = []
    for path in args.inputs:
        print(f"처리 중: {path}")
        img = process_image(
            path,
            do_perspective=not args.no_perspective,
            do_enhance=not args.no_enhance,
            dpi=args.dpi,
        )
        processed.append(img)

    images_to_pdf(processed, output_path, dpi=args.dpi)
    print(f"\n완료: {output_path}")


if __name__ == "__main__":
    main()
