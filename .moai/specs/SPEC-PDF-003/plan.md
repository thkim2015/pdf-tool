# SPEC-PDF-003 Implementation Plan

## 메타데이터

| 항목 | 값 |
|------|-----|
| SPEC ID | SPEC-PDF-003 |
| 제목 | Large PDF Processing & Progress Tracking |
| 생성일 | 2026-03-15 |

## 마일스톤

### Primary Goal: Progress Callback Framework (Phase 1)

**우선순위: High**

#### M1: ProgressCallback 프로토콜 및 기반 구현

- `core/progress.py` 신규 생성
  - `ProgressCallback` Protocol 정의 (on_start, on_progress, on_complete, on_error)
  - `NullProgressCallback` 구현 (no-op, 콜백 미지정 시 사용)
  - `RichProgressCallback` 구현 (CLI용 Rich Progress 어댑터)
  - `TkProgressCallback` 구현 (GUI용 tkinter 어댑터)
  - 콜백 내부 예외 안전 래퍼 (`safe_callback()` 유틸리티)
- 테스트: `test_progress_callbacks.py` - Protocol 준수, NullCallback, 예외 안전성 테스트

**관련 요구사항**: [SPEC-PDF-003-R1], [SPEC-PDF-003-R5], [SPEC-PDF-003-R6]

#### M2: 명령어 콜백 통합 (8개 명령어)

- `commands/cut.py`: 페이지 추출 루프에 콜백 호출 추가
- `commands/merge.py`: 파일별 병합 루프에 콜백 호출 추가
- `commands/split.py`: 페이지별 분할 루프에 콜백 호출 추가
- `commands/rotate.py`: 페이지별 회전 루프에 콜백 호출 추가
- `commands/resize.py`: 페이지별 크기 변경 루프에 콜백 호출 추가
- `commands/compress.py`: 압축 단계별 콜백 호출 추가
- `commands/watermark.py`: 페이지별 워터마크 루프에 콜백 호출 추가
- `commands/info.py`: 메타데이터 처리 콜백 호출 추가
- 모든 함수에 `callback: ProgressCallback | None = None` 매개변수 추가
- 테스트: 각 명령어별 콜백 호출 검증 테스트

**관련 요구사항**: [SPEC-PDF-003-R2], [SPEC-PDF-003-R5]

#### M3: CLI 진행률 표시 통합

- `cli.py` 수정: 각 명령어 호출 시 `RichProgressCallback` 인스턴스 생성 및 전달
- `--quiet` / `-q` 옵션 추가: 진행률 표시 비활성화
- TTY 감지 로직: 비 TTY 환경에서 텍스트 기반 진행률 출력
- 테스트: CLI 통합 테스트 (진행률 출력 검증)

**관련 요구사항**: [SPEC-PDF-003-R3]

#### M4: GUI 진행률 표시 통합

- `gui/pages/base_page_widget.py` 수정: 기존 스레딩 패턴에 콜백 연결
- `TkProgressCallback` 통합: `widget.after()`를 사용한 메인 스레드 UI 업데이트
- 작업 완료/오류 시 ProgressBarWidget 상태 전환
- 테스트: GUI 콜백 스레드 안전성 테스트

**관련 요구사항**: [SPEC-PDF-003-R4]

### Secondary Goal: Memory Optimization Research (Phase 2)

**우선순위: Medium**

#### M5: 라이브러리 비교 연구

- pypdf vs pypdfium2 메모리 사용 패턴 분석
- 대체 라이브러리 탐색 (pikepdf, pymupdf 등)
- 스트리밍 기반 처리 가능성 평가
- 100MB+ PDF 파일 벤치마크 실행

**관련 요구사항**: [SPEC-PDF-003-R7]

#### M6: 벤치마크 보고서 및 권장사항

- 메모리 사용량, 처리 시간, API 호환성 비교표 작성
- 점진적 마이그레이션 전략 제시
- 다음 SPEC 생성을 위한 권장사항 문서화

**관련 요구사항**: [SPEC-PDF-003-R8]

## 기술 접근 방식

### 아키텍처 설계

```
                    ProgressCallback (Protocol)
                    /          |          \
        NullCallback    RichCallback    TkCallback
             |               |              |
        (no-op)         Rich Progress   tkinter UI
                             |              |
                          cli.py      base_page_widget.py
                             \              /
                          commands/*.py (callback 매개변수)
                                  |
                            core/pdf_handler.py
```

### 설계 원칙

1. **Strategy 패턴**: ProgressCallback Protocol을 통한 다형적 진행률 표시
2. **Null Object 패턴**: 콜백 미지정 시 NullProgressCallback 사용으로 분기문 제거
3. **Adapter 패턴**: Rich와 tkinter를 ProgressCallback으로 래핑
4. **Thread Safety**: GUI 콜백은 `widget.after()` 사용, CLI 콜백은 단일 스레드
5. **Defensive Callback**: 모든 콜백 호출을 try-except로 감싸 안전성 보장

### 의존성 그래프

```
M1 (ProgressCallback 기반)
  -> M2 (명령어 통합)
    -> M3 (CLI 통합) [독립]
    -> M4 (GUI 통합) [독립]
M5 (연구) [Phase 1 완료 후]
  -> M6 (보고서)
```

- M3과 M4는 M2 완료 후 병렬 진행 가능
- M5는 Phase 1과 독립적이나, Phase 1 완료 후 진행 권장

## 리스크 및 대응 방안

| 리스크 | 영향 | 대응 방안 |
|--------|------|-----------|
| 기존 API 시그니처 변경으로 인한 regression | High | 콜백을 선택적 매개변수로 추가, 기존 테스트 전체 통과 확인 |
| GUI 스레드 안전성 문제 | Medium | `widget.after()`를 통한 메인 스레드 UI 업데이트 보장 |
| 콜백 내부 예외로 인한 처리 중단 | Medium | safe_callback 래퍼로 예외 격리 |
| Rich Progress와 기존 터미널 출력 충돌 | Low | Rich Console 컨텍스트 매니저 활용 |
| 100MB+ 파일 벤치마크 환경 부재 | Low | 테스트용 대용량 PDF 생성 스크립트 작성 |

## Coverage 목표

- 기존 테스트: 100% 통과 (zero regression)
- 신규 코드 coverage: 85% 이상
- 전체 프로젝트 coverage: 99%+ 유지
- 신규 테스트 케이스: 40개 이상

## Expert Consultation 권장

- **expert-backend**: ProgressCallback Protocol 설계 리뷰, 스레드 안전성 검증
- **expert-frontend**: GUI ProgressBarWidget 통합 및 UX 패턴 검증
