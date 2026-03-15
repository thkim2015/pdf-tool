# SPEC-UI-MAC-001 구현 전략서

생성일: 2026-03-15
SPEC 버전: 0.2.0
담당: manager-strategy
상태: 승인 대기

---

## 1. 개요

### SPEC 요약

PDF-Tool GUI를 현재 Windows 스타일 (Navy/Purple 색상 체계)에서 macOS Human Interface Guidelines 기반 디자인으로 전면 재설계한다. CustomTkinter 프레임워크를 유지하면서 Apple 색상 체계, SF 타이포그래피, macOS 스타일 컴포넌트를 적용한다.

### 구현 범위

- Apple HIG 기반 디자인 토큰 시스템 구축
- macOS Finder 스타일 사이드바 리디자인
- 6개 공유 위젯 macOS 스타일 적용
- 9개 페이지 레이아웃 통일
- 애니메이션 엔진 구축
- 접근성 (키보드 네비게이션, VoiceOver) 지원

### 범위 제외

- 비즈니스 로직 (commands/, core/) 변경 없음
- BasePage 순수 로직 파일 변경 없음
- CLI 기능 변경 없음
- 네이티브 Swift UI 전환 없음

---

## 2. 현재 아키텍처 분석

### 파일 의존성 맵

```
gui/
├── app.py                         [High Impact - 사이드바 + PageManager]
│   ├── imports: constants, theme
│   ├── contains: PageManager, PDFToolApp
│   └── creates: 9 page widgets, sidebar
│
├── colors.py                      [High Impact - 모든 위젯이 참조]
│   ├── defines: ColorPalette dataclass
│   └── exports: DARK_PALETTE, LIGHT_PALETTE, get_palette()
│
├── constants.py                   [High Impact - 모든 위젯이 참조]
│   ├── defines: 윈도우 크기, 패딩, 폰트, 버튼 높이
│   └── exports: ~50개 상수
│
├── theme.py                       [High Impact - 테마 전환 중앙]
│   ├── imports: colors.py
│   └── exports: apply_theme(), toggle_theme(), get_current_palette()
│
├── pages/
│   ├── base_page.py               [변경 없음 - 순수 로직]
│   ├── base_page_widget.py        [High Impact - 모든 페이지 위젯의 부모]
│   │   ├── imports: app, constants, theme, widgets/*
│   │   └── provides: 공통 레이아웃 (파일입력->파라미터->실행->결과)
│   ├── cut_page.py                [변경 없음 - 순수 로직]
│   ├── cut_page_widget.py         [Medium - base_page_widget 상속]
│   ├── merge_page.py              [변경 없음]
│   ├── merge_page_widget.py       [Medium]
│   ├── split_page.py              [변경 없음]
│   ├── split_page_widget.py       [Medium]
│   ├── rotate_page.py             [변경 없음]
│   ├── rotate_page_widget.py      [Medium]
│   ├── resize_page.py             [변경 없음]
│   ├── resize_page_widget.py      [Medium]
│   ├── compress_page.py           [변경 없음]
│   ├── compress_page_widget.py    [Medium]
│   ├── watermark_page.py          [변경 없음]
│   ├── watermark_page_widget.py   [Medium]
│   ├── image_to_pdf_page.py       [변경 없음]
│   ├── image_to_pdf_page_widget.py [Medium]
│   ├── info_page.py               [변경 없음]
│   └── info_page_widget.py        [Medium]
│
└── widgets/
    ├── file_picker.py             [변경 없음 - 순수 로직]
    ├── file_picker_widget.py      [Medium - macOS 드롭 영역]
    ├── file_list.py               [변경 없음 - 순수 로직]
    ├── file_list_widget.py        [Medium]
    ├── progress_bar.py            [변경 없음 - 순수 로직]
    ├── progress_bar_widget.py     [Medium]
    ├── result_display.py          [변경 없음 - 순수 로직]
    ├── result_display_widget.py   [Medium]
    ├── page_range_input.py        [변경 없음 - 순수 로직]
    ├── page_range_input_widget.py [Low]
    ├── pdf_preview.py             [변경 없음]
    └── pdf_preview_widget.py      [Low]
```

### 핵심 패턴 분석

**BasePage/PageWidget 분리 패턴:**
- `*_page.py`: 순수 로직 (테스트 가능, GUI 의존 없음) -- 변경하지 않음
- `*_page_widget.py`: CustomTkinter 위젯 (BasePageWidget 상속) -- 변경 대상
- `*_widget.py` vs `*.py` (widgets/): 동일 패턴 적용

