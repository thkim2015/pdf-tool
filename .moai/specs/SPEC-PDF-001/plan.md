# SPEC-PDF-001 구현 계획

## 관련 SPEC

- SPEC ID: SPEC-PDF-001
- 제목: PDF 핵심 조작 기능 (Cut, Merge, Split, Rotate)

## 마일스톤

### Primary Goal: 프로젝트 기반 및 Core 모듈 구축

**복잡도**: 중간

- 프로젝트 초기화 (pyproject.toml, src 구조, 의존성 설정)
- `core/pdf_handler.py`: PDF 파일 읽기/쓰기 공통 유틸리티
  - `load_pdf(path: Path) -> PdfReader` 함수
  - `save_pdf(writer: PdfWriter, path: Path)` 함수
  - 파일 존재 여부, PDF 유효성 검증 로직
- `core/page_range.py`: 페이지 범위 파서 구현
  - "1,3,5-10" 형식 파싱
  - 범위 유효성 검증 (최대 페이지 수 대비)
- `core/validators.py`: 입력값 검증 함수
- `utils/file_utils.py`: 출력 파일명 자동 생성 로직
- `utils/logging.py`: Rich 기반 로깅 설정
- 테스트 픽스처 준비 (샘플 PDF 생성)

### Secondary Goal: 핵심 명령어 구현

**복잡도**: 중간

의존성: Primary Goal 완료 필요

- `commands/cut.py`: 페이지 추출 기능
  - PdfReader에서 지정 페이지 추출 -> PdfWriter로 저장
  - 복합 범위 지원 (개별 + 연속)
  - 단위 테스트 작성
- `commands/merge.py`: PDF 병합 기능
  - PdfMerger 활용, 순차적 파일 병합
  - glob 패턴 지원
  - 단위 테스트 작성
- `commands/split.py`: PDF 분할 기능
  - 페이지별 분할 및 단위 분할
  - 출력 디렉토리 자동 생성
  - 단위 테스트 작성
- `commands/rotate.py`: 페이지 회전 기능
  - 전체/선택 페이지 회전
  - 각도 검증 (90, 180, 270만 허용)
  - 단위 테스트 작성

### Final Goal: CLI 통합 및 품질 보증

**복잡도**: 낮음

의존성: Secondary Goal 완료 필요

- `cli.py`: Typer 앱 구성 및 모든 명령어 등록
  - 공통 옵션 (`--output`, `--verbose`, `--version`)
  - 에러 핸들링 미들웨어 (typer callback)
  - Rich 기반 결과 출력
- 통합 테스트 작성 (CLI 레벨 E2E)
- 코드 품질 점검 (ruff, mypy type check)
- 설치 가능 패키지 검증 (`pip install -e .`)

## 기술 접근 방식

### 아키텍처 설계 방향

**계층형 구조 (Layered Architecture)**:

1. **CLI Layer** (`cli.py`): 사용자 입력 파싱, 옵션 처리, 결과 출력
2. **Command Layer** (`commands/`): 각 PDF 조작의 비즈니스 로직
3. **Core Layer** (`core/`): PDF I/O, 페이지 범위 파싱, 유효성 검증
4. **Utility Layer** (`utils/`): 파일 경로, 로깅 등 횡단 관심사

**의존성 방향**: CLI -> Command -> Core -> Utils (단방향)

### pypdf 활용 전략

- `PdfReader`: PDF 파일 읽기 및 메타데이터 접근
- `PdfWriter`: 새 PDF 파일 생성 및 페이지 추가
- `PdfMerger`: 다수 PDF 병합 (deprecated 주의, PdfWriter.append 사용 권장)
- 페이지 단위 조작: `reader.pages[i]` 접근 후 writer에 추가

### 에러 처리 전략

- 사용자 정의 예외 클래스 계층 구조:
  - `PDFToolError` (기본 예외)
  - `FileValidationError` (파일 관련)
  - `PageRangeError` (페이지 범위 관련)
  - `PDFProcessingError` (처리 중 에러)
- Typer callback에서 최상위 예외 포착 및 사용자 친화적 메시지 출력
- 부분 생성 파일 cleanup (atexit 또는 try-finally)

### 테스트 전략

- `conftest.py`에서 테스트용 PDF 동적 생성 (reportlab 또는 pypdf로)
- 각 명령어별 단위 테스트 + CLI 통합 테스트
- 엣지 케이스: 빈 PDF, 1페이지 PDF, 대용량 PDF, 암호화 PDF
- 커버리지 목표: 85% 이상

## 리스크 및 대응 방안

| 리스크 | 영향도 | 대응 방안 |
|--------|--------|-----------|
| pypdf의 특정 PDF 표준 미지원 | 중간 | 에러 메시지로 지원 범위 안내, pikepdf 대안 검토 |
| 대용량 PDF 메모리 부족 | 높음 | 스트리밍 처리 방식 도입, 메모리 사용량 모니터링 |
| 암호화된 PDF 처리 실패 | 낮음 | `--password` 옵션 제공, 미지원 암호화 방식 안내 |
| glob 패턴 보안 이슈 | 낮음 | 작업 디렉토리 제한, 심볼릭 링크 방지 |
