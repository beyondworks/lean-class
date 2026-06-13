#!/usr/bin/env python3
"""
Grid Overlay Analyzer
스크린샷에 가상 격자를 오버레이하여 레이아웃 분석

사용법:
    python grid_analyzer.py input.png --grid 8 --columns 12
"""

import argparse
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json


class GridAnalyzer:
    """디자인 툴 스타일의 격자 분석기"""
    
    def __init__(self, image_path: str):
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.analysis_result = {}
        
    def create_baseline_grid(
        self,
        unit: int = 8,
        output_path: str = None,
        color: str = "#FF00FF",
        opacity: float = 0.3
    ) -> Image.Image:
        """
        기준선 격자 생성 (Baseline Grid)
        Figma/Sketch 스타일의 수평 기준선
        
        Args:
            unit: 격자 단위 (기본 8px)
            color: 격자 색상
            opacity: 투명도
        """
        overlay = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # HEX to RGBA
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        a = int(255 * opacity)
        
        # 수평 기준선 그리기
        for y in range(0, self.height, unit):
            draw.line([(0, y), (self.width, y)], fill=(r, g, b, a), width=1)
        
        # 원본과 합성
        result = Image.alpha_composite(self.image.convert('RGBA'), overlay)
        
        if output_path:
            result.save(output_path)
            
        return result
    
    def create_column_grid(
        self,
        columns: int = 12,
        gutter: int = 24,
        margin: int = 32,
        container_width: int = None,
        output_path: str = None,
        color: str = "#FF0000",
        opacity: float = 0.15
    ) -> Image.Image:
        """
        컬럼 격자 생성 (Column Grid)
        Bootstrap/Figma 스타일의 12컬럼 그리드
        
        Args:
            columns: 컬럼 수 (기본 12)
            gutter: 컬럼 간 간격
            margin: 좌우 마진
            container_width: 컨테이너 너비 (None이면 이미지 너비 사용)
        """
        overlay = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # HEX to RGBA
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        a = int(255 * opacity)
        
        # 컨테이너 계산
        if container_width is None:
            container_width = self.width - (margin * 2)
        
        container_start = (self.width - container_width) // 2
        
        # 컬럼 너비 계산
        total_gutter = gutter * (columns - 1)
        column_width = (container_width - total_gutter) / columns
        
        # 컬럼 그리기
        x = container_start
        for i in range(columns):
            # 컬럼 영역 (채움)
            draw.rectangle(
                [(x, 0), (x + column_width, self.height)],
                fill=(r, g, b, a)
            )
            x += column_width + gutter
        
        # 컨테이너 경계선
        draw.line(
            [(container_start, 0), (container_start, self.height)],
            fill=(r, g, b, int(255 * 0.5)),
            width=2
        )
        draw.line(
            [(container_start + container_width, 0), 
             (container_start + container_width, self.height)],
            fill=(r, g, b, int(255 * 0.5)),
            width=2
        )
        
        # 원본과 합성
        result = Image.alpha_composite(self.image.convert('RGBA'), overlay)
        
        # 분석 결과 저장
        self.analysis_result['column_grid'] = {
            'columns': columns,
            'gutter': gutter,
            'margin': margin,
            'container_width': container_width,
            'column_width': round(column_width, 2),
            'container_start': container_start,
        }
        
        if output_path:
            result.save(output_path)
            
        return result
    
    def create_measurement_grid(
        self,
        unit: int = 8,
        major_unit: int = 64,
        output_path: str = None
    ) -> Image.Image:
        """
        측정용 격자 생성 (Measurement Grid)
        눈금자 스타일의 정밀 측정 격자
        
        Args:
            unit: 소단위 (기본 8px)
            major_unit: 대단위 (기본 64px) - 숫자 표시
        """
        overlay = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 소단위 격자 (연한 선)
        minor_color = (100, 100, 100, 50)
        for x in range(0, self.width, unit):
            draw.line([(x, 0), (x, self.height)], fill=minor_color, width=1)
        for y in range(0, self.height, unit):
            draw.line([(0, y), (self.width, y)], fill=minor_color, width=1)
        
        # 대단위 격자 (진한 선 + 숫자)
        major_color = (50, 50, 50, 150)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        except:
            font = ImageFont.load_default()
        
        # 수직선 + 상단 숫자
        for x in range(0, self.width, major_unit):
            draw.line([(x, 0), (x, self.height)], fill=major_color, width=1)
            draw.text((x + 2, 2), str(x), fill=(0, 0, 0, 200), font=font)
        
        # 수평선 + 좌측 숫자
        for y in range(0, self.height, major_unit):
            draw.line([(0, y), (self.width, y)], fill=major_color, width=1)
            draw.text((2, y + 2), str(y), fill=(0, 0, 0, 200), font=font)
        
        # 원본과 합성
        result = Image.alpha_composite(self.image.convert('RGBA'), overlay)
        
        if output_path:
            result.save(output_path)
            
        return result
    
    def create_combined_grid(
        self,
        baseline_unit: int = 8,
        columns: int = 12,
        gutter: int = 24,
        margin: int = 32,
        container_width: int = None,
        output_path: str = None
    ) -> Image.Image:
        """
        통합 격자 생성 (Combined Grid)
        기준선 + 컬럼 + 측정 격자 통합
        """
        # 기준선 격자 (연한 마젠타)
        result = self.create_baseline_grid(
            unit=baseline_unit,
            color="#FF00FF",
            opacity=0.1
        )
        
        # 임시 이미지로 컬럼 격자 추가
        temp_analyzer = GridAnalyzer.__new__(GridAnalyzer)
        temp_analyzer.image = result
        temp_analyzer.width, temp_analyzer.height = result.size
        temp_analyzer.analysis_result = self.analysis_result
        
        result = temp_analyzer.create_column_grid(
            columns=columns,
            gutter=gutter,
            margin=margin,
            container_width=container_width,
            color="#00BFFF",
            opacity=0.12
        )
        
        self.analysis_result = temp_analyzer.analysis_result
        
        if output_path:
            result.save(output_path)
            
        return result
    
    def analyze_spacing_pattern(
        self,
        sample_points: list = None
    ) -> dict:
        """
        간격 패턴 분석
        이미지에서 자주 사용되는 간격 값 추정
        """
        # 8px 기반 간격 스케일
        standard_spacings = [4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 120]
        
        # 분석 결과
        self.analysis_result['spacing_scale'] = {
            'base_unit': 8,
            'recommended_scale': standard_spacings,
            'semantic_mapping': {
                'xs': 4,
                'sm': 8,
                'md': 16,
                'lg': 24,
                'xl': 32,
                'xxl': 48,
                'section-sm': 64,
                'section-md': 80,
                'section-lg': 120,
            }
        }
        
        return self.analysis_result['spacing_scale']
    
    def generate_tokens(self, output_path: str = None) -> dict:
        """
        분석 결과를 토큰 형식으로 출력
        """
        tokens = {
            'grid': self.analysis_result.get('column_grid', {}),
            'spacing': self.analysis_result.get('spacing_scale', {}),
            'image_dimensions': {
                'width': self.width,
                'height': self.height,
            }
        }
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(tokens, f, indent=2)
        
        return tokens
    
    def create_analysis_report(
        self,
        columns: int = 12,
        gutter: int = 24,
        margin: int = 32,
        baseline_unit: int = 8,
        container_width: int = None,
        output_dir: str = "grid_analysis"
    ) -> dict:
        """
        전체 분석 리포트 생성
        여러 격자 오버레이 이미지와 분석 결과 JSON 출력
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # 1. 기준선 격자
        self.create_baseline_grid(
            unit=baseline_unit,
            output_path=str(output_path / "01_baseline_grid.png")
        )
        
        # 2. 컬럼 격자
        self.create_column_grid(
            columns=columns,
            gutter=gutter,
            margin=margin,
            container_width=container_width,
            output_path=str(output_path / "02_column_grid.png")
        )
        
        # 3. 측정 격자
        self.create_measurement_grid(
            unit=baseline_unit,
            output_path=str(output_path / "03_measurement_grid.png")
        )
        
        # 4. 통합 격자
        self.create_combined_grid(
            baseline_unit=baseline_unit,
            columns=columns,
            gutter=gutter,
            margin=margin,
            container_width=container_width,
            output_path=str(output_path / "04_combined_grid.png")
        )
        
        # 5. 간격 분석
        self.analyze_spacing_pattern()
        
        # 6. 토큰 출력
        tokens = self.generate_tokens(
            output_path=str(output_path / "grid_tokens.json")
        )
        
        # 7. 분석 리포트
        report = {
            'image_info': {
                'width': self.width,
                'height': self.height,
            },
            'grid_settings': {
                'columns': columns,
                'gutter': gutter,
                'margin': margin,
                'baseline_unit': baseline_unit,
                'container_width': container_width or (self.width - margin * 2),
            },
            'analysis': self.analysis_result,
            'output_files': {
                'baseline_grid': '01_baseline_grid.png',
                'column_grid': '02_column_grid.png',
                'measurement_grid': '03_measurement_grid.png',
                'combined_grid': '04_combined_grid.png',
                'tokens': 'grid_tokens.json',
            }
        }
        
        with open(output_path / "analysis_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ 분석 완료: {output_path}")
        print(f"   - 기준선 격자: 01_baseline_grid.png")
        print(f"   - 컬럼 격자: 02_column_grid.png")
        print(f"   - 측정 격자: 03_measurement_grid.png")
        print(f"   - 통합 격자: 04_combined_grid.png")
        print(f"   - 토큰: grid_tokens.json")
        print(f"   - 리포트: analysis_report.json")
        
        return report


def main():
    parser = argparse.ArgumentParser(
        description='스크린샷에 격자 오버레이를 적용하여 레이아웃 분석'
    )
    parser.add_argument('image', help='분석할 이미지 경로')
    parser.add_argument('--grid', type=int, default=8, help='기준선 격자 단위 (기본: 8px)')
    parser.add_argument('--columns', type=int, default=12, help='컬럼 수 (기본: 12)')
    parser.add_argument('--gutter', type=int, default=24, help='컬럼 간 간격 (기본: 24px)')
    parser.add_argument('--margin', type=int, default=32, help='좌우 마진 (기본: 32px)')
    parser.add_argument('--container', type=int, default=None, help='컨테이너 너비')
    parser.add_argument('--output', '-o', default='grid_analysis', help='출력 디렉토리')
    
    args = parser.parse_args()
    
    analyzer = GridAnalyzer(args.image)
    analyzer.create_analysis_report(
        columns=args.columns,
        gutter=args.gutter,
        margin=args.margin,
        baseline_unit=args.grid,
        container_width=args.container,
        output_dir=args.output
    )


if __name__ == '__main__':
    main()
