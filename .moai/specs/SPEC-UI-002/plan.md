---
id: SPEC-UI-002
type: plan
---

# SPEC-UI-002 구현 계획: PDF Preview (결과 PDF 미리보기)

## 1. 개요

기존 GUI 애플리케이션의 결과 표시 영역에 PDF 미리보기 기능을 추가한다. 작업 성공 후 결과 PDF의 첫 번째 페이지를 썸네일로 렌더링하여 사용자가 결과를 시각적으로 확인할 수 있도록 한다.

---

## 2. 의존성 변경

### 2.1 신규 의존성

| 패키지 | 용도 | 비고 |
|--------|------|------|
| `pypdfium2>=4.0.0` | PDF 페이지 -> PIL Image 렌더링 | 경량, 시스템 의존성 없음, 크로스 플랫폼 |
| `Pillow` (기존) | 이미지 리사이즈 및 CTkImage 생성 | 이미 설치됨 |

### 2.2 라이브러리 선택 근거

| 후보 | 장점 | 단점 | 결정 |
|------|------|------|------|
| `pypdfium2` | 경량, 순수 Python 바인딩, 시스템 의존성 없음, 크로스 플랫폼 | pdfium 바이너리 포함으로 패키지 크기 약간 큼 | **채택** |
| `PyMuPDF/fitz` | 고성능, 풍부한 기능 | 무거운 C 라이브러리, AGPL 라이선스 | 제외 |
| `pdf2image` | 간단한 API | poppler 시스템 의존성 필요, Windows 설치 어려움 | 제외 |

### 2.3 pyproject.toml 변경

```toml
[project.optional-dependencies]
gui = [
    "customtkinter>=5.2.0",
    "tkinterdnd2>=0.4.2",
    "pypdfium2>=4.0.0",   # PDF 페이지 렌더링
]
```

---

## 3. 모듈 구조

### 3.1 신규 파일

```
src/pdf_tool/gui/widgets/
+-- pdf_preview.py           # 순수 로직: PDF -> PIL Image 렌더링
+-- pdf_preview_widget.py    # CTk 위젯: 썸네일 표시 + 로딩 + 클릭 이벤트
```

### 3.2 수정 파일

```
src/pdf_tool/gui/widgets/
+-- result_display_widget.py  # 미리보기 영역 추가 (기존 텍스트 결과 아래)

src/pdf_tool/gui/pages/
+-- base_page_widget.py       # _on_success()에서 미리보기 트리거 추가
```

### 3.3 변경하지 않는 파일

- `src/pdf_tool/gui/widgets/result_display.py` (순수 로직 - 변경 불필요)
- `src/pdf_tool/commands/*` (비즈니스 로직 - 제약 C1)
- `src/pdf_tool/core/*` (핵심 서비스 - 제약 C1)
- `src/pdf_tool/utils/*` (유틸리티 - 제약 C1)
- `src/pdf_tool/cli.py` (CLI 진입점 - 제약 C1)

### 3.4 아키텍처 통합

```
기존 결과 흐름                     신규 미리보기 흐름
+---------------------+           +-------------------------+
| base_page_widget.py |           | pdf_preview.py          |
|   _on_success()     | --------> |   render_first_page()   |
|                     |           |   (백그라운드 스레드)     |
+---------------------+           +-------------------------+
        |                                    |
        v                                    v
+---------------------+           +-------------------------+
| result_display      |           | pdf_preview_widget.py   |
|   _widget.py        |           |   PdfPreviewWidget      |
|   텍스트 결과 표시    |           |   썸네일 이미지 표시     |
+---------------------+           +-------------------------+
```

---

## 4. 마일스톤

### Primary Goal: PDF 렌더링 엔진 + 위젯

- [ ] `gui/widgets/pdf_preview.py`: pypdfium2 기반 PDF -> PIL Image 렌더링 로직
  - 첫 번째 페이지만 렌더링
  - 비율 유지 리사이즈 (max_width 파라미터)
  - 에러 핸들링 (손상 PDF, 빈 PDF 등)
- [ ] `gui/widgets/pdf_preview_widget.py`: CTk 미리보기 위젯
  - CTkImage + CTkLabel 기반 썸네일 표시
  - 로딩 인디케이터 표시/숨김
  - 렌더링 실패 시 우아한 폴백
  - 이미지 클릭 시 PDF 열기 이벤트
- [ ] `pyproject.toml`: gui 의존성에 `pypdfium2>=4.0.0` 추가

### Secondary Goal: 기존 위젯 통합

- [ ] `gui/widgets/result_display_widget.py` 확장: 텍스트 결과 아래에 미리보기 영역 추가
  - 미리보기 위젯 임베드
  - 성공 시 미리보기 트리거
  - 새 작업 시작 시 미리보기 초기화
- [ ] `gui/pages/base_page_widget.py` 수정: `_on_success()`에서 미리보기 플로우 트리거
  - output_path가 .pdf 확장자인지 확인
  - 백그라운드 스레드에서 렌더링 시작
  - info_page 제외 로직

### Final Goal: 품질 및 에지 케이스

