#!/usr/bin/env python3
"""
Gemini API Image Generator (나노바나나 3.0 Pro)
상세페이지용 비주얼 에셋 자동 생성

사용법:
    python generate_image.py --prompt "프롬프트" --size 860x500 --output output.png
"""

import argparse
import os
import base64
from pathlib import Path
from io import BytesIO
from typing import Tuple, Optional

try:
    import google.generativeai as genai
    from PIL import Image
    from dotenv import load_dotenv
except ImportError as e:
    print(f"필수 패키지를 설치해주세요: pip install google-generativeai Pillow python-dotenv")
    raise e

# 환경 변수 로드
load_dotenv()


class GeminiImageGenerator:
    """Gemini API를 사용한 이미지 생성기"""
    
    # 플랫폼별 이미지 크기 프리셋
    PLATFORM_SIZES = {
        'coupang': {
            'hero': (860, 500),
            'section': (860, 300),
            'product': (800, 800),
            'icon': (120, 120),
        },
        'smartstore': {
            'hero': (860, 500),
            'section': (860, 300),
            'product': (800, 800),
            'icon': (120, 120),
        },
        'kurly': {
            'hero': (1010, 600),
            'section': (1010, 300),
            'product': (800, 800),
            'icon': (120, 120),
        },
        'cafe24': {
            'hero': (1200, 600),
            'section': (1200, 300),
            'product': (800, 800),
            'icon': (120, 120),
        },
    }
    
    def __init__(self, api_key: str = None):
        """
        Args:
            api_key: Gemini API 키. None이면 환경변수에서 로드
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY가 설정되지 않았습니다.\n"
                "환경변수 또는 .env 파일에 설정해주세요."
            )
        
        genai.configure(api_key=self.api_key)
        
        # Gemini 2.0 Flash (이미지 생성 지원 모델)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate(
        self,
        prompt: str,
        size: Tuple[int, int] = (860, 500),
        style: str = "photorealistic",
        output_path: str = None,
        optimize: bool = True,
        quality: int = 85
    ) -> Image.Image:
        """
        프롬프트로 이미지 생성
        
        Args:
            prompt: 이미지 생성 프롬프트 (영문 권장)
            size: (width, height) 튜플
            style: 스타일 (photorealistic, illustration, 3d-render)
            output_path: 저장 경로 (None이면 저장 안함)
            optimize: 웹 최적화 여부
            quality: JPEG 품질 (1-100)
        
        Returns:
            PIL Image 객체
        """
        # 스타일 접미사 추가
        style_suffix = {
            'photorealistic': ', professional photography, high quality, detailed',
            'illustration': ', digital illustration, clean vector style',
            '3d-render': ', 3D rendered, smooth surfaces, studio lighting',
            'flat-icon': ', flat design icon, simple shapes, bold colors',
        }
        
        enhanced_prompt = prompt + style_suffix.get(style, '')
        
        # 크기 요구사항 추가
        width, height = size
        enhanced_prompt += f", aspect ratio {width}:{height}"
        
        try:
            # Gemini API 호출 (이미지 생성)
            response = self.model.generate_content(
                enhanced_prompt,
                generation_config={
                    "response_mime_type": "image/png",
                }
            )
            
            # 응답에서 이미지 추출
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        image_data = base64.b64decode(part.inline_data.data)
                        image = Image.open(BytesIO(image_data))
                        break
                else:
                    raise ValueError("응답에 이미지가 없습니다")
            else:
                raise ValueError("유효한 응답을 받지 못했습니다")
            
        except Exception as e:
            print(f"Gemini API 오류: {e}")
            print("플레이스홀더 이미지를 생성합니다...")
            image = self._create_placeholder(size, prompt)
        
        # 크기 조정
        if image.size != size:
            image = self._resize_image(image, size)
        
        # 최적화
        if optimize:
            image = self._optimize_image(image, quality)
        
        # 저장
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if output_path.suffix.lower() in ['.jpg', '.jpeg']:
                image.convert('RGB').save(output_path, 'JPEG', quality=quality, optimize=True)
            else:
                image.save(output_path, 'PNG', optimize=True)
            
            print(f"✅ 이미지 저장: {output_path}")
        
        return image
    
    def generate_for_platform(
        self,
        prompt: str,
        platform: str,
        asset_type: str,
        output_path: str = None,
        **kwargs
    ) -> Image.Image:
        """
        플랫폼별 프리셋 크기로 이미지 생성
        
        Args:
            prompt: 이미지 프롬프트
            platform: coupang, smartstore, kurly, cafe24
            asset_type: hero, section, product, icon
            output_path: 저장 경로
        """
        if platform not in self.PLATFORM_SIZES:
            raise ValueError(f"지원하지 않는 플랫폼: {platform}")
        
        if asset_type not in self.PLATFORM_SIZES[platform]:
            raise ValueError(f"지원하지 않는 에셋 타입: {asset_type}")
        
        size = self.PLATFORM_SIZES[platform][asset_type]
        
        # 에셋 타입별 기본 스타일
        default_styles = {
            'hero': 'photorealistic',
            'section': 'photorealistic',
            'product': 'photorealistic',
            'icon': 'flat-icon',
        }
        
        style = kwargs.get('style', default_styles.get(asset_type, 'photorealistic'))
        
        return self.generate(
            prompt=prompt,
            size=size,
            style=style,
            output_path=output_path,
            **kwargs
        )
    
    def _resize_image(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """이미지 리사이징 (비율 유지 + 크롭)"""
        target_width, target_height = size
        target_ratio = target_width / target_height
        
        img_width, img_height = image.size
        img_ratio = img_width / img_height
        
        if img_ratio > target_ratio:
            # 이미지가 더 넓음 - 높이 맞추고 좌우 크롭
            new_height = target_height
            new_width = int(img_width * (target_height / img_height))
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            left = (new_width - target_width) // 2
            image = image.crop((left, 0, left + target_width, target_height))
        else:
            # 이미지가 더 높음 - 너비 맞추고 상하 크롭
            new_width = target_width
            new_height = int(img_height * (target_width / img_width))
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            top = (new_height - target_height) // 2
            image = image.crop((0, top, target_width, top + target_height))
        
        return image
    
    def _optimize_image(self, image: Image.Image, quality: int = 85) -> Image.Image:
        """웹 최적화"""
        # RGBA를 RGB로 변환 (투명도 제거)
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    
    def _create_placeholder(self, size: Tuple[int, int], prompt: str) -> Image.Image:
        """API 실패 시 플레이스홀더 이미지 생성"""
        from PIL import ImageDraw, ImageFont
        
        width, height = size
        
        # 그라데이션 배경
        image = Image.new('RGB', size, '#f0f0f0')
        draw = ImageDraw.Draw(image)
        
        # 테두리
        draw.rectangle(
            [(0, 0), (width-1, height-1)],
            outline='#cccccc',
            width=2
        )
        
        # 텍스트
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except:
            font = ImageFont.load_default()
        
        text = f"[Placeholder]\n{width}x{height}\n\n{prompt[:50]}..."
        
        # 텍스트 중앙 정렬
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill='#666666', font=font)
        
        return image


def parse_size(size_str: str) -> Tuple[int, int]:
    """크기 문자열 파싱 (예: '860x500')"""
    parts = size_str.lower().split('x')
    if len(parts) != 2:
        raise ValueError(f"잘못된 크기 형식: {size_str}")
    return int(parts[0]), int(parts[1])


def main():
    parser = argparse.ArgumentParser(
        description='Gemini API를 사용해 이미지 생성'
    )
    parser.add_argument('--prompt', '-p', required=True, help='이미지 생성 프롬프트')
    parser.add_argument('--size', '-s', default='860x500', help='이미지 크기 (예: 860x500)')
    parser.add_argument('--platform', help='플랫폼 (coupang, smartstore, kurly, cafe24)')
    parser.add_argument('--type', dest='asset_type', help='에셋 타입 (hero, section, product, icon)')
    parser.add_argument('--style', default='photorealistic', 
                       choices=['photorealistic', 'illustration', '3d-render', 'flat-icon'])
    parser.add_argument('--output', '-o', required=True, help='출력 파일 경로')
    parser.add_argument('--quality', type=int, default=85, help='JPEG 품질 (1-100)')
    parser.add_argument('--api-key', help='Gemini API 키 (환경변수 대신 사용)')
    
    args = parser.parse_args()
    
    generator = GeminiImageGenerator(api_key=args.api_key)
    
    if args.platform and args.asset_type:
        # 플랫폼 프리셋 사용
        generator.generate_for_platform(
            prompt=args.prompt,
            platform=args.platform,
            asset_type=args.asset_type,
            output_path=args.output,
            style=args.style,
            quality=args.quality
        )
    else:
        # 직접 크기 지정
        size = parse_size(args.size)
        generator.generate(
            prompt=args.prompt,
            size=size,
            style=args.style,
            output_path=args.output,
            quality=args.quality
        )


if __name__ == '__main__':
    main()
