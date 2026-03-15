# SPEC-UI-MAC-001: macOS Style UI Redesign

## Metadata

| Field | Value |
|-------|-------|
| SPEC ID | SPEC-UI-MAC-001 |
| Title | macOS Style UI Redesign |
| Version | 0.2.0 |
| Status | Planned |
| Priority | High |
| Created | 2026-03-15 |
| Related | SPEC-UI-001 (기존 GUI 구현) |

---

## Environment

- **Runtime**: Python >= 3.13, CustomTkinter >= 5.2.0
- **Platform**: macOS (주 대상), Windows/Linux (호환성 유지)
- **현재 상태**: CustomTkinter 기반 Windows 스타일 GUI (다크/라이트 테마)
- **GUI 구조**: 9개 페이지 (Cut, Merge, Split, Rotate, Resize, Compress, Watermark, Images to PDF, Info)
- **아키텍처**: BasePage (로직) + PageWidget (UI) 분리 패턴, PageManager 페이지 전환
- **디자인 시스템**: ColorPalette dataclass + constants.py 중앙 관리

---

## Assumptions

1. CustomTkinter 프레임워크를 유지하면서 macOS HIG 스타일을 적용한다 (네이티브 Swift UI 전환은 하지 않음)
2. 기존 비즈니스 로직 (commands/, core/) 은 변경하지 않는다
3. macOS에서 San Francisco 시스템 폰트가 사용 가능하다
4. Windows/Linux에서는 대체 폰트 (Segoe UI, Inter)로 자동 폴백한다
5. 기존 테스트 코드의 호환성을 유지한다
6. SF Symbols 대신 유사한 유니코드/SVG 아이콘을 사용한다 (SF Symbols는 Apple 전용 라이선스)

---

## Requirements

### REQ-THEME-001: Apple 색상 체계 적용 (Ubiquitous)

시스템은 **항상** Apple Human Interface Guidelines의 색상 체계를 사용해야 한다.

