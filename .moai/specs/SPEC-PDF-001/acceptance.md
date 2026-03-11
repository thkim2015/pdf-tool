# SPEC-PDF-001 인수 기준

## 관련 SPEC

- SPEC ID: SPEC-PDF-001
- 제목: PDF 핵심 조작 기능 (Cut, Merge, Split, Rotate)

## 테스트 시나리오

### TS-001: PDF 페이지 추출 (Cut)

**시나리오 1: 연속 페이지 범위 추출**

```gherkin
Given 10페이지짜리 PDF 파일 "sample.pdf"가 존재할 때
When 사용자가 "pdf-tool cut sample.pdf --pages 3-7 --output result.pdf" 명령을 실행하면
Then "result.pdf" 파일이 생성되어야 한다
And "result.pdf"는 정확히 5페이지를 포함해야 한다
And 원본 "sample.pdf"는 변경되지 않아야 한다
```

**시나리오 2: 복합 페이지 범위 추출**

```gherkin
Given 10페이지짜리 PDF 파일 "sample.pdf"가 존재할 때
When 사용자가 "pdf-tool cut sample.pdf --pages 1,3,5-7" 명령을 실행하면
Then 출력 파일은 정확히 5페이지(1, 3, 5, 6, 7페이지)를 포함해야 한다
```

**시나리오 3: 잘못된 페이지 범위**

```gherkin
Given 5페이지짜리 PDF 파일 "short.pdf"가 존재할 때
When 사용자가 "pdf-tool cut short.pdf --pages 3-10" 명령을 실행하면
Then 시스템은 "페이지 범위 초과: 최대 페이지는 5입니다" 에러를 출력해야 한다
And 종료 코드는 1이어야 한다
And 출력 파일은 생성되지 않아야 한다
```

### TS-002: PDF 병합 (Merge)

**시나리오 1: 여러 파일 병합**

```gherkin
Given "a.pdf"(3페이지)와 "b.pdf"(5페이지)와 "c.pdf"(2페이지)가 존재할 때
When 사용자가 "pdf-tool merge a.pdf b.pdf c.pdf --output merged.pdf" 명령을 실행하면
Then "merged.pdf"는 정확히 10페이지를 포함해야 한다
And 페이지 순서는 a.pdf -> b.pdf -> c.pdf 순이어야 한다
```

**시나리오 2: glob 패턴 병합**

```gherkin
Given "docs/" 디렉토리에 "01.pdf", "02.pdf", "03.pdf"가 존재할 때
When 사용자가 "pdf-tool merge 'docs/*.pdf' --output all.pdf" 명령을 실행하면
Then "all.pdf"가 생성되어야 한다
And 파일들이 알파벳 순서(01, 02, 03)로 병합되어야 한다
```

**시나리오 3: 존재하지 않는 파일 포함**

```gherkin
Given "a.pdf"는 존재하지만 "missing.pdf"는 존재하지 않을 때
When 사용자가 "pdf-tool merge a.pdf missing.pdf" 명령을 실행하면
Then 시스템은 "'missing.pdf' 파일을 찾을 수 없습니다" 에러를 출력해야 한다
And 병합된 출력 파일은 생성되지 않아야 한다
```

### TS-003: PDF 분할 (Split)

**시나리오 1: 페이지별 분할**

```gherkin
Given 5페이지짜리 PDF 파일 "document.pdf"가 존재할 때
When 사용자가 "pdf-tool split document.pdf --output-dir ./pages/" 명령을 실행하면
Then "./pages/" 디렉토리에 5개의 PDF 파일이 생성되어야 한다
And 각 파일은 "document_001.pdf" ~ "document_005.pdf" 형태여야 한다
And 각 파일은 정확히 1페이지를 포함해야 한다
```

**시나리오 2: 단위별 분할**

```gherkin
Given 12페이지짜리 PDF 파일 "book.pdf"가 존재할 때
When 사용자가 "pdf-tool split book.pdf --every 5 --output-dir ./parts/" 명령을 실행하면
Then 3개의 파일이 생성되어야 한다 (5페이지, 5페이지, 2페이지)
And 파일명은 "book_001.pdf", "book_002.pdf", "book_003.pdf"여야 한다
```

