---
id: SPEC-UI-001
type: plan
---

# SPEC-UI-001 구현 계획: Windows GUI Application (CustomTkinter)

## 1. 개요

기존 pdf-tool CLI 애플리케이션에 CustomTkinter 기반의 모던 GUI를 추가한다. 기존 비즈니스 로직(`commands/`, `core/`)을 수정 없이 재사용하며, GUI 계층을 독립 모듈로 구성한다.

---

## 2. 의존성 변경

### 2.1 신규 의존성

| 패키지 | 용도 | 비고 |
|--------|------|------|
| `customtkinter` | 모던 다크 테마 GUI 프레임워크 | tkinter 기반, pip 설치 |
| `tkinterdnd2` | 드래그 앤 드롭 지원 | Windows 파일 드롭 기능 |
| `Pillow` (기존) | 아이콘/이미지 리소스 처리 | 이미 설치됨 |

### 2.2 pyproject.toml 변경

```toml
[project.optional-dependencies]
gui = [
    "customtkinter>=5.2.0",
    "tkinterdnd2>=0.4.2",
]

[project.scripts]
pdf-tool = "pdf_tool.cli:app"
pdf-tool-gui = "pdf_tool.gui.app:main"
```

---

## 3. 모듈 구조

### 3.1 신규 디렉터리

```
src/pdf_tool/gui/
+-- __init__.py
+-- app.py              # CTk 메인 애플리케이션 클래스, 진입점
+-- theme.py            # 테마 설정 및 전환 로직
+-- pages/
|   +-- __init__.py
|   +-- base_page.py    # 공통 페이지 베이스 (파일 입력, 실행, 결과 표시)
|   +-- cut_page.py     # 페이지 범위 지정 PDF 추출
|   +-- merge_page.py   # 다중 PDF 병합 (파일 목록 + 순서 조정)
|   +-- split_page.py   # PDF 분할
|   +-- rotate_page.py  # 페이지 회전 (각도 선택)
|   +-- resize_page.py  # 페이지 크기 변경 (용지 크기 선택)
|   +-- compress_page.py # PDF 압축 (품질 레벨 선택)
|   +-- watermark_page.py # 워터마크 추가 (텍스트/이미지 선택)
|   +-- info_page.py    # PDF 메타데이터 표시
+-- widgets/
    +-- __init__.py
    +-- file_picker.py    # 파일 선택 + 드래그 앤 드롭 영역
    +-- progress_bar.py   # 진행률 표시 위젯
    +-- page_range_input.py  # 페이지 범위 입력 (예: "1-5, 8, 10-12")
    +-- file_list.py      # 다중 파일 목록 관리 (추가, 제거, 순서 변경)
    +-- result_display.py # 작업 결과 표시 (성공/실패 + 파일 열기)
```

### 3.2 기존 코드와의 통합 구조

```
GUI Layer (신규)                    Business Logic Layer (기존, 변경 없음)
+-------------------+              +----------------------------+
| gui/pages/        |  직접 호출   | commands/cut.py            |
|   cut_page.py     | ----------> |   execute_cut()            |
|   merge_page.py   | ----------> | commands/merge.py          |
|   ...             |              |   execute_merge()          |
+-------------------+              +----------------------------+
| gui/widgets/      |              | core/page_range.py         |
|   file_picker.py  |              | core/validators.py         |
|   progress_bar.py |              | core/pdf_handler.py        |
+-------------------+              +----------------------------+
```

- GUI는 `commands/` 모듈의 기존 함수를 `threading.Thread`로 래핑하여 호출
- 결과 및 에러는 콜백 함수를 통해 메인(GUI) 스레드로 전달
- `core/` 모듈의 유효성 검증(validators), 페이지 범위 파싱(page_range) 등을 그대로 활용

---

## 4. 마일스톤

### Primary Goal: 핵심 GUI 프레임 구축

- [ ] `gui/app.py`: CTk 메인 윈도우 + 사이드바 네비게이션 구현
- [ ] `gui/theme.py`: 다크 테마 기본 설정
- [ ] `gui/pages/base_page.py`: 공통 페이지 베이스 클래스 (파일 입력, 실행 버튼, 결과 영역)
- [ ] `gui/widgets/file_picker.py`: 파일 선택 다이얼로그 + 드래그 앤 드롭
- [ ] `gui/widgets/progress_bar.py`: 프로그레스 바 위젯
- [ ] `pyproject.toml`: gui 선택 의존성 및 진입점 추가

### Secondary Goal: 8개 작업 페이지 구현

- [ ] `gui/pages/cut_page.py`: 페이지 범위 입력 + cut 실행
- [ ] `gui/pages/merge_page.py`: 다중 파일 목록 + merge 실행
- [ ] `gui/pages/split_page.py`: 분할 옵션 + split 실행
- [ ] `gui/pages/rotate_page.py`: 각도 선택 + rotate 실행
- [ ] `gui/pages/resize_page.py`: 용지 크기 선택 + resize 실행
- [ ] `gui/pages/compress_page.py`: 품질 레벨 + compress 실행
- [ ] `gui/pages/watermark_page.py`: 텍스트/이미지 옵션 + watermark 실행
- [ ] `gui/pages/info_page.py`: PDF 메타데이터 표시

