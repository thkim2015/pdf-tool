# SPEC-PDF-003 Acceptance Criteria

## 메타데이터

| 항목 | 값 |
|------|-----|
| SPEC ID | SPEC-PDF-003 |
| 제목 | Large PDF Processing & Progress Tracking |
| 생성일 | 2026-03-15 |

---

## Phase 1: Progress Callback Framework

### AC-01: ProgressCallback Protocol 정의 [SPEC-PDF-003-R1]

**Given** core/progress.py 모듈이 존재할 때
**When** ProgressCallback Protocol을 확인하면
**Then** on_start, on_progress, on_complete, on_error 메서드가 정의되어 있어야 한다
**And** runtime_checkable 데코레이터가 적용되어 있어야 한다

### AC-02: NullProgressCallback 구현 [SPEC-PDF-003-R1]

**Given** 콜백이 제공되지 않을 때
**When** NullProgressCallback이 사용되면
**Then** 모든 메서드 호출이 아무 동작 없이 정상 완료되어야 한다
**And** ProgressCallback Protocol을 준수해야 한다

### AC-03: RichProgressCallback 구현 [SPEC-PDF-003-R3]

**Given** CLI 환경에서 PDF 처리 명령이 실행될 때
**When** RichProgressCallback이 생성되면
**Then** Rich Progress Bar가 터미널에 표시되어야 한다
**And** on_progress 호출 시 진행률이 실시간으로 업데이트되어야 한다
**And** 작업명, 처리 항목 수, 전체 항목 수, 경과 시간이 표시되어야 한다

### AC-04: TkProgressCallback 구현 [SPEC-PDF-003-R4]

**Given** GUI 환경에서 PDF 처리 작업이 실행될 때
**When** TkProgressCallback이 생성되면
**Then** ProgressBarWidget이 진행률을 표시해야 한다
**And** UI 업데이트는 widget.after()를 통해 메인 스레드에서 실행되어야 한다
**And** 작업 중에도 GUI가 응답성을 유지해야 한다

### AC-05: cut 명령 콜백 통합 [SPEC-PDF-003-R2]

**Given** 10페이지 PDF 파일에서 5개 페이지를 추출할 때
**When** cut 명령에 콜백이 전달되면
**Then** on_start(total=5)가 호출되어야 한다
**And** on_progress가 1부터 5까지 순차적으로 호출되어야 한다
**And** on_complete가 마지막에 호출되어야 한다

### AC-06: merge 명령 콜백 통합 [SPEC-PDF-003-R2]

**Given** 3개의 PDF 파일을 병합할 때
**When** merge 명령에 콜백이 전달되면
**Then** on_start(total=3)이 호출되어야 한다
**And** on_progress가 파일별로 호출되어야 한다
**And** on_complete가 마지막에 호출되어야 한다

### AC-07: 나머지 명령어 콜백 통합 (split, rotate, resize, compress, watermark, info) [SPEC-PDF-003-R2]

**Given** 각 명령어에 콜백이 전달될 때
**When** PDF 처리가 진행되면
**Then** on_start, on_progress, on_complete가 올바른 순서로 호출되어야 한다
**And** total 값이 실제 처리 단위(페이지 수, 단계 수)와 일치해야 한다

### AC-08: CLI --quiet 옵션 [SPEC-PDF-003-R3]

**Given** CLI에서 `--quiet` 옵션과 함께 명령을 실행할 때
**When** PDF 처리가 진행되면
**Then** Rich Progress Bar가 표시되지 않아야 한다
**And** 최종 결과 요약만 출력되어야 한다

### AC-09: 비 TTY 환경 처리 [SPEC-PDF-003-R3]

**Given** 파이프라인 등 비 TTY 환경에서 명령을 실행할 때
**When** PDF 처리가 진행되면
**Then** Rich Progress Bar 대신 텍스트 기반 진행률이 출력되어야 한다

### AC-10: 하위 호환성 검증 [SPEC-PDF-003-R5]

