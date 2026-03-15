# Changelog

All notable changes to pdf-tool are documented in this file.

Format: [Conventional Changelog](https://conventionalcommits.org)
Versioning: [Semantic Versioning](https://semver.org)

---

## [0.2.1] - 2026-03-16

### Added

- **Progress Callback Framework (SPEC-PDF-003)**
  - ProgressCallback Protocol로 장시간 PDF 작업의 실시간 진행 상황 추적
  - CLI 진행 표시줄 (Rich 라이브러리 통합: 파일 크기, 퍼센트, ETA 표시)
  - GUI 실시간 진행 업데이트 (100ms 인터벌 폴링)
  - ETA (예상 완료 시간) 계산 및 표시 모듈
  - 2초 이상 소요되는 작업에 대해 자동으로 진행 표시

### Features

- **Progress Tracking**:
  - `core/progress.py`: ProgressCallback 타입 및 exception-safe `safe_callback` 래퍼
  - `core/eta.py`: 작업 유형, 파일 크기, 페이지 수 기반 ETA 계산 모듈
  - CLI: Rich progress bar (파일 크기, 퍼센트, ETA 동시 표시)
  - GUI: Determinate ProgressBar 실시간 콜백 업데이트

- **Command Integration**:
  - 8개 PDF 명령어 (cut, merge, split, rotate, resize, compress, watermark, info) 모두 progress callback 지원
  - 하위 호환성 유지: callback 없이도 정상 동작

- **User Experience**:
  - 장시간 작업 (> 2초) 자동 진행 표시
  - 빠른 작업 (< 2초) 조용히 실행
  - CLI 및 GUI 모두 실시간 피드백 제공
  - 예상 완료 시간 (ETA) 표시

### Tests

- 75개 이상의 신규 테스트 (progress callback, ETA 계산, GUI 통합)
- 전체 645개 테스트 모두 통과
- 핵심 progress 모듈 커버리지 98.8%
- 회귀 없음

### Performance

- ETA 계산 오버헤드 최소화 (작업당 < 10ms)
- safe_callback으로 progress callback exception 안전 처리
- 빠른 작업 (< 2초)에 성능 영향 없음

### Notes

- SPEC-PDF-003 Phase 1 & 2 완료
- Phase 3 (메모리 최적화 연구)는 향후 릴리즈 예정

---

## [0.2.0] - 2026-03-15

### Added

- macOS Style UI Redesign (SPEC-UI-MAC-001)
  - Apple Human Interface Guidelines compliant design system
  - Dark/Light mode automatic switching via `darkdetect`
  - 3-section layout standard: toolbar + content + action bar for all 9 pages
  - Animation engine with easing functions (linear, ease-in, ease-out, ease-in-out)
  - Full keyboard navigation: Tab/Shift-Tab focus cycling, Cmd+1~9 page shortcuts
  - Accessibility labels and focus management (VoiceOver compatible)
  - High contrast mode support with automatic system detection
  - Cross-platform compatibility: macOS, Windows, Linux

### Features

- **Design Tokens** (`design_tokens.py`): Apple HIG colors, San Francisco typography scale, 8pt spacing grid, corner radius tokens, animation timing constants
- **Animation Engine** (`animation.py`): `Easing`, `Animation`, `Animator` classes; 60 fps tkinter integration; concurrent animation support
- **Accessibility Module** (`accessibility.py`): `FocusManager`, `AccessibilityLabel`, `AccessibilityManager`, `HighContrastMode`, `KeyboardNavigationMixin`
- **New Widgets**:
  - `macos_button.py`: Primary / Secondary / Destructive styles, Mini / Regular / Large sizes
  - `segmented_control.py`: Capsule-shaped segmented control with state management
  - `sidebar_item.py`: Sidebar navigation item with vibrancy effect and rounded selection
- **9 Pages Unified Layout**: All pages (Cut, Merge, Split, Rotate, Resize, Compress, Watermark, Images to PDF, Info) migrated to 3-section layout
- **Page Transition Animations**: Cross-fade transitions between pages
- **PDF Preview**: Quick Look style preview panel

### Dependencies

- Added: `darkdetect >= 0.8.0` — system dark/light mode detection

### Tests

- 570+ tests covering all new modules and widgets
- 99%+ coverage on core modules (`design_tokens`, `animation`, `accessibility`)
- All 14 acceptance criteria verified (AC-01 through AC-14)

### Notes

- Zero regressions detected; all existing tests continue to pass
- CustomTkinter framework retained (no native Swift UI migration)
- Business logic modules (`commands/`, `core/`) unchanged
- SF Symbols not used (Apple-exclusive license); Unicode equivalents applied

---

## [0.1.x] - Earlier releases

Previous releases covered the initial CLI and GUI implementation.
See git history for detailed change records.
