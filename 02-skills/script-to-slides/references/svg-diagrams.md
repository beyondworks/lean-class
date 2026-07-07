# SVG 다이어그램 패턴 (골든 레퍼런스 추출)

모두 `.dg` 클래스 + theme.css 의 `.l/.s/.nd/.na/.e/.ea` 토큰을 쓴다. **좌표는 viewBox 기준 px**(stage cqw 아님). 라벨만 교체해 재사용.

규칙: ① 선은 노드 **가장자리에서 끊는다**(관통 금지) ② 화살표 marker는 작게 ③ 라벨이 박스 밖으로 넘으면 `font-size` 축소/문구 단축 ④ split 레이아웃에선 `.dg`(46cqw)·`.dg.sm`(38cqw).

## 1. 박스맵 (중심 + 사방 연결)
중심 개념에서 4방향으로 뻗는 관계도. 선이 박스 edge에서 정확히 멈추게(아래 H170/H390 처럼 박스 변 좌표).
```html
<svg class="dg" viewBox="0 0 560 460">
  <rect x="210" y="195" width="140" height="70" rx="14" class="na"/>
  <text x="280" y="227" text-anchor="middle" class="l" style="fill:var(--green)">중심</text>
  <text x="280" y="248" text-anchor="middle" class="s">= 부제</text>
  <path d="M280 195V120" class="ea"/><path d="M280 265V340" class="ea"/>
  <path d="M210 230H170" class="ea"/><path d="M350 230H390" class="ea"/>
  <rect x="160" y="40"  width="240" height="80" rx="12" class="nd"/><text x="280" y="74"  text-anchor="middle" class="l">위</text><text x="280" y="98"  text-anchor="middle" class="s">부제</text>
  <rect x="160" y="340" width="240" height="80" rx="12" class="nd"/><text x="280" y="374" text-anchor="middle" class="l">아래</text><text x="280" y="398" text-anchor="middle" class="s">부제</text>
  <rect x="10"  y="190" width="160" height="80" rx="12" class="nd"/><text x="90"  y="224" text-anchor="middle" class="l">왼쪽</text><text x="90"  y="248" text-anchor="middle" class="s">부제</text>
  <rect x="390" y="190" width="160" height="80" rx="12" class="nd"/><text x="470" y="224" text-anchor="middle" class="l">오른쪽</text><text x="470" y="248" text-anchor="middle" class="s">부제</text>
</svg>
```

## 2. 흐름 (노드 → 화살표 → 노드, 단계별 통제 라벨)
순서(워크플로우) + 각 단계 제약. 화살표는 카드 사이 **중앙에 짧게**, marker 작게.
```html
<svg class="dg" viewBox="0 0 900 250" style="width:80cqw;max-width:1220px">
  <defs><marker id="arh" markerWidth="6" markerHeight="6" refX="4.6" refY="2.6" orient="auto"><path d="M0 0 L5 2.6 L0 5.2 Z" fill="var(--green)"/></marker></defs>
  <rect x="20" y="34" width="220" height="78" rx="12" class="nd"/><text x="130" y="80" text-anchor="middle" class="l">1단계</text>
  <rect x="340" y="34" width="220" height="78" rx="12" class="nd"/><text x="450" y="80" text-anchor="middle" class="l">2단계</text>
  <rect x="660" y="34" width="220" height="78" rx="12" class="nd"/><text x="770" y="80" text-anchor="middle" class="l">3단계</text>
  <path d="M278 73H302" class="ea" style="stroke-width:1.8" marker-end="url(#arh)"/><text x="290" y="56" text-anchor="middle" class="s">~하는 동안</text>
  <path d="M598 73H622" class="ea" style="stroke-width:1.8" marker-end="url(#arh)"/><text x="610" y="56" text-anchor="middle" class="s">~하는 동안</text>
  <text x="450" y="140" text-anchor="middle" class="s" style="fill:var(--green)">↓ 단계별 제약</text>
  <rect x="20"  y="160" width="220" height="58" rx="8" fill="rgba(10,207,131,.12)" stroke="rgba(10,207,131,.4)"/><text x="130" y="195" text-anchor="middle" class="s" style="fill:#fff;font-size:15px">제약 A</text>
  <rect x="340" y="160" width="220" height="58" rx="8" fill="rgba(10,207,131,.12)" stroke="rgba(10,207,131,.4)"/><text x="450" y="195" text-anchor="middle" class="s" style="fill:#fff;font-size:15px">제약 B</text>
  <rect x="660" y="160" width="220" height="58" rx="8" fill="rgba(10,207,131,.12)" stroke="rgba(10,207,131,.4)"/><text x="770" y="195" text-anchor="middle" class="s" style="fill:#fff;font-size:15px">제약 C</text>
</svg>
```

## 3. U자 곡선 (가운데가 떨어짐 — Lost in the Middle 류)
```html
<svg class="dg" viewBox="0 0 600 320">
  <line x1="70" y1="30" x2="70" y2="270" class="e"/><line x1="70" y1="270" x2="560" y2="270" class="e"/>
  <text x="60" y="40" text-anchor="end" class="s">높음</text><text x="60" y="268" text-anchor="end" class="s">낮음</text>
  <path d="M95 60 C 190 70, 250 235, 315 242 C 380 235, 440 70, 535 60" fill="none" stroke="var(--green)" stroke-width="3.5"/>
  <circle cx="95" cy="60" r="6" fill="var(--green)"/><circle cx="315" cy="242" r="6" fill="#f0857c"/><circle cx="535" cy="60" r="6" fill="var(--green)"/>
  <text x="315" y="300" text-anchor="middle" class="l" style="fill:#f0857c;font-size:15px">↑ 가운데가 떨어짐</text>
</svg>
```

## 4. 대비 박스 (A ≠ B)
```html
<svg class="dg" viewBox="0 0 600 300">
  <rect x="20" y="30" width="250" height="240" rx="14" class="nd"/><text x="145" y="64" text-anchor="middle" class="l">A</text>
  <text x="300" y="150" text-anchor="middle" style="fill:#f0857c;font-size:26px;font-weight:800">≠</text>
  <rect x="330" y="30" width="250" height="240" rx="14" class="na"/><text x="455" y="64" text-anchor="middle" class="l" style="fill:var(--green)">B</text>
</svg>
```

## 색
- 그린 `var(--green)` = 긍정/강조, 빨강 `#f0857c` = 부정/하락/≠. 노드 기본 `.nd`(회색), 강조 `.na`(그린 틴트).
- 도트·점선 경고: `stroke="#f0857c" stroke-dasharray="6 5"`.
