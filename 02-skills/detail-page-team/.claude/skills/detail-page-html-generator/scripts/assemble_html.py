#!/usr/bin/env python3
"""
Detail Page HTML Assembler
콘텐츠, 디자인 토큰, 비주얼 에셋을 조합하여 상세페이지 HTML 생성

사용법:
    python assemble_html.py --content content.md --tokens tokens/ --visuals visuals/ --platform coupang --output index.html
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

try:
    import markdown
except ImportError:
    markdown = None


class DetailPageAssembler:
    """상세페이지 HTML 조립기"""
    
    # 플랫폼별 스펙
    PLATFORM_SPECS = {
        'coupang': {
            'width': 860,
            'responsive': False,
            'font_family': "-apple-system, BlinkMacSystemFont, 'Malgun Gothic', '맑은 고딕', sans-serif",
            'external_css': False,
            'external_js': False,
        },
        'smartstore': {
            'width': 860,
            'responsive': False,
            'font_family': "-apple-system, BlinkMacSystemFont, 'Malgun Gothic', '맑은 고딕', sans-serif",
            'external_css': False,
            'external_js': False,
        },
        'kurly': {
            'width': 1010,
            'responsive': False,
            'font_family': "'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif",
            'external_css': False,
            'external_js': False,
        },
        'cafe24': {
            'width': 1200,
            'responsive': True,
            'font_family': "-apple-system, BlinkMacSystemFont, 'Malgun Gothic', sans-serif",
            'external_css': True,
            'external_js': True,
        },
    }
    
    def __init__(self, platform: str = 'coupang'):
        """
        Args:
            platform: 대상 플랫폼
        """
        if platform not in self.PLATFORM_SPECS:
            raise ValueError(f"지원하지 않는 플랫폼: {platform}")
        
        self.platform = platform
        self.spec = self.PLATFORM_SPECS[platform]
        self.tokens = {}
        self.visuals = {}
    
    def load_tokens(self, tokens_dir: str) -> Dict:
        """디자인 토큰 로드"""
        tokens_dir = Path(tokens_dir)
        
        token_files = ['colors.json', 'typography.json', 'spacing.json', 'grid.json']
        
        for filename in token_files:
            filepath = tokens_dir / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    key = filename.replace('.json', '')
                    self.tokens[key] = json.load(f)
        
        # CSS 변수 파일 로드
        css_path = tokens_dir / 'tokens.css'
        if css_path.exists():
            self.tokens['css'] = css_path.read_text(encoding='utf-8')
        
        return self.tokens
    
    def load_visuals(self, visuals_dir: str) -> Dict:
        """비주얼 에셋 (base64 HTML) 로드"""
        visuals_dir = Path(visuals_dir)
        
        # manifest.json에서 에셋 목록 로드
        manifest_path = visuals_dir / 'manifest.json'
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
                
            for asset in manifest.get('assets', []):
                code_path = asset.get('code_path')
                if code_path and Path(code_path).exists():
                    name = asset['name']
                    self.visuals[name] = Path(code_path).read_text(encoding='utf-8')
        
        # *-code.html 파일 직접 스캔
        for code_file in visuals_dir.glob('*-code.html'):
            name = code_file.stem.replace('-code', '')
            if name not in self.visuals:
                self.visuals[name] = code_file.read_text(encoding='utf-8')
        
        return self.visuals
    
    def markdown_to_html(self, md_content: str) -> str:
        """마크다운을 HTML로 변환"""
        if markdown:
            return markdown.markdown(
                md_content,
                extensions=['tables', 'fenced_code']
            )
        else:
            # 간단한 마크다운 변환 (markdown 패키지 없을 때)
            html = md_content
            
            # 헤더
            html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
            html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
            html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
            
            # 강조
            html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
            html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
            
            # 리스트
            html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
            html = re.sub(r'(<li>.+</li>\n?)+', r'<ul>\g<0></ul>', html)
            
            # 문단
            paragraphs = html.split('\n\n')
            html = '\n'.join(
                f'<p>{p.strip()}</p>' if not p.strip().startswith('<') else p
                for p in paragraphs if p.strip()
            )
            
            return html
    
    def parse_sections(self, content: str) -> List[Dict]:
        """마크다운 콘텐츠를 섹션별로 파싱"""
        sections = []
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            # H2 레벨에서 섹션 구분
            if line.startswith('## '):
                if current_section:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(current_content)
                    })
                current_section = line[3:].strip()
                current_content = []
            else:
                current_content.append(line)
        
        # 마지막 섹션
        if current_section:
            sections.append({
                'title': current_section,
                'content': '\n'.join(current_content)
            })
        
        return sections
    
    def get_inline_styles(self) -> str:
        """플랫폼에 맞는 인라인 스타일 생성"""
        colors = self.tokens.get('colors', {})
        typography = self.tokens.get('typography', {})
        
        primary_color = colors.get('primary', {}).get('main', '#333333')
        
        styles = f"""
        font-family: {self.spec['font_family']};
        color: #333;
        line-height: 1.6;
        """
        
        return styles.strip().replace('\n', ' ')
    
    def build_section_html(self, section: Dict, index: int) -> str:
        """단일 섹션 HTML 생성"""
        title = section['title']
        content = section['content']
        
        # 섹션 타입 추정
        section_type = self._guess_section_type(title)
        
        # 관련 비주얼 에셋 찾기
        visual_key = f"section-{section_type}"
        visual_html = self.visuals.get(visual_key, '')
        
        # 콘텐츠 HTML 변환
        content_html = self.markdown_to_html(content)
        
        # 섹션 스타일
        section_style = f"""
            margin-bottom: 48px;
            padding: 32px 24px;
        """.strip().replace('\n', ' ')
        
        # 제목 스타일
        title_style = f"""
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 24px;
            color: #222;
        """.strip().replace('\n', ' ')
        
        html = f'''
<section class="section section-{index}" style="{section_style}">
    {visual_html}
    <h2 style="{title_style}">{title}</h2>
    <div class="section-content">
        {content_html}
    </div>
</section>
'''
        return html
    
    def _guess_section_type(self, title: str) -> str:
        """섹션 제목에서 타입 추정"""
        title_lower = title.lower()
        
        mappings = {
            '혜택': 'benefits',
            '특징': 'features',
            '장점': 'benefits',
            '신뢰': 'trust',
            '인증': 'trust',
            '사용': 'usage',
            '활용': 'usage',
            '리뷰': 'reviews',
            '후기': 'reviews',
            'faq': 'faq',
            '질문': 'faq',
            '정보': 'info',
            '스펙': 'specs',
        }
        
        for keyword, section_type in mappings.items():
            if keyword in title_lower:
                return section_type
        
        return 'general'
    
    def assemble(
        self,
        content_path: str,
        tokens_dir: str = None,
        visuals_dir: str = None,
        output_path: str = None
    ) -> str:
        """
        전체 상세페이지 HTML 조립
        
        Args:
            content_path: 콘텐츠 마크다운 경로
            tokens_dir: 디자인 토큰 디렉토리
            visuals_dir: 비주얼 에셋 디렉토리
            output_path: 출력 경로
        
        Returns:
            조립된 HTML 문자열
        """
        # 입력 로드
        content = Path(content_path).read_text(encoding='utf-8')
        
        if tokens_dir:
            self.load_tokens(tokens_dir)
        
        if visuals_dir:
            self.load_visuals(visuals_dir)
        
        # 섹션 파싱
        sections = self.parse_sections(content)
        
        # 히어로 이미지
        hero_html = self.visuals.get('hero-banner', '')
        
        # 섹션 HTML 생성
        sections_html = '\n'.join(
            self.build_section_html(section, i)
            for i, section in enumerate(sections)
        )
        
        # 전체 래퍼 스타일
        wrapper_style = f"""
            width: {self.spec['width']}px;
            margin: 0 auto;
            {self.get_inline_styles()}
        """.strip().replace('\n', ' ')
        
        # 반응형 스타일 (카페24)
        responsive_css = ''
        if self.spec['responsive']:
            responsive_css = f'''
<style>
@media (max-width: 768px) {{
    .{self.platform}-detail-page {{
        width: 100% !important;
        padding: 0 16px;
        box-sizing: border-box;
    }}
    .{self.platform}-detail-page img {{
        width: 100% !important;
        height: auto !important;
    }}
}}
</style>
'''
        
        # 최종 HTML 조립
        html = f'''<!-- 
  상세페이지 HTML
  플랫폼: {self.platform}
  생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}
  
  사용법: 아래 코드를 플랫폼 에디터의 HTML 모드에 붙여넣기
-->
{responsive_css}
<div class="{self.platform}-detail-page" style="{wrapper_style}">

    <!-- 히어로 섹션 -->
    <section class="hero-section" style="margin-bottom: 48px;">
        {hero_html}
    </section>

    <!-- 콘텐츠 섹션 -->
    {sections_html}

</div>
'''
        
        # 저장
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding='utf-8')
            print(f"✅ HTML 저장: {output_path}")
            
            # 미리보기 HTML 생성
            preview_path = output_path.parent / 'preview.html'
            preview_html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>상세페이지 미리보기 - {self.platform}</title>
    <style>
        body {{
            margin: 0;
            padding: 40px 20px;
            background: #f5f5f5;
        }}
        .preview-wrapper {{
            max-width: {self.spec['width'] + 40}px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        .preview-info {{
            padding: 16px;
            background: #f0f0f0;
            margin-bottom: 20px;
            border-radius: 4px;
            font-family: sans-serif;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="preview-wrapper">
        <div class="preview-info">
            <strong>플랫폼:</strong> {self.platform} | 
            <strong>너비:</strong> {self.spec['width']}px |
            <strong>생성일:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </div>
        {html}
    </div>
</body>
</html>
'''
            preview_path.write_text(preview_html, encoding='utf-8')
            print(f"✅ 미리보기 저장: {preview_path}")
        
        return html


def main():
    parser = argparse.ArgumentParser(
        description='상세페이지 HTML 조립'
    )
    parser.add_argument('--content', '-c', required=True, help='콘텐츠 마크다운 경로')
    parser.add_argument('--tokens', '-t', help='디자인 토큰 디렉토리')
    parser.add_argument('--visuals', '-v', help='비주얼 에셋 디렉토리')
    parser.add_argument('--platform', '-p', default='coupang',
                       choices=['coupang', 'smartstore', 'kurly', 'cafe24'])
    parser.add_argument('--output', '-o', required=True, help='출력 HTML 경로')
    
    args = parser.parse_args()
    
    assembler = DetailPageAssembler(platform=args.platform)
    assembler.assemble(
        content_path=args.content,
        tokens_dir=args.tokens,
        visuals_dir=args.visuals,
        output_path=args.output
    )


if __name__ == '__main__':
    main()
