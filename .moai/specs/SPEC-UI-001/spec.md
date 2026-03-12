---
id: SPEC-UI-001
version: "1.0.0"
status: completed
created: "2026-03-11"
updated: "2026-03-11"
author: taehyunkim
priority: high
issue_number: 0
---

# SPEC-UI-001: Windows GUI Application (CustomTkinter)

## HISTORY

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| 1.0.0 | 2026-03-11 | taehyunkim | 초기 SPEC 작성 |

---

## 1. Environment (환경)

### 1.1 프로젝트 컨텍스트

- **프로젝트**: pdf-tool - Python CLI 기반 PDF 조작 도구
- **현재 아키텍처**: Typer CLI + 8개 커맨드 모듈 (cut, merge, split, rotate, resize, compress, watermark, info)
- **핵심 계층**: `src/pdf_tool/commands/` (비즈니스 로직), `src/pdf_tool/core/` (핵심 서비스), `src/pdf_tool/utils/` (유틸리티)
- **기존 빌드**: PyInstaller 기반 단일 EXE 빌드 (`build_exe.py`)

### 1.2 기술 환경

- **Python**: 3.13+
- **기존 의존성**: pypdf, typer, rich, reportlab, Pillow
- **신규 의존성**: customtkinter (모던 UI 프레임워크)
- **대상 플랫폼**: Windows 10/11
- **패키징**: PyInstaller 단일 EXE

### 1.3 사용자 환경

- PDF 파일 조작이 필요한 일반 사용자 (비개발자 포함)
- CLI에 익숙하지 않은 사용자를 위한 그래픽 인터페이스 제공
- 드래그 앤 드롭 등 직관적 상호작용 기대

---

## 2. Assumptions (가정)

### 2.1 기술적 가정

- A1: CustomTkinter가 Python 3.13+ 환경에서 안정적으로 동작한다
- A2: 기존 `commands/` 계층의 비즈니스 로직을 GUI에서 직접 재사용할 수 있다
- A3: PyInstaller가 CustomTkinter 리소스(테마, 폰트 등)를 단일 EXE로 번들링할 수 있다
- A4: Windows에서 TkinterDnD2 또는 동등한 라이브러리로 드래그 앤 드롭을 구현할 수 있다

### 2.2 비즈니스 가정

- A5: 사용자는 한 번에 하나의 PDF 작업을 수행한다 (동시 다중 작업은 필수가 아님)
- A6: GUI 애플리케이션의 파일 크기가 50MB 이하여야 배포에 적합하다
- A7: 다크 테마가 기본이며, 라이트 테마는 선택 사항이다

### 2.3 제약 조건

- C1: 기존 CLI 인터페이스는 유지해야 하며, GUI는 별도 진입점으로 제공한다
- C2: 기존 `commands/` 및 `core/` 모듈을 수정하지 않고 GUI 계층을 추가한다
- C3: GUI 코드는 `src/pdf_tool/gui/` 디렉터리에 독립적으로 위치한다

---

## 3. Requirements (요구사항)

### 3.1 Ubiquitous (보편적 요구사항)

- **REQ-U-001**: 시스템은 **항상** CustomTkinter 기반의 모던 다크 테마 GUI 윈도우를 제공해야 한다.
- **REQ-U-002**: 시스템은 **항상** 8개 PDF 작업(cut, merge, split, rotate, resize, compress, watermark, info)을 GUI 탭 또는 사이드바 네비게이션을 통해 접근할 수 있도록 해야 한다.
- **REQ-U-003**: 시스템은 **항상** 작업 결과(성공/실패)를 사용자에게 시각적으로 알려야 한다.

### 3.2 Event-Driven (이벤트 기반 요구사항)

- **REQ-E-001**: **WHEN** 사용자가 PDF 파일을 GUI 윈도우에 드래그 앤 드롭하면, **THEN** 시스템은 해당 파일을 로드하고 파일 정보를 표시해야 한다.
- **REQ-E-002**: **WHEN** 사용자가 작업 실행 버튼을 클릭하면, **THEN** 시스템은 선택된 PDF 작업을 해당 파라미터와 함께 실행해야 한다.
- **REQ-E-003**: **WHEN** 사용자가 파일 선택 버튼을 클릭하면, **THEN** 시스템은 OS 파일 선택 다이얼로그를 표시해야 한다.
- **REQ-E-004**: **WHEN** 사용자가 출력 경로를 지정하지 않으면, **THEN** 시스템은 원본 파일과 동일한 디렉터리에 `_output` 접미사를 붙여 저장해야 한다.

### 3.3 State-Driven (상태 기반 요구사항)

- **REQ-S-001**: **IF** PDF 작업이 진행 중이면, **THEN** 시스템은 프로그레스 바와 상태 메시지를 표시하고 실행 버튼을 비활성화해야 한다.
- **REQ-S-002**: **IF** PDF 파일이 로드되지 않은 상태이면, **THEN** 시스템은 작업 실행 버튼을 비활성화하고 파일 로드를 안내해야 한다.
- **REQ-S-003**: **IF** merge 작업 페이지가 활성화된 상태이면, **THEN** 시스템은 다중 파일 선택 및 순서 조정 UI를 표시해야 한다.

### 3.4 Optional (선택적 요구사항)

