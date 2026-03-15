# SPEC-PDF-003: 대용량 PDF 처리 지원 및 진행 상황 추적 개선

## 메타데이터

| 항목 | 값 |
|------|-----|
| SPEC ID | SPEC-PDF-003 |
| 제목 | Large PDF Processing & Progress Tracking |
| 생성일 | 2026-03-15 |
| 상태 | Planned |
| 우선순위 | High |
| 담당 | expert-backend |
| Lifecycle | spec-anchored |

## Environment (환경)

- **런타임**: Python 3.13+
- **핵심 라이브러리**: pypdf >= 6.8.0
- **CLI 프레임워크**: typer >= 0.24.1, rich >= 13.0.0
- **GUI 프레임워크**: customtkinter >= 5.2.0
- **PDF 렌더링**: pypdfium2 >= 4.0.0 (선택)
- **OS**: macOS, Linux, Windows (크로스 플랫폼)
- **기존 스레딩 모델**: threading 모듈 기반 GUI 비동기 실행

## Assumptions (가정)

- A1: pypdf는 전체 PDF를 메모리에 로드하는 설계이며, 이는 대용량 파일에서 메모리 병목을 유발한다
- A2: 현재 모든 PDF 명령어(8개)는 진행률 콜백 없이 동기적으로 실행된다
- A3: GUI는 threading 기반 비동기 패턴을 사용하며, 이 모델은 유지한다
- A4: Rich 라이브러리의 Progress 위젯이 CLI 진행률 표시에 적합하다
- A5: customtkinter의 ProgressBar 위젯이 GUI 진행률 표시에 적합하다
- A6: 100MB 이상 PDF 파일의 메모리 최적화는 Phase 2 연구 대상이며, 즉시 구현하지 않는다
- A7: 기존 테스트 스위트는 100% 통과 상태를 유지해야 한다 (zero regression)

## Requirements (요구사항)

### Phase 1: Progress Callback Framework

#### R1: ProgressCallback 인터페이스 설계 [SPEC-PDF-003-R1]

- 시스템은 **항상** `ProgressCallback` 프로토콜을 통해 진행률 정보를 외부에 전달할 수 있어야 한다
- **WHEN** PDF 처리 작업이 시작되면 **THEN** 시스템은 총 단계 수(total steps)를 콜백에 전달해야 한다
- **WHEN** PDF 처리 작업이 각 단계(페이지 처리, 파일 병합 등)를 완료하면 **THEN** 시스템은 현재 진행 단계(current step)를 콜백에 전달해야 한다
- **WHEN** PDF 처리 작업이 완료되면 **THEN** 시스템은 완료 상태를 콜백에 전달해야 한다
- **IF** 콜백이 제공되지 않으면 **THEN** 시스템은 기존 동작과 동일하게 콜백 없이 처리해야 한다 (하위 호환성)

#### R2: 명령어별 콜백 통합 [SPEC-PDF-003-R2]

- **WHEN** `cut` 명령이 실행되면 **THEN** 시스템은 페이지 추출 진행률을 콜백으로 전달해야 한다
- **WHEN** `merge` 명령이 실행되면 **THEN** 시스템은 파일별 병합 진행률을 콜백으로 전달해야 한다
- **WHEN** `split` 명령이 실행되면 **THEN** 시스템은 페이지별 분할 진행률을 콜백으로 전달해야 한다
- **WHEN** `rotate` 명령이 실행되면 **THEN** 시스템은 페이지별 회전 진행률을 콜백으로 전달해야 한다
- **WHEN** `resize` 명령이 실행되면 **THEN** 시스템은 페이지별 크기 변경 진행률을 콜백으로 전달해야 한다
- **WHEN** `compress` 명령이 실행되면 **THEN** 시스템은 압축 진행률을 콜백으로 전달해야 한다
- **WHEN** `watermark` 명령이 실행되면 **THEN** 시스템은 페이지별 워터마크 적용 진행률을 콜백으로 전달해야 한다
- **WHEN** `info` 명령이 실행되면 **THEN** 시스템은 메타데이터 처리 진행률을 콜백으로 전달해야 한다

#### R3: CLI 진행률 표시 [SPEC-PDF-003-R3]

- **WHEN** CLI에서 PDF 처리 명령이 실행되면 **THEN** 시스템은 Rich Progress Bar를 통해 진행률을 실시간으로 표시해야 한다
- 시스템은 **항상** 진행률 바에 현재 작업명, 처리된 항목 수, 전체 항목 수, 경과 시간을 표시해야 한다
- **IF** `--quiet` / `-q` 옵션이 지정되면 **THEN** 시스템은 진행률 표시를 생략해야 한다
- **IF** 터미널이 TTY가 아닌 경우(파이프라인 등) **THEN** 시스템은 진행률 바 대신 텍스트 기반 진행률을 출력해야 한다

#### R4: GUI 진행률 표시 [SPEC-PDF-003-R4]

- **WHEN** GUI에서 PDF 처리 작업이 시작되면 **THEN** 시스템은 ProgressBarWidget을 통해 진행률을 실시간으로 표시해야 한다
- **IF** [GUI 작업 실행 중] **AND WHEN** 사용자가 다른 UI 요소를 조작하면 **THEN** GUI는 응답성을 유지해야 한다 (메인 스레드 블로킹 방지)
- **WHEN** 작업이 완료되면 **THEN** 진행률 바는 100% 상태를 표시한 후 결과 화면으로 전환해야 한다
- **IF** 작업 중 오류가 발생하면 **THEN** 진행률 바는 오류 상태를 표시하고 오류 메시지를 사용자에게 보여줘야 한다