### Final Goal: 품질 및 배포

- [ ] `gui/widgets/page_range_input.py`: 페이지 범위 입력 커스텀 위젯
- [ ] `gui/widgets/file_list.py`: 드래그 순서 변경 가능한 파일 목록
- [ ] `gui/widgets/result_display.py`: 결과 표시 + 파일 열기 버튼
- [ ] 에러 핸들링: 모든 작업의 예외를 에러 다이얼로그로 표시
- [ ] PyInstaller 빌드 스크립트 업데이트 (`build_exe.py`)
- [ ] 테마 전환 토글 (선택)

### Optional Goal: 사용성 개선

- [ ] 최근 파일 목록 기능
- [ ] 결과 파일 바로 열기 기능
- [ ] 창 닫기 시 작업 중 확인 다이얼로그

---

## 5. 기술적 접근 방식

### 5.1 스레딩 전략

```
메인 스레드 (GUI)          워커 스레드 (작업 실행)
+------------------+       +--------------------+
| 사용자 입력 처리  |       | commands 함수 실행  |
| UI 업데이트       | <---- | 진행률 콜백 전달    |
| 이벤트 루프       |       | 결과/에러 콜백 전달 |
+------------------+       +--------------------+
```

- `threading.Thread(target=run_command, daemon=True)`로 작업 실행
- `widget.after()` 메서드로 GUI 스레드에서 안전하게 UI 업데이트
- 작업 완료/에러 시 콜백으로 메인 스레드에 통지

### 5.2 페이지 전환 패턴

- 사이드바 버튼 클릭 시 `pack_forget()` + `pack()` 패턴으로 페이지 전환
- 각 페이지는 `BasePage`를 상속하여 공통 UI 패턴 재사용
- 활성 페이지 하이라이트 표시

### 5.3 드래그 앤 드롭 구현

- `tkinterdnd2` 라이브러리를 사용하여 Windows 파일 드롭 이벤트 처리
- 드롭 영역에 시각적 피드백 제공 (하이라이트, 아이콘 변경)
- `.pdf` 확장자 검증 후 파일 로드

### 5.4 PyInstaller 빌드 업데이트

- `build_exe.py`에 GUI 모드 빌드 옵션 추가
- CustomTkinter 리소스(테마 파일, 폰트) `--add-data` 옵션으로 포함
- `--windowed` 플래그로 콘솔 창 숨김
- `--onefile` 플래그로 단일 EXE 생성

---

## 6. 리스크 분석

### 높은 위험

| 리스크 | 영향 | 대응 방안 |
|--------|------|-----------|
| CustomTkinter + PyInstaller 번들링 이슈 | EXE 실행 실패 | CustomTkinter 공식 PyInstaller 가이드 참조, `--collect-all customtkinter` 옵션 사용 |
| tkinterdnd2 Windows 호환성 | 드래그 앤 드롭 실패 | 대체 방안으로 파일 선택 다이얼로그만 지원, 드롭 기능은 Optional 처리 |

### 중간 위험

| 리스크 | 영향 | 대응 방안 |
|--------|------|-----------|
| GUI 스레드 블로킹 | 대용량 PDF 처리 시 UI 멈춤 | 모든 작업을 워커 스레드로 분리, 프로그레스 콜백 구현 |
| commands 함수 인터페이스 불일치 | GUI에서 호출 어려움 | 필요 시 얇은 어댑터 계층 추가 (commands 모듈 수정 없이) |

### 낮은 위험

| 리스크 | 영향 | 대응 방안 |
|--------|------|-----------|
| EXE 파일 크기 초과 (50MB+) | 배포 불편 | UPX 압축 적용, 불필요 모듈 제외 |
| macOS/Linux 호환성 | 크로스 플랫폼 미지원 | 초기 범위는 Windows 전용, 향후 확장 고려 |

---

## 7. 아키텍처 설계 방향

### 7.1 계층 분리 원칙

- **GUI 계층**: 사용자 입력 수집 + 결과 표시만 담당
- **비즈니스 로직 계층**: 기존 `commands/` + `core/` 모듈 그대로 사용
- **중간 계층 없음**: GUI에서 commands 함수를 직접 호출 (불필요한 추상화 방지)

### 7.2 확장성

- 새로운 PDF 작업 추가 시: `commands/`에 모듈 추가 + `gui/pages/`에 페이지 추가
- 위젯 재사용: `widgets/` 디렉터리의 공통 컴포넌트 활용
- 테마 확장: `theme.py`에서 커스텀 색상/폰트 관리

---

## 8. 다음 단계

1. `/moai:2-run SPEC-UI-001` 명령으로 구현 시작
2. Primary Goal 완료 후 Secondary Goal 진행
3. 구현 완료 후 `/moai:3-sync SPEC-UI-001`로 문서화
