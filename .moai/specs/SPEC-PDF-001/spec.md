# SPEC-PDF-001: PDF 핵심 조작 기능 (Cut, Merge, Split, Rotate)

## 메타데이터

| 항목 | 값 |
|------|-----|
| SPEC ID | SPEC-PDF-001 |
| 제목 | PDF Core Operations |
| 생성일 | 2026-03-11 |
| 상태 | Planned |
| 우선순위 | High |
| 담당 | expert-backend |

## Environment (환경)

- **런타임**: Python 3.13+
- **핵심 라이브러리**: pypdf >= 6.8.0
- **CLI 프레임워크**: typer >= 0.24.1
- **패키지 관리**: uv 또는 pip (pyproject.toml 기반)
- **OS**: macOS, Linux, Windows (크로스 플랫폼)

## Assumptions (가정)

- A1: 입력 PDF 파일은 유효한 PDF 형식이며, 암호화되지 않은 상태를 기본으로 한다
- A2: pypdf 라이브러리가 대부분의 PDF 표준(PDF 1.0~2.0)을 지원한다
- A3: CLI 인터페이스를 통해 사용자가 파일 경로와 옵션을 전달한다
- A4: 출력 파일은 입력 파일을 덮어쓰지 않고 별도 경로에 생성한다
- A5: 단일 PDF 파일 크기는 최대 500MB까지 처리 가능해야 한다

## Requirements (요구사항)

### R1: PDF 페이지 추출 (Cut)

- **WHEN** 사용자가 PDF 파일 경로와 페이지 범위를 지정하여 cut 명령을 실행하면 **THEN** 시스템은 해당 페이지만 포함된 새 PDF 파일을 생성해야 한다
- **WHEN** 사용자가 "1,3,5-10" 형태의 복합 페이지 범위를 입력하면 **THEN** 시스템은 개별 페이지와 범위를 모두 파싱하여 올바르게 추출해야 한다
- **IF** 지정된 페이지 번호가 PDF의 총 페이지 수를 초과하면 **THEN** 시스템은 명확한 에러 메시지를 출력하고 작업을 중단해야 한다
- 시스템은 **항상** 원본 PDF 파일을 수정하지 않아야 한다

### R2: PDF 병합 (Merge)

- **WHEN** 사용자가 2개 이상의 PDF 파일 경로를 지정하여 merge 명령을 실행하면 **THEN** 시스템은 입력 순서대로 모든 페이지를 결합한 새 PDF 파일을 생성해야 한다
- **WHEN** 사용자가 glob 패턴(예: `*.pdf`)을 입력하면 **THEN** 시스템은 매칭되는 모든 PDF 파일을 알파벳 순서로 병합해야 한다
- **IF** 입력 파일 중 하나가 존재하지 않거나 유효하지 않은 PDF이면 **THEN** 시스템은 해당 파일명을 포함한 에러 메시지를 출력해야 한다

### R3: PDF 분할 (Split)

- **WHEN** 사용자가 PDF 파일에 대해 split 명령을 실행하면 **THEN** 시스템은 각 페이지를 개별 PDF 파일로 분할해야 한다
- **WHEN** 사용자가 분할 단위(예: 매 5페이지)를 지정하면 **THEN** 시스템은 해당 단위로 PDF를 나누어 여러 파일을 생성해야 한다
- **IF** 분할 단위가 총 페이지 수보다 크면 **THEN** 시스템은 원본과 동일한 단일 파일을 생성하고 경고 메시지를 출력해야 한다

### R4: PDF 회전 (Rotate)

- **WHEN** 사용자가 PDF 파일과 회전 각도(90, 180, 270)를 지정하여 rotate 명령을 실행하면 **THEN** 시스템은 모든 페이지를 해당 각도만큼 시계 방향으로 회전한 새 PDF를 생성해야 한다
- **WHEN** 사용자가 특정 페이지 범위와 함께 회전을 요청하면 **THEN** 시스템은 지정된 페이지만 회전하고 나머지는 원본 상태로 유지해야 한다
- **IF** 유효하지 않은 각도(예: 45도)가 입력되면 **THEN** 시스템은 지원 가능한 각도 목록을 안내하는 에러 메시지를 출력해야 한다