#### R5: 하위 호환성 [SPEC-PDF-003-R5]

- 시스템은 **항상** 기존 API 시그니처를 유지해야 한다 (콜백은 선택적 매개변수)
- 시스템은 콜백 **없이도** 기존과 동일하게 동작**해야 한다**
- 시스템은 **항상** 기존 테스트 스위트를 100% 통과해야 한다

#### R6: 에러 처리 [SPEC-PDF-003-R6]

- **IF** 콜백 함수 내부에서 예외가 발생하면 **THEN** 시스템은 콜백 오류를 로깅하되 PDF 처리를 계속 진행해야 한다
- **IF** PDF 처리 중 오류가 발생하면 **THEN** 시스템은 콜백에 오류 상태를 전달한 후 적절한 예외를 발생시켜야 한다
- 시스템은 콜백 오류로 인해 PDF 처리가 **중단되지 않아야 한다**

### Phase 2: Memory Optimization Research

#### R7: 대체 라이브러리 연구 [SPEC-PDF-003-R7]

- **WHEN** Phase 1이 완료되면 **THEN** pypdf와 pypdfium2의 메모리 사용 패턴을 비교 분석해야 한다
- 시스템은 **항상** 100MB 이상 PDF 파일에 대한 벤치마크 결과를 문서화해야 한다
- **가능하면** 스트리밍 기반 PDF 처리 라이브러리를 평가하여 메모리 최적화 경로를 제시해야 한다

#### R8: 벤치마크 및 권장사항 [SPEC-PDF-003-R8]

- 시스템은 **항상** 벤치마크 결과에 메모리 사용량, 처리 시간, API 호환성을 포함해야 한다
- **WHEN** 벤치마크가 완료되면 **THEN** 다음 단계 권장사항을 문서로 작성해야 한다
- **가능하면** 점진적 마이그레이션 전략을 포함한 로드맵을 제시해야 한다

## Specifications (세부 사양)

### ProgressCallback 프로토콜 설계

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class ProgressCallback(Protocol):
    """PDF 처리 진행률 콜백 프로토콜."""

    def on_start(self, total: int, description: str = "") -> None:
        """작업 시작 시 호출. total은 전체 단계 수."""
        ...

    def on_progress(self, current: int, total: int, description: str = "") -> None:
        """각 단계 완료 시 호출. current는 현재 완료 단계."""
        ...

    def on_complete(self, description: str = "") -> None:
        """작업 완료 시 호출."""
        ...

    def on_error(self, error: Exception, description: str = "") -> None:
        """작업 중 오류 발생 시 호출."""
        ...
```

### 파일 수정 계획

| 파일 | 변경 유형 | 설명 |
|------|-----------|------|
| `core/progress.py` | 신규 | ProgressCallback 프로토콜 및 구현체 |
| `core/pdf_handler.py` | 수정 | callback 매개변수 추가 |
| `commands/cut.py` | 수정 | 페이지별 콜백 호출 |
| `commands/merge.py` | 수정 | 파일별 콜백 호출 |
| `commands/split.py` | 수정 | 페이지별 콜백 호출 |
| `commands/rotate.py` | 수정 | 페이지별 콜백 호출 |
| `commands/resize.py` | 수정 | 페이지별 콜백 호출 |
| `commands/compress.py` | 수정 | 압축 단계별 콜백 호출 |
| `commands/watermark.py` | 수정 | 페이지별 콜백 호출 |
| `commands/info.py` | 수정 | 메타데이터 처리 콜백 호출 |
| `cli.py` | 수정 | Rich ProgressBar 통합 |
| `gui/pages/base_page_widget.py` | 수정 | ProgressBarWidget 콜백 연결 |
| `tests/test_progress_callbacks.py` | 신규 | 40+ 테스트 케이스 |

### 기술 접근 방식

1. **Protocol 기반 설계**: Python Protocol을 사용하여 느슨한 결합 유지
2. **선택적 콜백**: 모든 명령어 함수에 `callback: ProgressCallback | None = None` 매개변수 추가
3. **안전한 콜백 호출**: 콜백 내부 예외를 잡아 로깅하되 처리 중단 방지
4. **CLI 어댑터**: Rich Progress를 ProgressCallback으로 래핑하는 `RichProgressCallback` 구현
5. **GUI 어댑터**: tkinter ProgressBar를 ProgressCallback으로 래핑하는 `TkProgressCallback` 구현
6. **스레드 안전**: GUI 콜백은 `widget.after()`를 사용하여 메인 스레드에서 UI 업데이트

### Traceability (추적성)

- [SPEC-PDF-003-R1] -> ProgressCallback 프로토콜 설계 (core/progress.py)
- [SPEC-PDF-003-R2] -> 8개 명령어 콜백 통합 (commands/*.py)
- [SPEC-PDF-003-R3] -> CLI Rich ProgressBar 통합 (cli.py)
- [SPEC-PDF-003-R4] -> GUI ProgressBarWidget 통합 (gui/pages/base_page_widget.py)
- [SPEC-PDF-003-R5] -> 하위 호환성 보장 (전체)
- [SPEC-PDF-003-R6] -> 에러 처리 및 콜백 안전성 (core/progress.py)
- [SPEC-PDF-003-R7] -> 대체 라이브러리 연구 (Phase 2)
- [SPEC-PDF-003-R8] -> 벤치마크 및 권장사항 (Phase 2)
