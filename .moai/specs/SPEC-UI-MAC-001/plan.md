# SPEC-UI-MAC-001: Implementation Plan

## SPEC Reference

| Field | Value |
|-------|-------|
| SPEC ID | SPEC-UI-MAC-001 |
| Title | macOS Style UI Redesign |
| Version | 0.2.0 |

---

## Technical Approach

### Architecture Decision: Enhanced CustomTkinter (Selected)

**평가된 대안:**

| 옵션 | 장점 | 단점 | 판정 |
|------|------|------|------|
| PyObjC + Swift UI | 완벽한 네이티브 느낌 | macOS 전용, Windows 포기 | 부적합 |
| PySide6/PyQt6 | 강력한 위젯, QSS 스타일링 | 대규모 의존성 (100MB+), 라이선스 복잡 | 부적합 |
| Enhanced CustomTkinter | 기존 코드 활용, 크로스 플랫폼 | 네이티브 느낌 한계 | **채택** |
| Dear PyGui | 고성능 렌더링 | GUI 패러다임 완전 변경 | 부적합 |

**채택 근거:**
1. 기존 CustomTkinter 코드 자산 활용 (BasePage/PageWidget 패턴 유지)
2. Windows EXE 배포 호환성 유지
3. 디자인 토큰 교체만으로 80%의 시각적 변화 달성 가능
4. 추가 의존성 최소화

### 신규 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| darkdetect | >= 0.8.0 | 시스템 다크모드 감지 |
| Pillow | >= 12.1.1 (기존) | 아이콘 렌더링, 블러 효과 |

### 파일 변경 범위

**수정 대상 (기존 파일):**

| 파일 | 변경 내용 | 영향도 |
|------|----------|--------|
| `gui/colors.py` | Apple 색상 체계로 전면 교체 | High |
| `gui/constants.py` | Apple HIG 스페이싱/폰트로 교체 | High |
| `gui/theme.py` | 시스템 테마 감지, 동적 전환 | Medium |
| `gui/app.py` | 사이드바 리디자인, 레이아웃 변경 | High |
| `gui/pages/base_page_widget.py` | macOS 레이아웃 표준화 | High |
| `gui/pages/*_page_widget.py` (9개) | macOS 스타일 적용 | Medium |
| `gui/widgets/file_picker.py` | macOS 드롭 영역 스타일 | Medium |
| `gui/widgets/progress_bar.py` | macOS 프로그레스 스타일 | Low |
| `gui/widgets/result_display.py` | macOS 알림 카드 스타일 | Medium |
| `gui/widgets/pdf_preview.py` | Quick Look 스타일 | Low |
| `gui/widgets/pdf_preview_widget.py` | Quick Look 위젯 | Low |

**신규 파일:**

| 파일 | 용도 |
|------|------|
| `gui/design_tokens.py` | 디자인 토큰 통합 관리 (색상, 타이포, 스페이싱) |
| `gui/animation.py` | 애니메이션 엔진 (easing, 타이머) |
| `gui/widgets/sidebar_item.py` | macOS 사이드바 항목 위젯 |
| `gui/widgets/macos_button.py` | macOS 스타일 버튼 (Primary/Secondary/Destructive) |
| `gui/widgets/segmented_control.py` | macOS 세그먼트 컨트롤 |
| `gui/icons.py` | 유니코드/SVG 아이콘 매핑 |
| `tests/test_design_tokens.py` | 디자인 토큰 테스트 |
| `tests/test_animation.py` | 애니메이션 엔진 테스트 |
| `tests/test_macos_widgets.py` | macOS 위젯 테스트 |

---

## Milestones

### Primary Goal: 디자인 토큰 및 테마 시스템 (Phase 1)

macOS HIG 기반의 디자인 토큰 시스템 구축 및 기존 색상/상수 교체.

**Tasks:**

1. `design_tokens.py` 생성
   - Apple 시스템 색상 팔레트 (SystemColors dataclass)
   - SF Pro 타이포그래피 스케일 + 크로스 플랫폼 폰트 폴백
   - 8pt 그리드 기반 스페이싱 시스템
   - 애니메이션 타이밍 상수
   - 코너 반지름 체계 (6pt/10pt/14pt)

2. `colors.py` 업데이트
   - `DARK_PALETTE` -> Apple 다크 모드 색상으로 교체
   - `LIGHT_PALETTE` -> Apple 라이트 모드 색상으로 교체
   - ColorPalette dataclass 필드 확장 (vibrancy 색상 추가)

3. `constants.py` 업데이트
   - 패딩: 8pt 그리드 체계
   - 폰트 크기: Apple Dynamic Type 스케일
   - 코너 반지름: Apple HIG 규격