- 다크 모드: `systemBackground` (#000000), `secondarySystemBackground` (#1C1C1E), `tertiarySystemBackground` (#2C2C2E)
- 라이트 모드: `systemBackground` (#FFFFFF), `secondarySystemBackground` (#F2F2F7), `tertiarySystemBackground` (#FFFFFF)
- 액센트 컬러: Apple Blue (#007AFF), Green (#34C759), Red (#FF3B30), Orange (#FF9500), Yellow (#FFCC00)
- Tint Color 시스템: 각 기능별 고유 tint color 지원

### REQ-THEME-002: San Francisco 타이포그래피 (Ubiquitous)

시스템은 **항상** Apple San Francisco 타이포그래피 시스템을 따라야 한다.

- macOS: SF Pro Text (본문), SF Pro Display (제목), SF Mono (코드)
- 폰트 크기 체계: Large Title (34pt), Title 1 (28pt), Title 2 (22pt), Title 3 (20pt), Headline (17pt Bold), Body (17pt), Callout (16pt), Subheadline (15pt), Footnote (13pt), Caption (12pt)
- Dynamic Type 대응: 사용자 시스템 폰트 크기 설정 존중
- Windows 폴백: "Segoe UI", Linux 폴백: "Inter" 또는 "Cantarell"

### REQ-THEME-003: 다크/라이트 모드 지원 (Event-Driven)

**WHEN** 사용자가 테마 전환 버튼을 클릭하거나 시스템 테마가 변경되면 **THEN** UI 전체가 즉시 해당 모드로 전환되어야 한다.

- 전환 시 모든 컴포넌트가 동시에 업데이트
- 시스템 테마 자동 감지 (macOS `NSApp.effectiveAppearance` 또는 `darkdetect` 라이브러리)
- 전환 애니메이션: 0.2초 페이드 트랜지션

### REQ-COMP-001: macOS 스타일 사이드바 (Ubiquitous)

시스템은 **항상** macOS Finder/Settings 스타일의 사이드바를 표시해야 한다.

- 사이드바 배경: vibrancy 효과 시뮬레이션 (반투명 블러 배경)
- 네비게이션 항목: 아이콘 + 텍스트 조합, 선택 시 rounded rectangle 하이라이트
- 하이라이트 색상: 시스템 accent color 기반 (#007AFF 기본)
- 항목 간격: 2pt, 항목 높이: 28pt, 코너 반지름: 6pt
- 섹션 그룹핑: "도구" 헤더로 기능 그룹화
- hover 효과: 배경색 미세 변화 (opacity 0.1)

### REQ-COMP-002: macOS 스타일 버튼 (Ubiquitous)

시스템은 **항상** macOS HIG 규격의 버튼을 표시해야 한다.

- Primary 버튼: 둥근 모서리 (corner radius 6pt), 시스템 accent color 배경, 흰색 텍스트
- Secondary 버튼: 시스템 기본 회색 배경, 텍스트 색상
- Destructive 버튼: Red (#FF3B30) 배경
- 버튼 크기: Regular (22pt 높이), Large (28pt 높이), Mini (16pt 높이)
- 눌림 효과: 배경색 20% 어두워짐, 0.1초 트랜지션
- 비활성 상태: opacity 0.5

### REQ-COMP-003: macOS 스타일 입력 필드 (Ubiquitous)

시스템은 **항상** macOS 네이티브 스타일의 입력 필드를 표시해야 한다.

- 테두리: 1pt solid, 라이트모드 #D1D1D6 / 다크모드 #3A3A3C
- 포커스 링: Apple Blue (#007AFF) 3pt 그림자
- 코너 반지름: 6pt
- 내부 패딩: 좌우 8pt, 상하 4pt
- placeholder 텍스트: #8E8E93 (tertiaryLabel)
- 배경: 라이트모드 #FFFFFF / 다크모드 #1C1C1E

### REQ-COMP-004: macOS 스타일 드롭다운/세그먼트 컨트롤 (Ubiquitous)

시스템은 **항상** 옵션 선택에 macOS 네이티브 스타일 컨트롤을 사용해야 한다.

- SegmentedControl: 캡슐 형태, 선택 항목 흰색 배경 슬라이딩
- 드롭다운: 시스템 팝업 버튼 스타일 (둥근 모서리, 화살표 아이콘)
- 코너 반지름: 8pt (세그먼트), 6pt (드롭다운)

### REQ-COMP-005: 파일 드롭 영역 (Ubiquitous)

시스템은 **항상** macOS 스타일의 파일 드래그-앤-드롭 영역을 표시해야 한다.

- 대시 보더: 2pt dashed, 코너 반지름 12pt
- 아이콘: 문서 아이콘 (SF Symbols 대체 유니코드)
- 안내 텍스트: "파일을 끌어다 놓거나 클릭하여 선택"
- 드래그 오버 상태: 보더 색상 accent color, 배경 accent color 10% opacity
- 파일 선택 후: 파일 이름 + 크기 표시, 제거 버튼

### REQ-COMP-006: 진행률 표시 (Ubiquitous)

시스템은 **항상** macOS 네이티브 스타일의 진행률 표시기를 사용해야 한다.

- 불확정 진행률: macOS 스타일 스피너 (회전 바)
- 확정 진행률: 가느다란 바 (높이 4pt), 둥근 모서리, accent color
- 배경: #E5E5EA (라이트) / #3A3A3C (다크)

### REQ-COMP-007: 결과 표시 영역 (Event-Driven)

**WHEN** 작업이 완료되면 **THEN** macOS 알림 스타일의 결과를 표시해야 한다.

- 성공: 초록색 체크 아이콘 + "완료" 텍스트 + 파일 경로
- 실패: 빨간색 X 아이콘 + 에러 메시지
- 결과 카드: 둥근 모서리 (12pt), 그림자 효과
- 파일 열기 버튼: "Finder에서 보기" (macOS) / "폴더 열기" (기타)

### REQ-COMP-008: PDF 미리보기 (Event-Driven)

**WHEN** 작업이 완료되면 **THEN** macOS Quick Look 스타일의 미리보기를 표시해야 한다.

- 썸네일: 둥근 모서리 (8pt), 가벼운 그림자
- 페이지 정보: 하단에 페이지 수/크기 표시
- 확대 버튼: Quick Look 아이콘

### REQ-LAYOUT-001: 페이지 레이아웃 표준화 (Ubiquitous)

시스템은 **항상** 다음 레이아웃 구조를 따라야 한다.

- 페이지 제목: Title 2 (22pt), 상단 고정
- 설명 텍스트: Body (17pt), secondaryLabel 색상
- 컨텐츠 영역: 상단 여백 20pt, 좌우 여백 24pt
- 섹션 구분: 16pt 간격
- 하단 액션 바: 실행 버튼 고정, 상단 구분선

### REQ-LAYOUT-002: 툴바 영역 (Ubiquitous)

시스템은 **항상** 각 페이지 상단에 macOS 스타일 툴바를 표시해야 한다.

- 배경: 사이드바와 동일한 vibrancy 시뮬레이션
- 제목: 중앙 정렬, SF Pro Display Bold
- 높이: 52pt

### REQ-ANIM-001: 페이지 전환 애니메이션 (Event-Driven)

**WHEN** 사이드바에서 다른 페이지를 선택하면 **THEN** 부드러운 전환 애니메이션을 실행해야 한다.

- 전환 방식: 크로스 페이드 (opacity 0 -> 1)
- 지속 시간: 0.15초
- 이징: ease-in-out
- 60fps 이상 유지

### REQ-ANIM-002: 마이크로 인터랙션 (Ubiquitous)

시스템은 **항상** 다음 마이크로 인터랙션을 제공해야 한다.

- 버튼 호버: 배경색 변화 (0.15초)
- 버튼 클릭: 약간의 축소 효과 (scale 0.98, 0.1초)
- 토글 전환: 슬라이딩 애니메이션 (0.2초)
- 파일 드롭: 바운스 효과 (0.3초)

### REQ-A11Y-001: VoiceOver 접근성 (Ubiquitous)

시스템은 **항상** macOS VoiceOver와 호환되어야 한다.

- 모든 인터랙티브 요소에 접근성 레이블 설정
- 포커스 순서: 논리적 탭 순서 (사이드바 -> 메인 컨텐츠 -> 액션 버튼)
- 상태 변경 시 VoiceOver 알림 (작업 시작/완료)

### REQ-A11Y-002: 키보드 네비게이션 (Ubiquitous)

시스템은 **항상** 키보드만으로 모든 기능에 접근 가능해야 한다.

- Tab: 다음 인터랙티브 요소로 이동
- Shift+Tab: 이전 요소로 이동
- Enter/Space: 버튼 활성화
- Escape: 대화상자 닫기, 작업 취소
- Cmd+1~9: 사이드바 페이지 직접 전환

### REQ-A11Y-003: 고대비 모드 (State-Driven)

**IF** 시스템 고대비 모드가 활성화되어 있으면 **THEN** 모든 UI 요소의 대비를 강화해야 한다.

- 텍스트/배경 대비: WCAG AAA (7:1) 이상
- 포커스 링 강화: 3pt solid accent color
- 아이콘 대비 향상

### REQ-CROSS-001: 크로스 플랫폼 호환성 (State-Driven)

**IF** 실행 환경이 Windows 또는 Linux이면 **THEN** macOS 스타일을 최대한 유사하게 시뮬레이션해야 한다.

- 폰트 폴백: Windows ("Segoe UI"), Linux ("Inter")
- 색상 체계: Apple 색상을 동일하게 적용
- 코너 반지름, 간격: 동일 규격
- 네이티브 요소 차이 허용: 파일 다이얼로그, 스크롤바

---

## Specifications

### SPEC-DESIGN-TOKEN: 디자인 토큰 시스템

현재 `ColorPalette` dataclass와 `constants.py`를 macOS HIG 기반으로 전면 재설계한다.

- `colors.py`: Apple 시스템 색상 팔레트 (SystemColors)로 교체
  - `DARK_PALETTE` / `LIGHT_PALETTE` -> `MACOS_DARK_PALETTE` / `MACOS_LIGHT_PALETTE`
- `constants.py`: Apple HIG 스페이싱/타이포그래피 체계로 교체
  - 패딩 단위: 4px -> 8pt 기반 (Apple 8pt 그리드)
  - 폰트 크기: Apple Dynamic Type 스케일
  - 코너 반지름: 6pt (소), 10pt (중), 14pt (대)
- 새 모듈 `design_tokens.py`: 디자인 토큰 중앙 관리
  - 색상, 타이포그래피, 스페이싱, 애니메이션을 하나로 통합

### SPEC-SIDEBAR: 사이드바 리디자인

현재 `app.py`의 `_create_sidebar()` 메서드를 macOS Finder 스타일로 재설계한다.

- 배경: vibrancy 시뮬레이션 (반투명 + 블러 효과)
- 항목: 아이콘 + 텍스트, rounded rectangle 하이라이트
- 하단: 테마 전환 + 버전 정보
- 신규 위젯: `SidebarItem` (아이콘, 텍스트, 선택 상태 관리)

### SPEC-COMPONENT: 컴포넌트 라이브러리

`widgets/` 디렉토리의 모든 위젯을 macOS 스타일로 재설계한다.

- `file_picker.py` -> macOS 스타일 드래그-앤-드롭 영역
- `progress_bar.py` -> macOS 스피너 + 얇은 진행률 바
- `result_display.py` -> macOS 알림 카드 스타일
- `pdf_preview.py` -> Quick Look 스타일 미리보기
- 신규: `segmented_control.py` (세그먼트 컨트롤)
- 신규: `macos_button.py` (Primary/Secondary/Destructive 버튼)

### SPEC-PAGE: 페이지 레이아웃

9개 페이지 (`*_page_widget.py`)의 레이아웃을 macOS Settings 앱 스타일로 통일한다.

- 상단: 툴바 (제목 중앙, vibrancy 배경)
- 중앙: 컨텐츠 (그룹화된 설정 카드)
- 하단: 액션 바 (실행 버튼, 상태 표시)

### SPEC-ANIMATION: 애니메이션 엔진

CustomTkinter의 `after()` 기반 애니메이션 시스템을 구축한다.

- 페이지 전환: 크로스 페이드 (opacity 애니메이션)
- 버튼 인터랙션: 호버/클릭 효과
- 세그먼트 컨트롤: 슬라이딩 선택 인디케이터
- 프레임워크: `animation.py` 모듈 (easing 함수, 타이머 관리)

### SPEC-ACCESSIBILITY: 접근성 지원

- Tkinter의 접근성 API 활용 (wm_attributes, accessibility labels)
- 키보드 네비게이션 체계 구축
- 포커스 관리 시스템
- 고대비 모드 감지 및 대응

---

## Traceability

| Requirement | Specification | Priority |
|-------------|--------------|----------|
| REQ-THEME-001 | SPEC-DESIGN-TOKEN | Primary Goal |
| REQ-THEME-002 | SPEC-DESIGN-TOKEN | Primary Goal |
| REQ-THEME-003 | SPEC-DESIGN-TOKEN | Primary Goal |
| REQ-COMP-001 | SPEC-SIDEBAR | Primary Goal |
| REQ-COMP-002 | SPEC-COMPONENT | Primary Goal |
| REQ-COMP-003 | SPEC-COMPONENT | Primary Goal |
| REQ-COMP-004 | SPEC-COMPONENT | Secondary Goal |
| REQ-COMP-005 | SPEC-COMPONENT | Primary Goal |
| REQ-COMP-006 | SPEC-COMPONENT | Primary Goal |
| REQ-COMP-007 | SPEC-COMPONENT | Primary Goal |
| REQ-COMP-008 | SPEC-COMPONENT | Secondary Goal |
| REQ-LAYOUT-001 | SPEC-PAGE | Primary Goal |
| REQ-LAYOUT-002 | SPEC-PAGE | Secondary Goal |
| REQ-ANIM-001 | SPEC-ANIMATION | Secondary Goal |
| REQ-ANIM-002 | SPEC-ANIMATION | Optional Goal |
| REQ-A11Y-001 | SPEC-ACCESSIBILITY | Secondary Goal |
| REQ-A11Y-002 | SPEC-ACCESSIBILITY | Primary Goal |
| REQ-A11Y-003 | SPEC-ACCESSIBILITY | Optional Goal |
| REQ-CROSS-001 | SPEC-DESIGN-TOKEN | Primary Goal |