**시나리오 3: 분할 단위가 총 페이지 초과**

```gherkin
Given 3페이지짜리 PDF 파일 "small.pdf"가 존재할 때
When 사용자가 "pdf-tool split small.pdf --every 10" 명령을 실행하면
Then 1개의 파일이 생성되어야 한다
And 경고 메시지 "분할 단위(10)가 총 페이지(3)보다 큽니다"가 출력되어야 한다
```

### TS-004: PDF 회전 (Rotate)

**시나리오 1: 전체 페이지 회전**

```gherkin
Given 5페이지짜리 PDF 파일 "document.pdf"가 존재할 때
When 사용자가 "pdf-tool rotate document.pdf --angle 90 --output rotated.pdf" 명령을 실행하면
Then "rotated.pdf"의 모든 페이지가 시계 방향 90도 회전되어야 한다
And 페이지 수는 원본과 동일하게 5페이지여야 한다
```

**시나리오 2: 특정 페이지만 회전**

```gherkin
Given 5페이지짜리 PDF 파일 "document.pdf"가 존재할 때
When 사용자가 "pdf-tool rotate document.pdf --angle 180 --pages 2,4" 명령을 실행하면
Then 2페이지와 4페이지만 180도 회전되어야 한다
And 1, 3, 5페이지는 원본 상태를 유지해야 한다
```

**시나리오 3: 잘못된 각도 입력**

```gherkin
Given PDF 파일 "document.pdf"가 존재할 때
When 사용자가 "pdf-tool rotate document.pdf --angle 45" 명령을 실행하면
Then 시스템은 "지원되지 않는 각도: 45. 사용 가능한 값: 90, 180, 270" 에러를 출력해야 한다
And 종료 코드는 1이어야 한다
```

### TS-005: 공통 에러 처리

**시나리오 1: 파일 미존재**

```gherkin
Given "nonexistent.pdf" 파일이 존재하지 않을 때
When 사용자가 어떤 명령이든 해당 파일을 입력으로 지정하면
Then 시스템은 "'nonexistent.pdf' 파일을 찾을 수 없습니다" 에러를 출력해야 한다
And 종료 코드는 1이어야 한다
```

**시나리오 2: 유효하지 않은 PDF**

```gherkin
Given "not_a_pdf.txt" 텍스트 파일이 존재할 때
When 사용자가 "pdf-tool cut not_a_pdf.txt --pages 1" 명령을 실행하면
Then 시스템은 "유효한 PDF 파일이 아닙니다" 에러를 출력해야 한다
```

### TS-006: 출력 경로 자동 생성

**시나리오 1: 출력 옵션 미지정**

```gherkin
Given "report.pdf" 파일이 존재할 때
When 사용자가 "pdf-tool cut report.pdf --pages 1-3" 명령을 실행하면
Then 출력 파일이 "report_cut.pdf"로 자동 생성되어야 한다
```

## 품질 게이트 기준

| 기준 | 목표 |
|------|------|
| 테스트 커버리지 | >= 85% |
| 린터 경고 | 0건 (ruff) |
| 타입 체크 | mypy strict 통과 |
| CLI 통합 테스트 | 모든 명령어 정상/에러 케이스 통과 |
| 문서화 | 모든 공개 함수 docstring 포함 |

## 엣지 케이스

- 0페이지(빈) PDF 처리
- 단일 페이지 PDF에서 split 실행
- 동일 파일을 입력과 출력으로 지정
- 읽기 전용 디렉토리에 출력 시도
- 매우 큰 PDF(100MB+) 메모리 처리
- 파일명에 한글/특수문자 포함
- 이미 존재하는 출력 파일 덮어쓰기 확인

## Definition of Done

- [ ] 모든 EARS 요구사항에 대한 구현 완료
- [ ] 모든 테스트 시나리오 통과
- [ ] 테스트 커버리지 85% 이상
- [ ] ruff 린터 경고 0건
- [ ] `pip install -e .` 설치 후 `pdf-tool --help` 정상 동작
- [ ] 모든 명령어에 대한 `--help` 도움말 정상 출력