4. `theme.py` 업데이트
   - `darkdetect` 연동 시스템 테마 자동 감지
   - 동적 테마 전환 (전체 위젯 실시간 업데이트)

5. `icons.py` 생성
   - 9개 기능별 아이콘 매핑 (유니코드 기반)
   - 다크/라이트 모드별 아이콘 색상

**검증 기준:**
- 디자인 토큰 단위 테스트 통과
- 다크/라이트 모드 색상 정확성 확인
- 크로스 플랫폼 폰트 폴백 동작 확인

---

### Primary Goal: 사이드바 및 컴포넌트 리디자인 (Phase 2)

macOS Finder 스타일 사이드바 및 핵심 위젯 재설계.

**Tasks:**

1. `widgets/sidebar_item.py` 생성
   - 아이콘 + 텍스트 레이아웃
   - 선택 상태: rounded rectangle 하이라이트
   - 호버 효과: 배경색 미세 변화
   - 접근성: 키보드 네비게이션 지원

2. `widgets/macos_button.py` 생성
   - Primary: accent color 배경, 흰색 텍스트
   - Secondary: 시스템 회색 배경
   - Destructive: 빨간색 배경
   - 호버/눌림/비활성 상태

3. `app.py` 사이드바 리디자인
   - `_create_sidebar()` 전면 재작성
   - `SidebarItem` 위젯 사용
   - vibrancy 시뮬레이션 배경
   - 하단: 테마 전환 + 앱 정보

4. `widgets/file_picker.py` macOS 스타일
   - dashed border 드롭 영역
   - 드래그 오버 하이라이트 효과
   - 파일 정보 카드 표시

5. `widgets/progress_bar.py` macOS 스타일
   - 얇은 진행률 바 (4pt 높이)
   - macOS 스피너 애니메이션

6. `widgets/result_display.py` macOS 알림 카드
   - 둥근 모서리 카드 레이아웃
   - 성공/실패 아이콘 + 메시지

7. `widgets/segmented_control.py` 생성 (신규)
   - 캡슐 형태 세그먼트
   - 슬라이딩 선택 인디케이터
   - Rotate/Resize 페이지에서 사용

**검증 기준:**
- 모든 위젯 유닛 테스트
- 사이드바 네비게이션 동작 확인
- 키보드 네비게이션 테스트

---

### Primary Goal: 9개 페이지 레이아웃 통일 (Phase 3)

모든 작업 페이지를 macOS Settings 스타일로 통일.

**Tasks:**

1. `pages/base_page_widget.py` macOS 레이아웃 표준화
   - 상단 툴바 영역 (제목, vibrancy 배경)
   - 중앙 컨텐츠 영역 (스크롤 가능)
   - 하단 액션 바 (실행 버튼, 상태)

2. 9개 페이지 위젯 업데이트
   - `cut_page_widget.py`: 파일 선택 + 페이지 범위 입력
   - `merge_page_widget.py`: 파일 리스트 + 순서 변경
   - `split_page_widget.py`: 분할 옵션 세그먼트 컨트롤
   - `rotate_page_widget.py`: 회전 각도 세그먼트 컨트롤
   - `resize_page_widget.py`: 용지 크기 드롭다운 + 모드 세그먼트
   - `compress_page_widget.py`: 압축 옵션
   - `watermark_page_widget.py`: 워터마크 설정 카드
   - `image_to_pdf_page_widget.py`: 이미지 리스트 + 옵션
   - `info_page_widget.py`: 메타데이터 테이블

**검증 기준:**
- 9개 페이지 모두 동일한 레이아웃 구조
- 기존 기능 정상 동작 확인
- 회귀 테스트 전체 통과

---

### Secondary Goal: 애니메이션 및 폴리싱 (Phase 4)

부드러운 전환 효과와 마이크로 인터랙션 구현.

**Tasks:**

1. `animation.py` 애니메이션 엔진 구축
   - Easing 함수: ease-in, ease-out, ease-in-out, spring
   - 타이머 관리: `after()` 기반 프레임 스케줄러
   - 속성 애니메이션: opacity, position, size, color

2. 페이지 전환 애니메이션
   - PageManager에 크로스 페이드 연동
   - 0.15초 전환, 60fps 목표

3. 버튼 마이크로 인터랙션
   - 호버: 배경색 전환 (0.15초)
   - 클릭: 미세 축소 효과

4. 세그먼트 컨트롤 슬라이딩 애니메이션

**검증 기준:**
- 애니메이션 프레임 드롭 없음 (60fps 이상)
- 애니메이션 엔진 단위 테스트
- 메모리 누수 없음