- [ ] 백그라운드 렌더링 취소 로직 (새 작업 시작 시 이전 렌더링 취소)
- [ ] 대용량 PDF 렌더링 타임아웃 처리
- [ ] 단위 테스트: `pdf_preview.py` 렌더링 로직 테스트
- [ ] 통합 테스트: 미리보기 플로우 전체 검증

### Optional Goal: 사용성 개선

- [ ] 미리보기 이미지 클릭 시 시스템 기본 PDF 뷰어로 열기
- [ ] 미리보기 이미지에 마우스 호버 시 "클릭하여 열기" 툴팁

---

## 5. 기술적 접근 방식

### 5.1 렌더링 스레딩 전략

```
메인 스레드 (GUI)                  워커 스레드 (렌더링)
+-------------------------+       +---------------------------+
| 1. _on_success() 호출    |       |                           |
| 2. 로딩 인디케이터 표시   |       |                           |
| 3. 렌더링 스레드 시작 -->  |------>| 4. pypdfium2 렌더링 실행  |
|                         |       | 5. PIL Image 생성          |
| 7. CTkImage 생성 + 표시  |<------| 6. widget.after() 콜백    |
+-------------------------+       +---------------------------+
```

- `threading.Thread(target=render_preview, daemon=True)`로 렌더링 실행
- `widget.after(0, callback)` 메서드로 GUI 스레드에서 안전하게 이미지 표시
- 렌더링 실패 시 폴백 콜백으로 로딩 인디케이터 숨김

### 5.2 이미지 표시 패턴

```python
# CTkImage를 사용한 테마 호환 이미지 표시 (개념)
from customtkinter import CTkImage, CTkLabel
from PIL import Image

# 다크/라이트 테마 모두 동일한 이미지 사용
ctk_image = CTkImage(
    light_image=pil_image,
    dark_image=pil_image,
    size=(width, height)
)
label = CTkLabel(parent, image=ctk_image, text="")
```

### 5.3 시스템 뷰어 열기

```python
import subprocess
import sys

def open_pdf_in_viewer(pdf_path: str) -> None:
    """시스템 기본 PDF 뷰어로 파일을 연다."""
    if sys.platform == "win32":
        subprocess.Popen(["start", "", pdf_path], shell=True)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", pdf_path])
    else:
        subprocess.Popen(["xdg-open", pdf_path])
```

### 5.4 에러 핸들링 전략

| 에러 상황 | 대응 방안 |
|-----------|----------|
| pypdfium2 미설치 | `ImportError` 캐치 -> 미리보기 기능 비활성화 (텍스트 결과만) |
| 손상된 PDF | 렌더링 예외 캐치 -> 폴백 (텍스트 결과만 표시) |
| 빈 PDF (0 페이지) | 페이지 수 확인 -> 폴백 |
| 렌더링 중 새 작업 시작 | 이전 렌더링 스레드 무시 (결과 콜백에서 유효성 검사) |
| 메모리 부족 (대용량 PDF) | 낮은 스케일로 렌더링 재시도, 최종 폴백 |

---

## 6. 리스크 분석

### 중간 위험

| 리스크 | 영향 | 대응 방안 |
|--------|------|-----------|
| pypdfium2 렌더링 속도 저하 (대용량 PDF) | 로딩 시간 길어짐 | 타임아웃 설정 (5초), 폴백 처리 |
| pypdfium2 + PyInstaller 번들링 이슈 | EXE에서 렌더링 실패 | `--collect-all pypdfium2` 옵션 사용, ImportError 폴백 |

### 낮은 위험

| 리스크 | 영향 | 대응 방안 |
|--------|------|-----------|
| CTkImage 메모리 누수 | 장시간 사용 시 메모리 증가 | 이전 CTkImage 참조 해제, 가비지 컬렉션 |
| 렌더링 스레드 경합 | 빠른 연속 작업 시 이미지 겹침 | 렌더링 ID로 유효성 검사, 최신 결과만 표시 |
| EXE 파일 크기 증가 | pypdfium2 바이너리 포함으로 크기 증가 | 기존 50MB 제한 내 유지 가능 (pypdfium2 약 15MB) |

---

## 7. 아키텍처 설계 방향

### 7.1 계층 분리 원칙

- **순수 로직 계층** (`pdf_preview.py`): PDF 렌더링 로직만 담당, GUI 의존성 없음
- **위젯 계층** (`pdf_preview_widget.py`): CTk 위젯으로 이미지 표시, 이벤트 처리
- **통합 계층** (`result_display_widget.py`): 기존 텍스트 결과 + 미리보기 통합

### 7.2 확장성

- 향후 다중 페이지 미리보기 (페이지 네비게이션) 추가 가능
- 미리보기 크기 조절 (확대/축소) 기능 확장 가능
- 다른 파일 형식 미리보기 (이미지 등) 확장 가능

---

## 8. 다음 단계

1. `/moai:2-run SPEC-UI-002` 명령으로 구현 시작
2. Primary Goal 완료 후 Secondary Goal 진행
3. 구현 완료 후 `/moai:3-sync SPEC-UI-002`로 문서화
