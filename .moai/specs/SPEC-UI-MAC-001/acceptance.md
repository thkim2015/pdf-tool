# SPEC-UI-MAC-001: Acceptance Criteria

## SPEC Reference

| Field | Value |
|-------|-------|
| SPEC ID | SPEC-UI-MAC-001 |
| Title | macOS Style UI Redesign |
| Version | 0.2.0 |

---

## Acceptance Criteria

### AC-01: Apple 색상 체계 적용

**Given** pdf-tool GUI가 macOS에서 실행될 때
**When** 다크 모드로 설정하면
**Then** 배경색이 Apple systemBackground (#000000 또는 #1C1C1E)으로 표시되어야 한다
**And** 액센트 컬러가 Apple Blue (#007AFF)로 표시되어야 한다
**And** 상태 색상 (성공, 경고, 에러)이 Apple 표준 색상을 사용해야 한다

**Given** pdf-tool GUI가 macOS에서 실행될 때
**When** 라이트 모드로 설정하면
**Then** 배경색이 Apple systemBackground (#FFFFFF 또는 #F2F2F7)으로 표시되어야 한다
**And** 모든 텍스트가 Apple label 색상 체계를 따라야 한다

---

### AC-02: San Francisco 타이포그래피

**Given** pdf-tool GUI가 macOS에서 실행될 때
**When** 어떤 페이지든 열면
**Then** 제목은 SF Pro Display (또는 시스템 기본) 22pt Bold로 표시되어야 한다
**And** 본문 텍스트는 SF Pro Text (또는 시스템 기본) 17pt Regular로 표시되어야 한다
**And** 보조 텍스트는 secondaryLabel 색상으로 표시되어야 한다

**Given** pdf-tool GUI가 Windows에서 실행될 때
**When** 어떤 페이지든 열면
**Then** 폰트가 "Segoe UI"로 폴백되어야 한다
**And** 레이아웃이 macOS와 동일한 구조를 유지해야 한다

---

### AC-03: 다크/라이트 모드 전환

**Given** pdf-tool GUI가 다크 모드에서 실행 중일 때
**When** 테마 전환 버튼을 클릭하면
**Then** 0.3초 이내에 모든 UI 요소가 라이트 모드로 전환되어야 한다
**And** 사이드바, 메인 영역, 버튼, 입력 필드 모두 동시에 전환되어야 한다
**And** 현재 진행 중인 작업에 영향이 없어야 한다

**Given** macOS 시스템 설정에서 다크 모드를 변경할 때
**When** pdf-tool GUI가 실행 중이면
**Then** 자동으로 시스템 테마에 맞게 전환되어야 한다

---

### AC-04: macOS 스타일 사이드바

**Given** pdf-tool GUI가 실행될 때
**When** 사이드바가 표시되면
**Then** 각 네비게이션 항목이 아이콘 + 텍스트 조합으로 표시되어야 한다
**And** 선택된 항목이 rounded rectangle 하이라이트로 표시되어야 한다
**And** 마우스 호버 시 배경색이 미세하게 변해야 한다
**And** 사이드바 배경이 메인 영역과 구분되는 톤이어야 한다

---

### AC-05: macOS 스타일 버튼

**Given** pdf-tool GUI의 어떤 페이지에서
**When** Primary 버튼 (실행 버튼)이 표시되면
**Then** Apple accent color (#007AFF) 배경에 흰색 텍스트로 표시되어야 한다
**And** 코너 반지름이 6pt이어야 한다
**And** 마우스 호버 시 배경색이 약간 어두워져야 한다

**Given** 버튼이 비활성 상태일 때
**When** 파일이 로드되지 않은 상태이면
**Then** 버튼 opacity가 0.5로 표시되어야 한다
**And** 클릭이 무시되어야 한다

---

### AC-06: 파일 드래그-앤-드롭 영역

**Given** pdf-tool GUI의 파일 입력이 필요한 페이지에서
**When** 파일 드롭 영역이 표시되면
**Then** dashed 보더 (2pt)와 12pt 코너 반지름으로 표시되어야 한다
**And** 문서 아이콘과 안내 텍스트가 중앙에 표시되어야 한다

**Given** 파일을 드래그하여 드롭 영역 위로 올릴 때
**When** 드래그 오버 상태가 되면
**Then** 보더 색상이 accent color로 변경되어야 한다
**And** 배경에 accent color 10% opacity가 적용되어야 한다

**Given** PDF 파일을 드롭 영역에 놓으면
**When** 유효한 PDF 파일이면
**Then** 파일 이름과 크기가 표시되어야 한다
**And** 파일 제거 버튼이 표시되어야 한다

---

### AC-07: 진행률 표시

**Given** 사용자가 PDF 작업을 실행할 때
**When** 작업이 진행 중이면
**Then** macOS 스타일 진행률 표시기가 표시되어야 한다
**And** 진행률 바 높이가 4pt이어야 한다
**And** 진행률 바 색상이 accent color이어야 한다

---

### AC-08: 작업 결과 표시

**Given** PDF 작업이 성공적으로 완료될 때
**When** 결과가 표시되면
**Then** 초록색 체크 아이콘과 "완료" 텍스트가 표시되어야 한다
**And** 출력 파일 경로가 표시되어야 한다
**And** 결과 카드가 둥근 모서리 (12pt)로 표시되어야 한다

**Given** PDF 작업이 실패할 때
**When** 에러가 표시되면
**Then** 빨간색 X 아이콘과 에러 메시지가 표시되어야 한다

---

### AC-09: 9개 페이지 레이아웃 통일

**Given** pdf-tool GUI에서 어떤 페이지든 열 때
**When** 페이지가 표시되면
**Then** 상단에 제목 영역이 표시되어야 한다
**And** 중앙에 컨텐츠 영역이 있어야 한다
**And** 하단에 실행 버튼이 포함된 액션 바가 있어야 한다
**And** 9개 페이지 모두 동일한 레이아웃 구조를 따라야 한다

---

### AC-10: 페이지 전환 애니메이션

**Given** pdf-tool GUI에서 사이드바 항목을 클릭할 때
**When** 다른 페이지로 전환하면
**Then** 크로스 페이드 애니메이션이 실행되어야 한다
**And** 전환 시간이 0.15초 이내여야 한다
**And** 애니메이션 중 프레임 드롭이 눈에 띄지 않아야 한다

---

### AC-11: 키보드 네비게이션

**Given** pdf-tool GUI가 실행 중일 때
**When** Tab 키를 누르면
**Then** 포커스가 논리적 순서대로 다음 인터랙티브 요소로 이동해야 한다

**Given** pdf-tool GUI가 실행 중일 때
**When** Cmd+1 (macOS) 또는 Ctrl+1 (Windows)을 누르면
**Then** 첫 번째 페이지 (Cut)로 전환되어야 한다
**And** Cmd+9 / Ctrl+9는 마지막 페이지 (Info)로 전환되어야 한다

---

### AC-12: 크로스 플랫폼 호환성

**Given** pdf-tool GUI가 Windows에서 실행될 때
**When** 어떤 페이지든 열면
**Then** macOS와 동일한 색상 체계가 적용되어야 한다
**And** 동일한 레이아웃 구조가 유지되어야 한다
**And** 폰트만 시스템 기본 (Segoe UI)으로 폴백되어야 한다

---

### AC-13: 기존 기능 회귀 없음

**Given** macOS 스타일 UI가 적용된 후
**When** 모든 PDF 작업 (Cut, Merge, Split, Rotate, Resize, Compress, Watermark, Images to PDF, Info)을 실행하면
**Then** 기존과 동일한 결과를 생성해야 한다
**And** 기존 CLI 기능에 영향이 없어야 한다
**And** 기존 비즈니스 로직 테스트가 100% 통과해야 한다

---

### AC-14: PDF 미리보기

**Given** PDF 작업이 성공적으로 완료된 후
**When** 결과 PDF 미리보기가 표시되면
**Then** Quick Look 스타일 (둥근 모서리 8pt, 가벼운 그림자)로 렌더링되어야 한다
**And** 페이지 수와 파일 크기 정보가 하단에 표시되어야 한다

---

## Quality Gate Criteria

### 테스트 커버리지

| 영역 | 최소 커버리지 | 검증 방법 |
|------|-------------|----------|
| 디자인 토큰 (design_tokens.py) | 95% | pytest + pytest-cov |
| 애니메이션 엔진 (animation.py) | 85% | pytest (타이밍 mock) |
| 신규 위젯 (widgets/*) | 85% | pytest (CustomTkinter mock) |
| 페이지 위젯 (*_page_widget.py) | 80% | pytest (기존 테스트 확장) |
| 전체 gui/ 패키지 | >= 85% | pytest-cov |

### 성능 기준

| 지표 | 기준값 | 검증 방법 |
|------|--------|----------|
| 앱 시작 시간 | < 2초 | 타이머 측정 |
| 페이지 전환 | < 0.2초 | 프레임 타이밍 |
| 메모리 사용량 | < 150MB | 프로파일러 |
| 애니메이션 FPS | >= 50fps (macOS) | 프레임 카운터 |

### 코드 품질

| 기준 | 조건 | 도구 |
|------|------|------|
| Lint 에러 | 0개 | ruff |
| Type 에러 | 0개 | mypy |
| 코드 복잡도 | 함수당 <= 15 | ruff (C901) |
| 라인 길이 | <= 99자 | ruff |

---

## Verification Methods

### 자동화 테스트

1. **단위 테스트**: pytest로 모든 디자인 토큰, 애니메이션 엔진, 위젯 로직 검증
2. **회귀 테스트**: 기존 22개 테스트 파일 전체 통과 확인
3. **커버리지 리포트**: `pytest --cov=pdf_tool.gui --cov-report=html`

### 수동 검증

1. **시각적 검증**: macOS/Windows에서 스크린샷 비교
2. **접근성 검증**: macOS VoiceOver로 전체 워크플로우 탐색
3. **키보드 검증**: 키보드만으로 모든 기능 접근 테스트
4. **성능 검증**: 페이지 전환 시 프레임 드롭 확인

### 빌드 검증

1. **Windows EXE**: PyInstaller 빌드 성공 및 실행 확인
2. **macOS**: 직접 실행 (`python -m pdf_tool gui`) 정상 확인
3. **Linux**: 기본 기능 동작 확인

---

## Definition of Done

- [ ] 모든 Acceptance Criteria (AC-01 ~ AC-14) 충족
- [ ] 전체 테스트 커버리지 >= 85%
- [ ] ruff lint 에러 0개
- [ ] mypy type 에러 0개
- [ ] macOS에서 시각적 검증 통과
- [ ] Windows에서 시각적 검증 통과
- [ ] 키보드 네비게이션 전체 기능 접근 가능
- [ ] Windows EXE 빌드 성공
- [ ] 기존 비즈니스 로직 테스트 100% 통과
- [ ] 기존 CLI 기능 영향 없음 확인