---

### Secondary Goal: 접근성 완성 (Phase 5)

VoiceOver 호환성 및 키보드 네비게이션 완성.

**Tasks:**

1. 접근성 레이블 설정
   - 모든 버튼, 입력 필드, 드롭다운에 접근성 레이블
   - 상태 변경 알림

2. 키보드 네비게이션 체계
   - Tab 순서 정의
   - Cmd+1~9 단축키
   - Escape 동작

3. 고대비 모드 대응
   - 시스템 고대비 감지
   - 강화된 색상/테두리

4. 포커스 관리
   - 포커스 링 시각 효과
   - 포커스 트래핑 (모달 대화상자)

**검증 기준:**
- VoiceOver 기본 동작 확인
- 키보드만으로 전체 기능 접근 가능
- WCAG AA 대비 기준 충족

---

## Risks and Mitigation

### Risk 1: CustomTkinter의 스타일링 한계 (Impact: High)

- **위험**: CustomTkinter는 CSS/QSS 수준의 스타일링을 지원하지 않아 macOS 네이티브 수준 달성이 어려울 수 있음
- **대응**: Canvas 기반 커스텀 렌더링으로 부족한 부분 보완. vibrancy 효과는 Pillow 블러 처리로 시뮬레이션
- **수용 기준**: 70% 이상의 macOS 스타일 유사도 달성

### Risk 2: 크로스 플랫폼 일관성 (Impact: Medium)

- **위험**: macOS/Windows/Linux 간 렌더링 차이 (폰트, DPI, 테마)
- **대응**: 플랫폼별 폰트 폴백 체계, DPI 스케일링 처리, 플랫폼 감지 유틸리티
- **수용 기준**: 3개 플랫폼에서 동일한 레이아웃 구조 유지

### Risk 3: 애니메이션 성능 (Impact: Medium)

- **위험**: CustomTkinter의 `after()` 기반 애니메이션이 60fps를 보장하지 못할 수 있음
- **대응**: 애니메이션 프레임 드롭 감지 및 적응형 프레임 레이트, 저성능 환경에서 애니메이션 비활성화 옵션
- **수용 기준**: macOS에서 평균 50fps 이상, 최소 30fps

### Risk 4: 기존 테스트 깨짐 (Impact: High)

- **위험**: 위젯 구조 변경으로 기존 22개 테스트 파일 중 GUI 관련 테스트 실패 가능
- **대응**: 로직/위젯 분리 패턴 유지 (BasePage 순수 로직은 변경 없음), 위젯 테스트만 업데이트
- **수용 기준**: 기존 비즈니스 로직 테스트 100% 통과, GUI 테스트 업데이트

### Risk 5: Windows EXE 빌드 호환성 (Impact: Medium)

- **위험**: 신규 위젯/애니메이션이 PyInstaller 빌드에서 문제 발생 가능
- **대응**: 각 Phase 완료 후 Windows EXE 빌드 검증, `build_exe.py` 필요 시 업데이트
- **수용 기준**: Windows EXE 빌드 및 실행 정상

---

## Architecture Design Direction

```
GUI Layer (macOS Style)
├── design_tokens.py       # 디자인 토큰 (색상, 폰트, 스페이싱)
├── animation.py           # 애니메이션 엔진
├── icons.py               # 아이콘 매핑
├── colors.py              # Apple 색상 팔레트 (기존 파일 수정)
├── constants.py           # Apple HIG 상수 (기존 파일 수정)
├── theme.py               # 테마 관리 + 시스템 감지 (기존 파일 수정)
├── app.py                 # 메인 윈도우 + macOS 사이드바 (기존 파일 수정)
├── pages/
│   ├── base_page_widget.py  # macOS 레이아웃 베이스 (기존 파일 수정)
│   └── *_page_widget.py     # 9개 페이지 (기존 파일 수정)
└── widgets/
    ├── sidebar_item.py      # macOS 사이드바 항목 (신규)
    ├── macos_button.py      # macOS 버튼 (신규)
    ├── segmented_control.py # 세그먼트 컨트롤 (신규)
    ├── file_picker.py       # macOS 드롭 영역 (기존 수정)
    ├── progress_bar.py      # macOS 프로그레스 (기존 수정)
    ├── result_display.py    # macOS 알림 카드 (기존 수정)
    └── pdf_preview*.py      # Quick Look 스타일 (기존 수정)
```

**핵심 원칙:**
- 로직 레이어 (commands/, core/) 변경 없음
- BasePage 순수 로직 변경 없음
- 위젯 레이어만 교체/확장
- 디자인 토큰 기반 일관성 보장