- **REQ-O-001**: **가능하면** 사용자가 다크/라이트 테마를 전환할 수 있는 토글을 제공한다.
- **REQ-O-002**: **가능하면** 최근 사용한 파일 목록을 표시하여 빠른 재접근을 지원한다.
- **REQ-O-003**: **가능하면** 작업 완료 후 결과 파일을 기본 PDF 뷰어로 열 수 있는 버튼을 제공한다.

### 3.5 Unwanted (금지 요구사항)

- **REQ-N-001**: 시스템은 원본 PDF 파일을 사용자 확인 없이 덮어쓰기**하지 않아야 한다**.
- **REQ-N-002**: 시스템은 지원하지 않는 파일 형식(.docx, .txt 등)을 PDF로 로드**하지 않아야 한다**.
- **REQ-N-003**: **IF** 작업 실행 중 예외가 발생하면, **THEN** 시스템은 무응답 상태로 멈추지 **않아야 하며**, 에러 다이얼로그를 표시하고 안정 상태로 복귀해야 한다.

### 3.6 Complex (복합 요구사항)

- **REQ-C-001**: **IF** 작업 진행 중이고 **AND WHEN** 사용자가 창을 닫으려 하면, **THEN** 시스템은 확인 다이얼로그를 표시하고 사용자 선택에 따라 작업을 중단하거나 대기해야 한다.
- **REQ-C-002**: **IF** watermark 작업이 선택된 상태이고 **AND WHEN** 사용자가 실행을 클릭하면, **THEN** 시스템은 텍스트 또는 이미지 워터마크 유형에 따라 적절한 파라미터 입력 UI를 표시해야 한다.

---

## 4. Specifications (명세)

### 4.1 GUI 구조

```
메인 윈도우 (CTk)
+-- 사이드바 네비게이션 (CTkFrame)
|   +-- 로고/타이틀
|   +-- Cut 버튼
|   +-- Merge 버튼
|   +-- Split 버튼
|   +-- Rotate 버튼
|   +-- Resize 버튼
|   +-- Compress 버튼
|   +-- Watermark 버튼
|   +-- Info 버튼
|   +-- 테마 토글 (선택)
+-- 메인 콘텐츠 영역 (CTkFrame)
    +-- 각 작업별 페이지 (동적 전환)
        +-- 파일 입력 위젯 (드래그 앤 드롭 + 파일 선택)
        +-- 파라미터 입력 위젯 (작업별 상이)
        +-- 실행 버튼 + 프로그레스 바
        +-- 결과 표시 영역
```

### 4.2 모듈 구조

```
src/pdf_tool/gui/
+-- __init__.py
+-- app.py              # CTk 애플리케이션 메인 클래스
+-- theme.py            # 테마 설정 (다크/라이트)
+-- pages/
|   +-- __init__.py
|   +-- base_page.py    # 공통 페이지 베이스 클래스
|   +-- cut_page.py
|   +-- merge_page.py
|   +-- split_page.py
|   +-- rotate_page.py
|   +-- resize_page.py
|   +-- compress_page.py
|   +-- watermark_page.py
|   +-- info_page.py
+-- widgets/
    +-- __init__.py
    +-- file_picker.py    # 파일 선택 + 드래그 앤 드롭
    +-- progress_bar.py   # 진행률 표시
    +-- page_range_input.py  # 페이지 범위 입력
    +-- file_list.py      # 다중 파일 목록 (merge용)
    +-- result_display.py # 결과 표시
```

### 4.3 기존 코드 통합 방식

- GUI 페이지는 `src/pdf_tool/commands/` 모듈의 함수를 직접 호출한다
- 작업은 `threading.Thread`로 실행하여 GUI 멈춤을 방지한다
- 작업 진행/완료 상태는 콜백 또는 이벤트를 통해 메인 스레드에 전달한다

### 4.4 진입점

- CLI 모드: `pdf-tool` (기존 Typer CLI, 변경 없음)
- GUI 모드: `pdf-tool-gui` (새로운 진입점) 또는 `pdf-tool --gui` 플래그

---

## 5. Traceability (추적성)

| 요구사항 ID | 관련 파일 | 우선순위 |
|------------|-----------|---------|
| REQ-U-001 | gui/app.py, gui/theme.py | High |
| REQ-U-002 | gui/pages/*.py | High |
| REQ-U-003 | gui/widgets/result_display.py | High |
| REQ-E-001 | gui/widgets/file_picker.py | High |
| REQ-E-002 | gui/pages/base_page.py | High |
| REQ-E-003 | gui/widgets/file_picker.py | Medium |
| REQ-E-004 | gui/pages/base_page.py | Medium |
| REQ-S-001 | gui/widgets/progress_bar.py | High |
| REQ-S-002 | gui/pages/base_page.py | Medium |
| REQ-S-003 | gui/pages/merge_page.py | Medium |
| REQ-O-001 | gui/theme.py | Low |
| REQ-O-002 | gui/app.py | Low |
| REQ-O-003 | gui/widgets/result_display.py | Low |
| REQ-N-001 | gui/pages/base_page.py | High |
| REQ-N-002 | gui/widgets/file_picker.py | High |
| REQ-N-003 | gui/pages/base_page.py | High |
| REQ-C-001 | gui/app.py | Medium |
| REQ-C-002 | gui/pages/watermark_page.py | Medium |