**현재 테마 시스템:**
- `ColorPalette` dataclass (frozen=True): 19개 필드 (primary, secondary, accent, background, surface, ...)
- `get_palette(theme)` -> DARK/LIGHT 팔레트 반환
- `theme.py`: 글로벌 `_current_theme` 상태 + CustomTkinter appearance mode 연동
- 모든 위젯이 `get_current_palette()`로 색상 참조

**현재 색상 체계 (교체 대상):**
- Dark: Navy Black (#0f172a) 기반 -- Apple Dark (#000000/#1C1C1E)로 교체
- Light: Very Light Slate (#f8fafc) 기반 -- Apple Light (#FFFFFF/#F2F2F7)로 교체
- Primary: Blue (#3b82f6) -- Apple Blue (#007AFF)로 교체

---

## 3. 기술 스택

### 신규 라이브러리

| 라이브러리 | 버전 | 용도 | 선택 근거 |
|-----------|------|------|----------|
| darkdetect | >= 0.8.0 | 시스템 다크모드 자동 감지 | macOS/Windows 네이티브 API 호출, 경량 (의존성 없음), REQ-THEME-003 충족 |

### 기존 라이브러리 (변경 없음)

| 라이브러리 | 현재 버전 | 용도 |
|-----------|----------|------|
| customtkinter | >= 5.2.0 | GUI 프레임워크 |
| Pillow | >= 12.1.1 | 아이콘 렌더링, 블러 효과 시뮬레이션 |
| tkinterdnd2 | >= 0.4.2 | 드래그 앤 드롭 |
| pypdfium2 | >= 4.0.0 | PDF 미리보기 렌더링 |

### 환경 요구사항

- Python: >= 3.13
- macOS: San Francisco 시스템 폰트 사용 (기본 내장)
- Windows: Segoe UI 폴백 (기본 내장)
- Linux: Inter 또는 Cantarell 폴백

---

## 4. TAG 체인 설계

### TAG 목록

```
[TAG-001: Design Tokens] ──→ [TAG-002: Sidebar + Widgets] ──→ [TAG-003: Page Layouts]
                                                                        │
                                                                        ↓
                                                           [TAG-004: Animations]
                                                                        │
                                                                        ↓
                                                           [TAG-005: Accessibility]
```

### TAG-001: 디자인 토큰 시스템 구축

**목적:** Apple HIG 기반 디자인 토큰을 생성하고 기존 colors.py/constants.py를 교체한다.

**범위:**
- 신규: `gui/design_tokens.py` -- 통합 디자인 토큰 (색상, 타이포, 스페이싱, 애니메이션)
- 신규: `gui/icons.py` -- 유니코드 아이콘 매핑 (9개 기능별)
- 수정: `gui/colors.py` -- Apple 시스템 색상으로 팔레트 교체
- 수정: `gui/constants.py` -- Apple 8pt 그리드, SF 폰트 스케일로 교체
- 수정: `gui/theme.py` -- darkdetect 연동, 시스템 테마 자동 감지
- 신규: `tests/test_design_tokens.py`

**완료 조건:**
- 다크/라이트 모드 색상이 Apple HIG 규격과 일치
- 크로스 플랫폼 폰트 폴백 동작 확인
- 디자인 토큰 단위 테스트 95%+ 커버리지
- 기존 테스트 100% 통과 (API 호환성 유지)

**의존성:** 없음 (최초 TAG)

---

### TAG-002: 사이드바 및 공유 위젯 리디자인

**목적:** macOS Finder 스타일 사이드바와 핵심 공유 위젯을 재설계한다.

**범위:**
- 신규: `gui/widgets/sidebar_item.py` -- macOS 사이드바 항목 (아이콘+텍스트, rounded rect 하이라이트)
- 신규: `gui/widgets/macos_button.py` -- Primary/Secondary/Destructive 버튼
- 신규: `gui/widgets/segmented_control.py` -- 세그먼트 컨트롤
- 수정: `gui/app.py` -- `_create_sidebar()` 재작성 (SidebarItem 사용)
- 수정: `gui/widgets/file_picker_widget.py` -- macOS dashed border 드롭 영역
- 수정: `gui/widgets/progress_bar_widget.py` -- 4pt 높이 진행률 바
- 수정: `gui/widgets/result_display_widget.py` -- macOS 알림 카드 스타일
- 수정: `gui/widgets/pdf_preview_widget.py` -- Quick Look 스타일
- 신규: `tests/test_macos_widgets.py`

**완료 조건:**
- 사이드바 네비게이션 정상 동작
- 모든 위젯 유닛 테스트 85%+ 커버리지
- 키보드 네비게이션 (Tab/Shift+Tab) 동작
- 버튼 호버/클릭/비활성 상태 시각 피드백

**의존성:** TAG-001 (디자인 토큰 필요)

---

### TAG-003: 9개 페이지 레이아웃 통일

**목적:** 모든 작업 페이지를 macOS Settings 스타일로 통일한다.

**범위:**
- 수정: `gui/pages/base_page_widget.py` -- macOS 레이아웃 표준 (툴바+컨텐츠+액션바)
- 수정: 9개 `*_page_widget.py` 파일:
  - `cut_page_widget.py`
  - `merge_page_widget.py`
  - `split_page_widget.py`
  - `rotate_page_widget.py` (세그먼트 컨트롤 적용)
  - `resize_page_widget.py` (세그먼트 컨트롤 + 드롭다운 적용)
  - `compress_page_widget.py`
  - `watermark_page_widget.py`
  - `image_to_pdf_page_widget.py`
  - `info_page_widget.py`

**완료 조건:**
- 9개 페이지 동일한 레이아웃 구조 (상단 제목/중앙 컨텐츠/하단 액션바)
- 기존 기능 100% 정상 동작 (회귀 테스트 통과)
- 페이지 전환 정상 동작

**의존성:** TAG-002 (공유 위젯 필요)

---

### TAG-004: 애니메이션 엔진

**목적:** CustomTkinter after() 기반 애니메이션 시스템을 구축한다.

**범위:**
- 신규: `gui/animation.py` -- 애니메이션 엔진
  - Easing 함수: ease_in, ease_out, ease_in_out, spring
  - AnimationTimer: after() 기반 프레임 스케줄러
  - PropertyAnimator: opacity, position, color 속성 애니메이션
- 수정: `gui/app.py` -- PageManager에 크로스 페이드 전환 연동
- 수정: `gui/widgets/macos_button.py` -- 호버/클릭 마이크로 인터랙션
- 수정: `gui/widgets/segmented_control.py` -- 슬라이딩 선택 인디케이터
- 신규: `tests/test_animation.py`

**완료 조건:**
- 페이지 전환 크로스 페이드 (0.15초) 동작
- 버튼 호버 효과 (0.15초) 동작
- 애니메이션 엔진 단위 테스트 85%+ 커버리지
- 메모리 누수 없음 (after 콜백 정리)

**의존성:** TAG-003 (페이지 레이아웃 완성 후 적용)

---

### TAG-005: 접근성 완성

**목적:** VoiceOver 호환성, 키보드 네비게이션, 고대비 모드를 완성한다.

**범위:**
- 수정: 모든 위젯 파일 -- 접근성 레이블 추가
- 수정: `gui/app.py` -- Cmd+1~9 단축키, 포커스 관리
- 수정: `gui/theme.py` -- 고대비 모드 감지 및 대응
- 수정: `gui/pages/base_page_widget.py` -- Tab 순서 정의

**완료 조건:**
- 키보드만으로 모든 기능 접근 가능
- Cmd+1~9 페이지 전환 동작
- WCAG AA 대비 기준 충족
- 포커스 링 시각 효과 동작

**의존성:** TAG-004 (모든 위젯/페이지 완성 후)

---

## 5. 단계별 구현 계획

### Phase 1: 디자인 토큰 시스템 (TAG-001)

**목표:** macOS HIG 기반 디자인 파운데이션 구축

**태스크 분해:**

| Task ID | 설명 | 요구사항 매핑 | 의존성 | 수락 기준 |
|---------|------|-------------|--------|----------|
| TASK-001 | `design_tokens.py` 생성: Apple 시스템 색상, SF 타이포, 8pt 그리드, 애니메이션 타이밍, 코너 반지름 | REQ-THEME-001, REQ-THEME-002 | 없음 | 단위 테스트 통과, 다크/라이트 색상 Apple HIG 일치 |
| TASK-002 | `colors.py` 업데이트: DARK_PALETTE/LIGHT_PALETTE를 Apple 색상으로 교체 | REQ-THEME-001 | TASK-001 | ColorPalette API 호환성 유지, 기존 테스트 통과 |
| TASK-003 | `constants.py` 업데이트: 8pt 그리드 패딩, SF 폰트 스케일, Apple 코너 반지름 | REQ-THEME-002, REQ-LAYOUT-001 | TASK-001 | 상수 이름 호환성 유지, 기존 import 깨지지 않음 |
| TASK-004 | `theme.py` 업데이트: darkdetect 연동, 시스템 테마 자동 감지, 동적 전환 | REQ-THEME-003 | TASK-002 | 시스템 테마 변경 시 자동 전환, darkdetect 없으면 graceful fallback |
| TASK-005 | `icons.py` 생성: 9개 기능별 유니코드 아이콘 매핑, 다크/라이트 색상 | REQ-COMP-001 | TASK-001 | 모든 아이콘 렌더링 확인 |
| TASK-006 | `tests/test_design_tokens.py` 작성 | 전체 | TASK-001~005 | 커버리지 95%+ |

**변경 파일 (6개):**
- 신규: `gui/design_tokens.py`, `gui/icons.py`, `tests/test_design_tokens.py`
- 수정: `gui/colors.py`, `gui/constants.py`, `gui/theme.py`

**핵심 설계 결정:**
- `ColorPalette` dataclass API 유지 (하위 호환): 필드 추가는 허용, 기존 필드 삭제 금지
- `design_tokens.py`는 `colors.py` + `constants.py`를 통합하는 상위 모듈로 동작
- `darkdetect`가 없는 환경에서는 수동 토글만 지원 (import 실패 시 graceful degradation)
- 기존 `FONT_FAMILY_DEFAULT = "System"`은 플랫폼 감지로 교체:
  - macOS: `"SF Pro Text"` / `"SF Pro Display"`
  - Windows: `"Segoe UI"`
  - Linux: `"Inter"` -> `"Cantarell"` -> `"Sans"`

---

### Phase 2: 사이드바 및 공유 위젯 (TAG-002)

**목표:** macOS 네이티브 스타일 컴포넌트 라이브러리 구축

**태스크 분해:**

| Task ID | 설명 | 요구사항 매핑 | 의존성 | 수락 기준 |
|---------|------|-------------|--------|----------|
| TASK-007 | `widgets/sidebar_item.py` 생성: 아이콘+텍스트, rounded rect 하이라이트, 호버 효과 | REQ-COMP-001 | TAG-001 | 선택 상태 시각 피드백, 호버 효과 동작 |
| TASK-008 | `widgets/macos_button.py` 생성: Primary/Secondary/Destructive, 호버/눌림/비활성 상태 | REQ-COMP-002 | TAG-001 | 3가지 버튼 타입, 4가지 상태 동작 |
| TASK-009 | `widgets/segmented_control.py` 생성: 캡슐 형태, 선택 인디케이터 | REQ-COMP-004 | TAG-001 | 다중 세그먼트 선택 동작, 값 반환 |
| TASK-010 | `app.py` 사이드바 리디자인: SidebarItem 사용, vibrancy 시뮬레이션, 하단 테마 전환 | REQ-COMP-001, REQ-LAYOUT-002 | TASK-007, TASK-008 | 사이드바 네비게이션, 페이지 전환 정상 |
| TASK-011 | `widgets/file_picker_widget.py` macOS 스타일: dashed border 드롭 영역, 드래그 오버 하이라이트 | REQ-COMP-005 | TAG-001 | dashed 보더, 드래그 오버 효과, 파일 정보 표시 |
| TASK-012 | `widgets/progress_bar_widget.py` macOS 스타일: 4pt 높이 바, accent color | REQ-COMP-006 | TAG-001 | 얇은 진행률 바, 애니메이션 동작 |
| TASK-013 | `widgets/result_display_widget.py` macOS 알림 카드: 둥근 모서리, 아이콘+메시지 | REQ-COMP-007 | TAG-001, TASK-008 | 성공/실패 카드 스타일, Finder 열기 버튼 |
| TASK-014 | `widgets/pdf_preview_widget.py` Quick Look 스타일 | REQ-COMP-008 | TAG-001 | 둥근 모서리 썸네일, 페이지 정보 표시 |
| TASK-015 | `tests/test_macos_widgets.py` 작성 | 전체 | TASK-007~014 | 커버리지 85%+ |

**변경 파일 (9개):**
- 신규: `gui/widgets/sidebar_item.py`, `gui/widgets/macos_button.py`, `gui/widgets/segmented_control.py`, `tests/test_macos_widgets.py`
- 수정: `gui/app.py`, `gui/widgets/file_picker_widget.py`, `gui/widgets/progress_bar_widget.py`, `gui/widgets/result_display_widget.py`, `gui/widgets/pdf_preview_widget.py`

---

### Phase 3: 9개 페이지 레이아웃 통일 (TAG-003)

**목표:** 모든 작업 페이지를 macOS Settings 스타일로 통일

**태스크 분해:**

| Task ID | 설명 | 요구사항 매핑 | 의존성 | 수락 기준 |
|---------|------|-------------|--------|----------|
| TASK-016 | `base_page_widget.py` macOS 레이아웃: 툴바(제목)+컨텐츠(스크롤)+액션바(실행 버튼) | REQ-LAYOUT-001, REQ-LAYOUT-002 | TAG-002 | 3단 레이아웃, macOS 버튼 사용 |
| TASK-017 | `cut_page_widget.py` macOS 스타일 적용 | REQ-LAYOUT-001 | TASK-016 | 동일 레이아웃, 기능 정상 |
| TASK-018 | `merge_page_widget.py` macOS 스타일 적용 | REQ-LAYOUT-001 | TASK-016 | 파일 리스트 + 순서 변경 정상 |
| TASK-019 | `split_page_widget.py` macOS 스타일 + 세그먼트 컨트롤 | REQ-LAYOUT-001, REQ-COMP-004 | TASK-016, TASK-009 | 분할 옵션 세그먼트 동작 |
| TASK-020 | `rotate_page_widget.py` macOS 스타일 + 세그먼트 컨트롤 | REQ-LAYOUT-001, REQ-COMP-004 | TASK-016, TASK-009 | 회전 각도 세그먼트 동작 |
| TASK-021 | `resize_page_widget.py` macOS 스타일 + 세그먼트/드롭다운 | REQ-LAYOUT-001, REQ-COMP-004 | TASK-016, TASK-009 | 용지 크기/모드 선택 정상 |
| TASK-022 | `compress_page_widget.py` macOS 스타일 적용 | REQ-LAYOUT-001 | TASK-016 | 압축 옵션 정상 |
| TASK-023 | `watermark_page_widget.py` macOS 스타일 적용 | REQ-LAYOUT-001 | TASK-016 | 워터마크 설정 카드 정상 |
| TASK-024 | `image_to_pdf_page_widget.py` macOS 스타일 적용 | REQ-LAYOUT-001 | TASK-016 | 이미지 리스트 + 옵션 정상 |
| TASK-025 | `info_page_widget.py` macOS 스타일 적용 | REQ-LAYOUT-001 | TASK-016 | 메타데이터 테이블 정상 |

**변경 파일 (10개):**
- 수정: `gui/pages/base_page_widget.py` + 9개 `*_page_widget.py`

---

### Phase 4: 애니메이션 엔진 (TAG-004)

**목표:** 부드러운 전환 효과와 마이크로 인터랙션

**태스크 분해:**

| Task ID | 설명 | 요구사항 매핑 | 의존성 | 수락 기준 |
|---------|------|-------------|--------|----------|
| TASK-026 | `animation.py` 엔진: easing 함수, AnimationTimer, PropertyAnimator | REQ-ANIM-001, REQ-ANIM-002 | TAG-003 | 단위 테스트 85%+, 메모리 누수 없음 |
| TASK-027 | PageManager 크로스 페이드: opacity 0->1, 0.15초, ease-in-out | REQ-ANIM-001 | TASK-026 | 페이지 전환 시 페이드 동작, 60fps 목표 |
| TASK-028 | 버튼 마이크로 인터랙션: 호버 배경 전환, 클릭 미세 축소 | REQ-ANIM-002 | TASK-026 | 시각적 피드백 동작 |
| TASK-029 | `tests/test_animation.py` 작성 | 전체 | TASK-026~028 | 커버리지 85%+ |

**변경 파일 (4개):**
- 신규: `gui/animation.py`, `tests/test_animation.py`
- 수정: `gui/app.py` (PageManager), `gui/widgets/macos_button.py`

---

### Phase 5: 접근성 완성 (TAG-005)

**목표:** VoiceOver, 키보드 네비게이션, 고대비 모드

**태스크 분해:**

| Task ID | 설명 | 요구사항 매핑 | 의존성 | 수락 기준 |
|---------|------|-------------|--------|----------|
| TASK-030 | 접근성 레이블: 모든 인터랙티브 요소에 label 설정 | REQ-A11Y-001 | TAG-004 | VoiceOver에서 모든 요소 읽힘 |
| TASK-031 | 키보드 네비게이션: Tab 순서, Cmd+1~9, Escape | REQ-A11Y-002 | TAG-004 | 키보드만으로 전체 기능 접근 |
| TASK-032 | 고대비 모드: 시스템 감지, 강화된 색상/테두리 | REQ-A11Y-003 | TASK-030 | WCAG AAA (7:1) 대비 달성 |
| TASK-033 | 포커스 관리: 포커스 링 시각 효과, 포커스 트래핑 | REQ-A11Y-002 | TASK-031 | 3pt 포커스 링 표시 |

**변경 파일 (다수):**
- 수정: 모든 위젯 파일 (접근성 레이블), `gui/app.py`, `gui/theme.py`, `gui/pages/base_page_widget.py`

---

## 6. 리스크 및 대응

### 기술 리스크

| 리스크 | 영향도 | 발생 확률 | 대응 계획 |
|--------|--------|----------|----------|
| CustomTkinter 스타일링 한계 (vibrancy 효과 불가) | High | High | Canvas 기반 커스텀 렌더링, Pillow 블러 시뮬레이션. 70% macOS 유사도 수용 |
| 크로스 플랫폼 폰트 렌더링 차이 | Medium | Medium | 플랫폼 감지 유틸 (sys.platform), 폰트 폴백 체인, 크기 보정 계수 |
| after() 애니메이션 60fps 미달 | Medium | Medium | 적응형 프레임 레이트, 저성능 환경에서 애니메이션 비활성화 옵션 |
| 기존 GUI 테스트 파괴 | High | Medium | ColorPalette API 호환성 유지, 필드 추가만 허용 (삭제 금지) |
| Windows EXE 빌드 실패 | Medium | Low | 각 Phase 후 PyInstaller 빌드 검증, build_exe.py 업데이트 |
| darkdetect 패키지 미설치 환경 | Low | Low | try/except import, 수동 토글 폴백 |

### 호환성 리스크

| 항목 | 전략 |
|------|------|
| ColorPalette dataclass | 기존 19개 필드 유지 + 신규 필드 추가 (vibrancy_bg 등). `frozen=True` 유지 |
| constants.py 상수 이름 | 기존 상수 이름 유지, 값만 Apple HIG 규격으로 변경 |
| theme.py API | `apply_theme()`, `toggle_theme()`, `get_current_palette()` 시그니처 유지 |
| BasePageWidget | 인터페이스 (`create_params_ui`, `execute_command`) 변경 없음 |

### 롤백 전략

- Phase별 git 커밋으로 롤백 지점 확보
- Phase 1은 기존 colors.py/constants.py 값 교체만이므로 git revert로 즉시 롤백 가능
- Phase 2-3은 신규 파일 추가 + 기존 파일 수정이므로 git revert 또는 branch 분리
- 각 Phase 완료 후 기존 전체 테스트 실행하여 회귀 확인

---

## 7. 승인 요청

### 핵심 결정 사항

1. **프레임워크 유지**: CustomTkinter를 유지하면서 macOS 스타일을 시뮬레이션한다
   - 대안 A: PyObjC + Swift UI (macOS 전용, Windows 포기)
   - 대안 B: PySide6/PyQt6 (대규모 의존성 100MB+, 라이선스 복잡)
   - **권장: 현행 CustomTkinter 유지** (코드 자산 활용, 크로스 플랫폼)

2. **신규 의존성**: darkdetect >= 0.8.0 추가
   - 경량 패키지 (의존성 없음), macOS/Windows 네이티브 API
   - 설치 불가 시 graceful fallback

3. **API 호환성**: ColorPalette dataclass 확장 (필드 추가만, 삭제 없음)
   - 기존 코드가 참조하는 19개 필드 유지
   - 신규 필드 (vibrancy 관련) 추가

4. **macOS 유사도 목표**: 70% 이상
   - 완벽한 네이티브 느낌은 CustomTkinter 한계로 불가
   - 색상, 타이포, 레이아웃, 코너 반지름으로 시각적 유사도 확보

### 승인 체크리스트

- [ ] 기술 스택 승인 (CustomTkinter 유지 + darkdetect 추가)
- [ ] TAG 체인 승인 (5단계 순차 실행)
- [ ] 구현 순서 승인 (토큰 -> 위젯 -> 페이지 -> 애니메이션 -> 접근성)
- [ ] 리스크 대응 계획 승인
- [ ] macOS 유사도 70% 목표 승인

---

## 8. 다음 단계

승인 후 manager-ddd에게 다음 정보를 전달합니다:

- **TAG 체인**: TAG-001 ~ TAG-005 (의존성 순서)
- **라이브러리 버전**: darkdetect >= 0.8.0 (신규), 기존 유지
- **핵심 결정**: CustomTkinter 유지, ColorPalette API 호환, 70% macOS 유사도
- **태스크 목록**: TASK-001 ~ TASK-033 (의존성 포함)
- **리스크 대응**: Phase별 빌드 검증, API 호환성 유지, graceful degradation

---

## 변경 파일 총 요약

### 신규 파일 (9개)

| 파일 | 용도 |
|------|------|
| `gui/design_tokens.py` | 디자인 토큰 통합 관리 |
| `gui/icons.py` | 유니코드 아이콘 매핑 |
| `gui/animation.py` | 애니메이션 엔진 |
| `gui/widgets/sidebar_item.py` | macOS 사이드바 항목 |
| `gui/widgets/macos_button.py` | macOS 스타일 버튼 |
| `gui/widgets/segmented_control.py` | 세그먼트 컨트롤 |
| `tests/test_design_tokens.py` | 디자인 토큰 테스트 |
| `tests/test_macos_widgets.py` | macOS 위젯 테스트 |
| `tests/test_animation.py` | 애니메이션 테스트 |

### 수정 파일 (17개)

| 파일 | 변경 내용 |
|------|----------|
| `gui/colors.py` | Apple 색상 체계로 교체 |
| `gui/constants.py` | Apple HIG 스페이싱/폰트 교체 |
| `gui/theme.py` | darkdetect 연동, 동적 전환 |
| `gui/app.py` | 사이드바 리디자인, 애니메이션 연동 |
| `gui/pages/base_page_widget.py` | macOS 레이아웃 표준화 |
| `gui/pages/cut_page_widget.py` | macOS 스타일 적용 |
| `gui/pages/merge_page_widget.py` | macOS 스타일 적용 |
| `gui/pages/split_page_widget.py` | macOS 스타일 + 세그먼트 |
| `gui/pages/rotate_page_widget.py` | macOS 스타일 + 세그먼트 |
| `gui/pages/resize_page_widget.py` | macOS 스타일 + 세그먼트/드롭다운 |
| `gui/pages/compress_page_widget.py` | macOS 스타일 적용 |
| `gui/pages/watermark_page_widget.py` | macOS 스타일 적용 |
| `gui/pages/image_to_pdf_page_widget.py` | macOS 스타일 적용 |
| `gui/pages/info_page_widget.py` | macOS 스타일 적용 |
| `gui/widgets/file_picker_widget.py` | macOS 드롭 영역 |
| `gui/widgets/progress_bar_widget.py` | macOS 프로그레스 |
| `gui/widgets/result_display_widget.py` | macOS 알림 카드 |

### 변경 없는 파일 (순수 로직)

`base_page.py`, `cut_page.py`, `merge_page.py`, `split_page.py`, `rotate_page.py`, `resize_page.py`, `compress_page.py`, `watermark_page.py`, `image_to_pdf_page.py`, `info_page.py`, `file_picker.py`, `file_list.py`, `progress_bar.py`, `result_display.py`, `page_range_input.py`, `pdf_preview.py`

### pyproject.toml 변경

```toml
[project.optional-dependencies]
gui = [
    "customtkinter>=5.2.0",
    "tkinterdnd2>=0.4.2",
    "pypdfium2>=4.0.0",
    "darkdetect>=0.8.0",  # 신규 추가
]
```

---

총 변경 파일: 26개 (신규 9 + 수정 17)
총 태스크: 33개 (TASK-001 ~ TASK-033)
예상 코드 변경량: ~3,000줄 (신규) + ~2,000줄 (수정)