### R5: CLI 인터페이스 (공통)

- 시스템은 **항상** `--output` / `-o` 옵션을 통해 출력 파일 경로를 지정할 수 있어야 한다
- **IF** 출력 경로가 지정되지 않으면 **THEN** 시스템은 입력 파일명 기반으로 자동 생성해야 한다 (예: `input_cut.pdf`)
- 시스템은 **항상** `--verbose` / `-v` 옵션으로 상세 처리 로그를 출력할 수 있어야 한다
- 시스템은 **항상** `--version` 명령으로 현재 버전을 표시해야 한다
- 시스템은 **항상** 처리 완료 후 결과 요약(생성된 파일, 페이지 수 등)을 출력해야 한다

### R6: 에러 처리 (공통)

- **IF** 입력 파일이 존재하지 않으면 **THEN** 시스템은 `FileNotFoundError` 메시지와 함께 종료 코드 1로 종료해야 한다
- **IF** 입력 파일이 유효한 PDF가 아니면 **THEN** 시스템은 파일 형식 에러 메시지를 출력해야 한다
- **IF** 암호화된 PDF가 입력되면 **THEN** 시스템은 비밀번호 옵션(`--password`)을 안내하는 메시지를 출력해야 한다
- 시스템은 **항상** 에러 발생 시 부분적으로 생성된 출력 파일을 정리해야 한다

## Specifications (세부 사양)

### 프로젝트 구조

```
pdf_tool/
├── pyproject.toml
├── src/
│   └── pdf_tool/
│       ├── __init__.py
│       ├── cli.py              # Typer CLI 진입점
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── cut.py          # 페이지 추출
│       │   ├── merge.py        # 병합
│       │   ├── split.py        # 분할
│       │   └── rotate.py       # 회전
│       ├── core/
│       │   ├── __init__.py
│       │   ├── pdf_handler.py  # PDF I/O 공통 유틸리티
│       │   ├── page_range.py   # 페이지 범위 파서
│       │   └── validators.py   # 입력 검증
│       └── utils/
│           ├── __init__.py
│           ├── file_utils.py   # 파일 경로 유틸리티
│           └── logging.py      # 로깅 설정
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # 테스트 픽스처
│   ├── test_cut.py
│   ├── test_merge.py
│   ├── test_split.py
│   ├── test_rotate.py
│   └── test_page_range.py
└── fixtures/                    # 테스트용 샘플 PDF
    ├── sample_10pages.pdf
    └── sample_encrypted.pdf
```

### CLI 명령 설계

```
pdf-tool cut INPUT_FILE --pages "1,3,5-10" --output output.pdf
pdf-tool merge file1.pdf file2.pdf file3.pdf --output merged.pdf
pdf-tool merge "*.pdf" --output merged.pdf
pdf-tool split INPUT_FILE --every 5 --output-dir ./output/
pdf-tool rotate INPUT_FILE --angle 90 --pages "1-3" --output rotated.pdf
```

### 기술 스택

| 라이브러리 | 버전 | 용도 |
|-----------|------|------|
| pypdf | >= 6.8.0 | PDF 읽기/쓰기/조작 |
| typer | >= 0.24.1 | CLI 프레임워크 |
| rich | >= 13.0.0 | 터미널 출력 포맷팅 |
| pytest | >= 8.0.0 | 테스트 프레임워크 |
| ruff | >= 0.9.0 | 린터/포맷터 |

### Traceability (추적성)

- [SPEC-PDF-001-R1] -> Cut 기능 구현
- [SPEC-PDF-001-R2] -> Merge 기능 구현
- [SPEC-PDF-001-R3] -> Split 기능 구현
- [SPEC-PDF-001-R4] -> Rotate 기능 구현
- [SPEC-PDF-001-R5] -> CLI 공통 인터페이스
- [SPEC-PDF-001-R6] -> 에러 처리 공통 로직
