#!/usr/bin/env python3
"""
Batch Visual Asset Generator
상세페이지용 비주얼 에셋 일괄 생성

사용법:
    python batch_generate.py --brief brief.md --platform coupang --output outputs/visuals/
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

try:
    from generate_image import GeminiImageGenerator
    from image_to_code import ImageToCodeConverter
except ImportError:
    # 스크립트 디렉토리에서 직접 실행 시
    import sys
    sys.path.append(str(Path(__file__).parent))
    from generate_image import GeminiImageGenerator
    from image_to_code import ImageToCodeConverter


class BatchAssetGenerator:
    """상세페이지 비주얼 에셋 일괄 생성기"""
    
    # 기본 에셋 구성
    DEFAULT_ASSETS = [
        {'type': 'hero', 'name': 'hero-banner', 'count': 1},
        {'type': 'section', 'name': 'section-benefits', 'count': 1},
        {'type': 'section', 'name': 'section-features', 'count': 1},
        {'type': 'section', 'name': 'section-trust', 'count': 1},
        {'type': 'product', 'name': 'product-main', 'count': 1},
        {'type': 'icon', 'name': 'icon-delivery', 'count': 1},
        {'type': 'icon', 'name': 'icon-quality', 'count': 1},
        {'type': 'icon', 'name': 'icon-guarantee', 'count': 1},
    ]
    
    # 카테고리별 스타일 프리셋
    CATEGORY_STYLES = {
        'food': {
            'hero': 'warm cozy kitchen, natural lighting, appetizing food photography, steam rising, wooden table',
            'section': 'soft warm gradient, organic shapes, cream and brown tones',
            'product': 'clean white background, natural lighting, appetizing presentation',
            'icon': 'warm orange and brown, friendly rounded style',
        },
        'beauty': {
            'hero': 'elegant marble surface, soft pink lighting, luxury cosmetics photography, rose petals',
            'section': 'soft pink and white gradient, elegant curves, subtle sparkles',
            'product': 'clean white or marble background, soft shadows, premium feel',
            'icon': 'soft pink and gold, elegant minimal style',
        },
        'electronics': {
            'hero': 'modern minimalist studio, cool lighting, tech product photography, gradient background',
            'section': 'blue gradient, geometric shapes, tech feel',
            'product': 'pure white background, sharp reflections, studio lighting',
            'icon': 'blue and gray, modern geometric style',
        },
        'fashion': {
            'hero': 'stylish studio setup, dramatic lighting, fashion photography, neutral background',
            'section': 'neutral gradient, elegant typography space, sophisticated',
            'product': 'clean background, professional fashion photography style',
            'icon': 'black and white, minimal elegant style',
        },
        'default': {
            'hero': 'professional studio, clean background, product-focused',
            'section': 'subtle gradient, clean modern design',
            'product': 'white background, professional photography',
            'icon': 'clean minimal style, brand colors',
        },
    }
    
    def __init__(
        self,
        api_key: str = None,
        platform: str = 'coupang',
        output_dir: str = 'outputs/visuals'
    ):
        """
        Args:
            api_key: Gemini API 키
            platform: 대상 플랫폼
            output_dir: 출력 디렉토리
        """
        self.image_generator = GeminiImageGenerator(api_key=api_key)
        self.code_converter = ImageToCodeConverter(optimize=True)
        self.platform = platform
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.manifest = {
            'generated_at': datetime.now().isoformat(),
            'platform': platform,
            'assets': []
        }
    
    def parse_brief(self, brief_path: str) -> Dict:
        """
        brief.md에서 제품 정보 추출
        
        Returns:
            {product_name, category, key_benefits, brand_color, ...}
        """
        brief_path = Path(brief_path)
        if not brief_path.exists():
            raise FileNotFoundError(f"brief 파일을 찾을 수 없습니다: {brief_path}")
        
        content = brief_path.read_text(encoding='utf-8')
        
        # 정보 추출 (마크다운 파싱)
        info = {
            'product_name': self._extract_field(content, r'제품명[:\s]*(.+)'),
            'category': self._extract_field(content, r'카테고리[:\s]*(.+)'),
            'key_benefits': self._extract_list(content, r'핵심\s*혜택[:\s]*\n((?:[-*]\s*.+\n?)+)'),
            'target_audience': self._extract_field(content, r'타겟[:\s]*(.+)'),
            'brand_color': self._extract_field(content, r'브랜드\s*컬러[:\s]*(#[0-9a-fA-F]{6})'),
            'differentiators': self._extract_list(content, r'차별점[:\s]*\n((?:[-*]\s*.+\n?)+)'),
        }
        
        # 카테고리 매핑
        category_mapping = {
            '식품': 'food',
            '음식': 'food',
            '뷰티': 'beauty',
            '화장품': 'beauty',
            '가전': 'electronics',
            '전자기기': 'electronics',
            '패션': 'fashion',
            '의류': 'fashion',
        }
        
        if info['category']:
            info['category_key'] = category_mapping.get(info['category'], 'default')
        else:
            info['category_key'] = 'default'
        
        return info
    
    def _extract_field(self, content: str, pattern: str) -> Optional[str]:
        """정규식으로 단일 필드 추출"""
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _extract_list(self, content: str, pattern: str) -> List[str]:
        """정규식으로 리스트 추출"""
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            items = re.findall(r'[-*]\s*(.+)', match.group(1))
            return [item.strip() for item in items]
        return []
    
    def generate_prompt(
        self,
        product_info: Dict,
        asset_type: str,
        asset_name: str
    ) -> str:
        """
        에셋용 프롬프트 생성
        
        Args:
            product_info: brief에서 추출한 제품 정보
            asset_type: hero, section, product, icon
            asset_name: 에셋 이름
        
        Returns:
            영문 프롬프트
        """
        category_key = product_info.get('category_key', 'default')
        style = self.CATEGORY_STYLES.get(category_key, self.CATEGORY_STYLES['default'])
        
        product_name = product_info.get('product_name', 'product')
        benefits = product_info.get('key_benefits', [])
        
        base_style = style.get(asset_type, '')
        
        if asset_type == 'hero':
            prompt = f"{product_name}, main hero banner image, {base_style}, high quality professional photography"
        
        elif asset_type == 'section':
            section_topic = asset_name.replace('section-', '')
            prompt = f"Abstract background for {section_topic} section, {base_style}, suitable for text overlay"
        
        elif asset_type == 'product':
            prompt = f"{product_name}, product shot, {base_style}, e-commerce ready"
        
        elif asset_type == 'icon':
            icon_topic = asset_name.replace('icon-', '')
            benefit_text = benefits[0] if benefits else icon_topic
            prompt = f"Simple icon representing {icon_topic} or {benefit_text}, {base_style}, flat design"
        
        else:
            prompt = f"{product_name}, {base_style}"
        
        return prompt
    
    def generate_all(
        self,
        brief_path: str,
        assets: List[Dict] = None,
        generate_code: bool = True
    ) -> Dict:
        """
        모든 에셋 일괄 생성
        
        Args:
            brief_path: brief.md 경로
            assets: 생성할 에셋 목록 (None이면 기본값)
            generate_code: HTML 코드 생성 여부
        
        Returns:
            생성 결과 manifest
        """
        # brief 파싱
        product_info = self.parse_brief(brief_path)
        print(f"📋 제품: {product_info.get('product_name', 'Unknown')}")
        print(f"📁 카테고리: {product_info.get('category', 'Unknown')}")
        print(f"🎨 플랫폼: {self.platform}")
        print("-" * 50)
        
        assets = assets or self.DEFAULT_ASSETS
        
        for asset in assets:
            asset_type = asset['type']
            asset_name = asset['name']
            count = asset.get('count', 1)
            
            for i in range(count):
                suffix = f"-{i+1}" if count > 1 else ""
                filename = f"{asset_name}{suffix}"
                
                print(f"🎨 생성 중: {filename}")
                
                # 프롬프트 생성
                prompt = self.generate_prompt(product_info, asset_type, asset_name)
                
                # 이미지 생성
                output_path = self.output_dir / f"{filename}.png"
                
                try:
                    self.image_generator.generate_for_platform(
                        prompt=prompt,
                        platform=self.platform,
                        asset_type=asset_type,
                        output_path=str(output_path)
                    )
                    
                    # HTML 코드 생성
                    code_path = None
                    if generate_code:
                        code_path = self.output_dir / f"{filename}-code.html"
                        html_code = self.code_converter.to_html_img(
                            str(output_path),
                            alt=f"{product_info.get('product_name', '')} {asset_name}",
                            css_class=f"detail-page-{asset_type}"
                        )
                        code_path.write_text(html_code, encoding='utf-8')
                    
                    # manifest에 추가
                    self.manifest['assets'].append({
                        'name': filename,
                        'type': asset_type,
                        'prompt': prompt,
                        'image_path': str(output_path),
                        'code_path': str(code_path) if code_path else None,
                        'status': 'success'
                    })
                    
                    print(f"   ✅ 완료: {output_path}")
                    
                except Exception as e:
                    print(f"   ❌ 실패: {e}")
                    self.manifest['assets'].append({
                        'name': filename,
                        'type': asset_type,
                        'prompt': prompt,
                        'status': 'failed',
                        'error': str(e)
                    })
        
        # manifest 저장
        manifest_path = self.output_dir / 'manifest.json'
        manifest_path.write_text(
            json.dumps(self.manifest, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        print("-" * 50)
        print(f"📄 Manifest 저장: {manifest_path}")
        
        # 통합 HTML 생성
        if generate_code:
            self._generate_combined_html()
        
        return self.manifest
    
    def _generate_combined_html(self):
        """모든 에셋을 포함한 통합 HTML 생성"""
        html_parts = ['<!DOCTYPE html>', '<html>', '<head>',
                     '<meta charset="UTF-8">',
                     '<title>Generated Visual Assets</title>',
                     '<style>',
                     'body { font-family: sans-serif; padding: 20px; background: #f5f5f5; }',
                     '.asset { margin: 20px 0; padding: 20px; background: white; border-radius: 8px; }',
                     '.asset h3 { margin: 0 0 10px 0; }',
                     '.asset img { max-width: 100%; height: auto; }',
                     '.asset-type { color: #666; font-size: 12px; }',
                     '</style>',
                     '</head>', '<body>',
                     f'<h1>Visual Assets - {self.platform}</h1>']
        
        for asset in self.manifest['assets']:
            if asset['status'] == 'success' and asset.get('image_path'):
                code_path = asset.get('code_path')
                if code_path and Path(code_path).exists():
                    img_html = Path(code_path).read_text(encoding='utf-8')
                    html_parts.append(f'''
<div class="asset">
    <h3>{asset['name']}</h3>
    <span class="asset-type">{asset['type']}</span>
    {img_html}
</div>''')
        
        html_parts.extend(['</body>', '</html>'])
        
        combined_path = self.output_dir / 'all-assets.html'
        combined_path.write_text('\n'.join(html_parts), encoding='utf-8')
        print(f"📦 통합 HTML: {combined_path}")


def main():
    parser = argparse.ArgumentParser(
        description='상세페이지 비주얼 에셋 일괄 생성'
    )
    parser.add_argument('--brief', '-b', required=True, help='brief.md 경로')
    parser.add_argument('--platform', '-p', default='coupang',
                       choices=['coupang', 'smartstore', 'kurly', 'cafe24'])
    parser.add_argument('--output', '-o', default='outputs/visuals', help='출력 디렉토리')
    parser.add_argument('--api-key', help='Gemini API 키')
    parser.add_argument('--no-code', action='store_true', help='HTML 코드 생성 안함')
    
    args = parser.parse_args()
    
    generator = BatchAssetGenerator(
        api_key=args.api_key,
        platform=args.platform,
        output_dir=args.output
    )
    
    generator.generate_all(
        brief_path=args.brief,
        generate_code=not args.no_code
    )


if __name__ == '__main__':
    main()
