---
id: SPEC-UI-002
version: "1.0.0"
status: completed
created: "2026-03-12"
updated: "2026-03-12"
author: taehyunkim
priority: medium
issue_number: 0
---

# SPEC-UI-002: PDF Preview (결과 PDF 미리보기)

## HISTORY

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|-----------|
| 1.0.0 | 2026-03-12 | taehyunkim | 초기 SPEC 작성 |

---

## 1. Environment (환경)

### 1.1 프로젝트 컨텍스트

- **프로젝트**: pdf-tool - Python CLI + GUI 기반 PDF 조작 도구
- **현재 아키텍처**: CustomTkinter GUI (SPEC-UI-001 구현 완료) + 8개 작업 페이지
- **핵심 계층**: `src/pdf_tool/gui/pages/` (페이지), `src/pdf_tool/gui/widgets/` (위젯)
- **기존 결과 표시**: `ResultDisplayWidget` - 텍스트 기반 성공/에러/정보 메시지 표시

### 1.2 기술 환경

- **Python**: 3.13+
- **GUI 프레임워크**: CustomTkinter (다크/라이트 테마)
- **기존 의존성**: pypdf, typer, rich, reportlab, Pillow, customtkinter
- **신규 의존성**: `pypdfium2` (PDF 페이지 렌더링, 경량 순수 Python 바인딩)
- **대상 플랫폼**: Windows 10/11, macOS, Linux

### 1.3 사용자 환경

- GUI를 통해 PDF 작업을 수행하는 일반 사용자
- 작업 완료 후 결과 PDF의 내용을 시각적으로 확인하고 싶은 사용자
- 결과 파일이 올바르게 생성되었는지 빠르게 검증하려는 사용자

---

## 2. Assumptions (가정)

### 2.1 기술적 가정

- A1: `pypdfium2`가 Python 3.13+ 환경에서 안정적으로 동작한다
- A2: `pypdfium2`는 시스템 의존성 없이 pip 설치만으로 사용 가능하다 (순수 Python 바인딩)
- A3: `pypdfium2`로 PDF 첫 번째 페이지를 PIL Image로 렌더링할 수 있다
- A4: `CTkImage(light_image, dark_image, size)` + `CTkLabel(image=...)` 조합으로 썸네일을 표시할 수 있다
- A5: 대부분의 PDF 파일에서 첫 페이지 렌더링이 1초 이내에 완료된다

### 2.2 비즈니스 가정

- A6: 사용자는 첫 번째 페이지만 미리보기로 충분하다 (전체 페이지 탐색은 불필요)
- A7: 미리보기 썸네일 크기는 약 300x400px이 적절하다
- A8: info 작업은 출력 파일이 없으므로 미리보기 대상에서 제외한다

### 2.3 제약 조건

- C1: 기존 `commands/`, `core/`, `utils/`, `cli.py`를 수정하지 **않는다**
- C2: GUI 코드는 `src/pdf_tool/gui/` 디렉터리에만 위치한다
- C3: 미리보기 렌더링은 GUI 스레드를 차단하지 **않는다** (백그라운드 스레드 필수)
- C4: 코드 주석은 한국어로 작성한다
- C5: info 페이지는 출력 파일이 없으므로 미리보기를 건너뛴다

---

## 3. Requirements (요구사항)

### 3.1 Ubiquitous (보편적 요구사항)

- **REQ-U-001**: 시스템은 **항상** 성공적인 PDF 작업 완료 후 결과 PDF의 첫 번째 페이지를 썸네일 이미지로 결과 영역에 표시해야 한다.

### 3.2 Event-Driven (이벤트 기반 요구사항)

- **REQ-E-001**: **WHEN** 작업이 성공적으로 완료되고 **AND** 출력이 PDF 파일이면, **THEN** 시스템은 첫 번째 페이지를 썸네일 이미지로 렌더링하여 결과 영역에 표시해야 한다.
- **REQ-E-002**: **WHEN** 사용자가 미리보기 이미지를 클릭하면, **THEN** 시스템은 해당 PDF 파일을 시스템 기본 PDF 뷰어로 열어야 한다.

### 3.3 State-Driven (상태 기반 요구사항)

- **REQ-S-001**: **IF** 미리보기 렌더링이 진행 중이면, **THEN** 시스템은 로딩 인디케이터(스피너 또는 "미리보기 로딩 중..." 텍스트)를 표시해야 한다.
- **REQ-S-002**: **IF** 미리보기 렌더링이 실패하면 (손상된 PDF 등), **THEN** 시스템은 미리보기 없이 텍스트 결과만 표시해야 한다 (우아한 폴백).

### 3.4 Optional (선택적 요구사항)

- **REQ-O-001**: **가능하면** 사용자가 미리보기 이미지를 클릭하여 시스템 기본 뷰어에서 전체 PDF를 열 수 있도록 한다.

### 3.5 Unwanted (금지 요구사항)

