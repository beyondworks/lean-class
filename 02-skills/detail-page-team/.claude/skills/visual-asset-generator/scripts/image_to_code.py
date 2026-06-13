#!/usr/bin/env python3
"""
Image to Code Converter
이미지를 base64로 인코딩하여 HTML/CSS 코드로 변환

사용법:
    python image_to_code.py --input image.png --format html --output code.html
"""

import argparse
import base64
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from PIL import Image
except ImportError:
    print("Pillow를 설치해주세요: pip install Pillow")
    raise


class ImageToCodeConverter:
    """이미지를 HTML/CSS 코드로 변환하는 클래스"""
    
    # 파일 크기 경고 임계값 (500KB)
    SIZE_WARNING_THRESHOLD = 500 * 1024
    
    def __init__(self, optimize: bool = True, max_size: Tuple[int, int] = None):
        """
        Args:
            optimize: 이미지 최적화 여부
            max_size: 최대 크기 제한 (width, height)
        """
        self.optimize = optimize
        self.max_size = max_size
    
    def image_to_base64(
        self,
        image_path: str,
        quality: int = 85,
        format: str = None
    ) -> Tuple[str, str, int, int]:
        """
        이미지를 base64로 인코딩
        
        Args:
            image_path: 이미지 파일 경로
            quality: JPEG 품질 (1-100)
            format: 출력 포맷 (png, jpeg, webp). None이면 자동
        
        Returns:
            (base64_string, mime_type, width, height)
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {image_path}")
        
        with Image.open(image_path) as img:
            width, height = img.size
            
            # 크기 제한 적용
            if self.max_size:
                img = self._resize_if_needed(img, self.max_size)
                width, height = img.size
            
            # 포맷 결정
            if format is None:
                format = image_path.suffix.lower().replace('.', '')
                if format not in ['png', 'jpeg', 'jpg', 'webp']:
                    format = 'png'
            
            format = format.replace('jpg', 'jpeg')
            
            # RGBA 이미지 처리
            if format == 'jpeg' and img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode not in ['RGB', 'RGBA', 'L']:
                img = img.convert('RGB')
            
            # base64 인코딩
            from io import BytesIO
            buffer = BytesIO()
            
            if format == 'jpeg':
                img.save(buffer, 'JPEG', quality=quality, optimize=self.optimize)
                mime_type = 'image/jpeg'
            elif format == 'webp':
                img.save(buffer, 'WEBP', quality=quality, optimize=self.optimize)
                mime_type = 'image/webp'
            else:
                img.save(buffer, 'PNG', optimize=self.optimize)
                mime_type = 'image/png'
            
            buffer.seek(0)
            b64_string = base64.b64encode(buffer.read()).decode('utf-8')
            
            # 크기 경고
            encoded_size = len(b64_string)
            if encoded_size > self.SIZE_WARNING_THRESHOLD:
                print(f"⚠️ 경고: 인코딩된 크기가 큽니다 ({encoded_size / 1024:.1f}KB)")
                print("   품질을 낮추거나 이미지 크기를 줄이는 것을 권장합니다.")
            
            return b64_string, mime_type, width, height
    
    def to_html_img(
        self,
        image_path: str,
        alt: str = "",
        css_class: str = "",
        css_id: str = "",
        inline_style: str = "",
        quality: int = 85
    ) -> str:
        """
        이미지를 <img> 태그로 변환
        
        Args:
            image_path: 이미지 파일 경로
            alt: alt 텍스트
            css_class: CSS 클래스
            css_id: CSS ID
            inline_style: 인라인 스타일
            quality: JPEG 품질
        
        Returns:
            HTML <img> 태그 문자열
        """
        b64, mime, width, height = self.image_to_base64(image_path, quality)
        
        attrs = [f'src="data:{mime};base64,{b64}"']
        attrs.append(f'alt="{alt}"')
        attrs.append(f'width="{width}"')
        attrs.append(f'height="{height}"')
        
        if css_class:
            attrs.append(f'class="{css_class}"')
        if css_id:
            attrs.append(f'id="{css_id}"')
        if inline_style:
            attrs.append(f'style="{inline_style}"')
        
        return f'<img {" ".join(attrs)}>'
    
    def to_html_div(
        self,
        image_path: str,
        css_class: str = "",
        css_id: str = "",
        width: str = "100%",
        height: str = "auto",
        quality: int = 85
    ) -> str:
        """
        이미지를 background-image가 있는 <div>로 변환
        
        Args:
            image_path: 이미지 파일 경로
            css_class: CSS 클래스
            css_id: CSS ID
            width: div 너비
            height: div 높이
            quality: JPEG 품질
        
        Returns:
            HTML <div> 태그 문자열
        """
        b64, mime, img_width, img_height = self.image_to_base64(image_path, quality)
        
        style = f"background-image: url('data:{mime};base64,{b64}');"
        style += f" width: {width}; height: {height};"
        style += " background-size: cover; background-position: center;"
        
        attrs = [f'style="{style}"']
        if css_class:
            attrs.append(f'class="{css_class}"')
        if css_id:
            attrs.append(f'id="{css_id}"')
        
        return f'<div {" ".join(attrs)}></div>'
    
    def to_css_background(
        self,
        image_path: str,
        selector: str,
        quality: int = 85
    ) -> str:
        """
        이미지를 CSS background 규칙으로 변환
        
        Args:
            image_path: 이미지 파일 경로
            selector: CSS 선택자
            quality: JPEG 품질
        
        Returns:
            CSS 규칙 문자열
        """
        b64, mime, width, height = self.image_to_base64(image_path, quality)
        
        css = f"""{selector} {{
  background-image: url('data:{mime};base64,{b64}');
  background-size: cover;
  background-position: center;
  width: {width}px;
  height: {height}px;
}}"""
        return css
    
    def to_json(
        self,
        image_path: str,
        quality: int = 85
    ) -> Dict:
        """
        이미지를 JSON 형식으로 변환
        
        Returns:
            {base64, mimeType, width, height, fileSize} 딕셔너리
        """
        b64, mime, width, height = self.image_to_base64(image_path, quality)
        
        return {
            'base64': b64,
            'mimeType': mime,
            'width': width,
            'height': height,
            'fileSize': len(b64),
            'dataUri': f'data:{mime};base64,{b64}'
        }
    
    def batch_to_html(
        self,
        image_paths: List[str],
        wrapper_class: str = "image-gallery",
        item_class: str = "gallery-item",
        quality: int = 85
    ) -> str:
        """
        여러 이미지를 HTML로 일괄 변환
        
        Args:
            image_paths: 이미지 파일 경로 리스트
            wrapper_class: 래퍼 div 클래스
            item_class: 각 이미지 클래스
            quality: JPEG 품질
        
        Returns:
            HTML 문자열
        """
        items = []
        for path in image_paths:
            img_html = self.to_html_img(
                path, 
                alt=Path(path).stem,
                css_class=item_class,
                quality=quality
            )
            items.append(f'  {img_html}')
        
        return f'<div class="{wrapper_class}">\n' + '\n'.join(items) + '\n</div>'
    
    def _resize_if_needed(self, img: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
        """필요시 이미지 리사이징"""
        max_width, max_height = max_size
        width, height = img.size
        
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_size = (int(width * ratio), int(height * ratio))
            return img.resize(new_size, Image.Resampling.LANCZOS)
        
        return img


def main():
    parser = argparse.ArgumentParser(
        description='이미지를 base64 HTML/CSS 코드로 변환'
    )
    parser.add_argument('--input', '-i', required=True, help='입력 이미지 경로')
    parser.add_argument('--format', '-f', default='html',
                       choices=['html', 'html-div', 'css', 'json'],
                       help='출력 형식')
    parser.add_argument('--output', '-o', help='출력 파일 경로 (생략시 stdout)')
    parser.add_argument('--alt', default='', help='alt 텍스트')
    parser.add_argument('--class', dest='css_class', default='', help='CSS 클래스')
    parser.add_argument('--id', dest='css_id', default='', help='CSS ID')
    parser.add_argument('--selector', default='.bg-image', help='CSS 선택자 (css 형식용)')
    parser.add_argument('--quality', type=int, default=85, help='JPEG 품질 (1-100)')
    parser.add_argument('--max-width', type=int, help='최대 너비')
    parser.add_argument('--max-height', type=int, help='최대 높이')
    
    args = parser.parse_args()
    
    # 최대 크기 설정
    max_size = None
    if args.max_width and args.max_height:
        max_size = (args.max_width, args.max_height)
    
    converter = ImageToCodeConverter(optimize=True, max_size=max_size)
    
    # 형식별 변환
    if args.format == 'html':
        result = converter.to_html_img(
            args.input,
            alt=args.alt,
            css_class=args.css_class,
            css_id=args.css_id,
            quality=args.quality
        )
    elif args.format == 'html-div':
        result = converter.to_html_div(
            args.input,
            css_class=args.css_class,
            css_id=args.css_id,
            quality=args.quality
        )
    elif args.format == 'css':
        result = converter.to_css_background(
            args.input,
            selector=args.selector,
            quality=args.quality
        )
    elif args.format == 'json':
        data = converter.to_json(args.input, quality=args.quality)
        result = json.dumps(data, indent=2, ensure_ascii=False)
    
    # 출력
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding='utf-8')
        print(f"✅ 저장됨: {args.output}")
    else:
        print(result)


if __name__ == '__main__':
    main()