**Given** 기존 코드에서 콜백 없이 명령어 함수를 호출할 때
**When** cut_pdf, merge_pdfs, split_pdf 등의 함수를 기존 방식으로 호출하면
**Then** 기존과 동일하게 정상 동작해야 한다
**And** 기존 테스트 스위트가 100% 통과해야 한다

### AC-11: 콜백 예외 안전성 [SPEC-PDF-003-R6]

**Given** 콜백의 on_progress 메서드가 예외를 발생시킬 때
**When** PDF 처리가 진행 중이면
**Then** PDF 처리는 중단 없이 완료되어야 한다
**And** 콜백 예외가 로깅되어야 한다
**And** 최종 결과물이 정상적이어야 한다

### AC-12: GUI 작업 중 오류 처리 [SPEC-PDF-003-R4, SPEC-PDF-003-R6]

**Given** GUI에서 PDF 처리 중 오류가 발생할 때
**When** 콜백의 on_error가 호출되면
**Then** ProgressBarWidget이 오류 상태를 표시해야 한다
**And** 사용자에게 오류 메시지가 보여야 한다
**And** GUI가 복구 가능한 상태를 유지해야 한다

---

## Phase 2: Memory Optimization Research

### AC-13: pypdf vs pypdfium2 메모리 비교 [SPEC-PDF-003-R7]

**Given** 100MB 이상 테스트 PDF 파일이 준비되었을 때
**When** pypdf와 pypdfium2로 동일한 작업을 수행하면
**Then** 각 라이브러리의 메모리 사용량이 측정되어 문서화되어야 한다
**And** 처리 시간이 함께 비교되어야 한다

### AC-14: 대체 라이브러리 평가 [SPEC-PDF-003-R7]

**Given** pikepdf, pymupdf 등 대체 라이브러리를 평가할 때
**When** 동일한 벤치마크를 실행하면
**Then** API 호환성, 메모리 효율성, 처리 속도가 비교표로 작성되어야 한다
**And** 각 라이브러리의 라이선스와 유지보수 상태가 확인되어야 한다

### AC-15: 벤치마크 결과 문서화 [SPEC-PDF-003-R8]

**Given** 모든 벤치마크가 완료되었을 때
**When** 결과 보고서를 작성하면
**Then** 메모리 사용량, 처리 시간, API 호환성 비교표가 포함되어야 한다
**And** 시각적 차트(표 형태)가 포함되어야 한다

### AC-16: 마이그레이션 권장사항 [SPEC-PDF-003-R8]

**Given** 벤치마크 결과가 문서화되었을 때
**When** 권장사항을 작성하면
**Then** 다음 단계 SPEC 생성을 위한 명확한 방향이 제시되어야 한다
**And** 점진적 마이그레이션 전략이 포함되어야 한다
**And** 리스크와 대응 방안이 식별되어야 한다

---

## Quality Gate

### Definition of Done

- [ ] 모든 AC (AC-01 ~ AC-12)가 Phase 1에서 충족됨
- [ ] 기존 테스트 스위트 100% 통과 (zero regression)
- [ ] 신규 테스트 40개 이상 작성
- [ ] 전체 코드 coverage 85% 이상 유지
- [ ] ruff 린터 경고 0건
- [ ] 콜백 없는 기존 호출 방식 하위 호환성 확인
- [ ] Phase 2: AC-13 ~ AC-16이 연구 보고서로 충족됨

### 검증 방법

| 항목 | 방법 | 도구 |
|------|------|------|
| Protocol 준수 | isinstance 검증 | pytest |
| 콜백 호출 순서 | Mock 기반 호출 순서 검증 | pytest-mock |
| CLI 출력 | stdout/stderr 캡처 | typer.testing.CliRunner |
| GUI 응답성 | 스레드 안전성 테스트 | threading + unittest.mock |
| 하위 호환성 | 기존 테스트 전체 실행 | pytest --tb=short |
| 예외 안전성 | 예외 발생 콜백으로 처리 검증 | pytest |
| Coverage | 커버리지 보고서 | pytest-cov |