- **REQ-N-001**: 시스템은 PDF의 모든 페이지를 렌더링**하지 않아야 한다** (첫 번째 페이지만 렌더링).
- **REQ-N-002**: 시스템은 미리보기 렌더링 중 UI를 차단**하지 않아야 한다**.
- **REQ-N-003**: 시스템은 info 작업 결과에 대해 미리보기를 표시**하지 않아야 한다** (출력 파일 없음).

### 3.6 Complex (복합 요구사항)

- **REQ-C-001**: **IF** 새로운 작업이 시작된 상태이고 **AND WHEN** 이전 미리보기 렌더링이 아직 진행 중이면, **THEN** 시스템은 이전 렌더링을 취소하고 결과 영역을 초기화해야 한다.

---

## 4. Specifications (명세)

### 4.1 아키텍처 설계

```
결과 표시 영역 (ResultDisplayWidget 확장)
+-- 텍스트 결과 영역 (기존)
|   +-- 성공: 녹색 "완료!" + 출력 파일 경로
|   +-- 에러: 빨간색 에러 메시지
|   +-- 정보: Key-Value 테이블 (info_page 전용)
+-- 미리보기 영역 (신규)
    +-- 로딩 상태: "미리보기 로딩 중..." 텍스트
    +-- 성공 상태: CTkImage 썸네일 (클릭 시 PDF 열기)
    +-- 실패 상태: 미리보기 숨김 (텍스트 결과만 표시)
```

### 4.2 모듈 구조

```
src/pdf_tool/gui/
+-- widgets/
    +-- pdf_preview.py           # 순수 로직: PDF -> PIL Image 렌더링
    +-- pdf_preview_widget.py    # CTk 위젯: 썸네일 표시 + 클릭 이벤트
    +-- result_display_widget.py # 기존 위젯 확장: 미리보기 영역 추가
    +-- result_display.py        # 기존 순수 로직 (변경 없음)
```

### 4.3 렌더링 파이프라인

```
작업 완료 (메인 스레드)
  |
  v
_on_success(result, output_path) 호출
  |
  v
output_path가 .pdf인지 확인
  |-- 아니오 --> 텍스트 결과만 표시
  |-- 예 -->
      |
      v
  백그라운드 스레드에서 렌더링 시작
  + 로딩 인디케이터 표시
      |
      v
  pypdfium2로 첫 페이지 -> PIL Image 변환
      |
      v
  widget.after()로 메인 스레드에 전달
      |
      v
  CTkImage 생성 + CTkLabel에 표시
```

### 4.4 기술 스택

| 컴포넌트 | 라이브러리 | 용도 |
|----------|-----------|------|
| PDF 렌더링 | `pypdfium2` | PDF 첫 페이지 -> PIL Image 변환 |
| 이미지 처리 | `Pillow` (기존) | PIL Image 리사이즈, CTkImage 생성 |
| 위젯 표시 | `customtkinter` (기존) | CTkImage + CTkLabel로 썸네일 표시 |
| 파일 열기 | `subprocess` (표준 라이브러리) | 시스템 기본 PDF 뷰어로 열기 |

### 4.5 pypdfium2 렌더링 방식

```python
# pdf_preview.py 핵심 로직 (개념)
import pypdfium2 as pdfium
from PIL import Image

def render_first_page(pdf_path: str, max_width: int = 300) -> Image.Image:
    """PDF 첫 번째 페이지를 PIL Image로 렌더링한다."""
    pdf = pdfium.PdfDocument(pdf_path)
    page = pdf[0]
    # 적절한 스케일로 렌더링
    bitmap = page.render(scale=2.0)
    pil_image = bitmap.to_pil()
    # 비율 유지하면서 리사이즈
    pil_image.thumbnail((max_width, max_width * 1.4))
    return pil_image
```

### 4.6 pyproject.toml 변경

```toml
[project.optional-dependencies]
gui = [
    "customtkinter>=5.2.0",
    "tkinterdnd2>=0.4.2",
    "pypdfium2>=4.0.0",   # 신규: PDF 페이지 렌더링
]
```

---

## 5. Traceability (추적성)

| 요구사항 ID | 관련 파일 | 우선순위 |
|------------|-----------|---------|
| REQ-U-001 | gui/widgets/pdf_preview.py, gui/widgets/pdf_preview_widget.py | High |
| REQ-E-001 | gui/widgets/pdf_preview.py, gui/widgets/result_display_widget.py | High |
| REQ-E-002 | gui/widgets/pdf_preview_widget.py | Medium |
| REQ-S-001 | gui/widgets/pdf_preview_widget.py | Medium |
| REQ-S-002 | gui/widgets/pdf_preview_widget.py, gui/widgets/result_display_widget.py | High |
| REQ-O-001 | gui/widgets/pdf_preview_widget.py | Low |
| REQ-N-001 | gui/widgets/pdf_preview.py | High |
| REQ-N-002 | gui/widgets/pdf_preview.py, gui/pages/base_page_widget.py | High |
| REQ-N-003 | gui/pages/base_page_widget.py | Medium |
| REQ-C-001 | gui/widgets/pdf_preview_widget.py, gui/widgets/result_display_widget.py | Medium |
