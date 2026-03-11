# SPEC-PDF-002 인수 기준

## 관련 SPEC

- SPEC ID: SPEC-PDF-002
- 제목: PDF 고급 조작 기능 (Resize, Compress, Watermark, Metadata)

## 테스트 시나리오

### TS-001: PDF 리사이즈 (Resize)

**시나리오 1: 표준 용지 크기로 리사이즈**

```gherkin
Given Letter 크기(216x279mm) PDF 파일 "letter.pdf"가 존재할 때
When 사용자가 "pdf-tool resize letter.pdf --size A4 --output a4.pdf" 명령을 실행하면
Then "a4.pdf"의 모든 페이지가 A4 크기(210x297mm)여야 한다
And 콘텐츠의 가로세로 비율이 유지되어야 한다
```

**시나리오 2: 커스텀 크기로 리사이즈**

```gherkin
Given A4 크기 PDF 파일 "document.pdf"가 존재할 때
When 사용자가 "pdf-tool resize document.pdf --width 150 --height 200 --output small.pdf" 명령을 실행하면
Then "small.pdf"의 페이지 크기가 150x200mm여야 한다
```

**시나리오 3: 지원되지 않는 크기**

```gherkin
Given PDF 파일이 존재할 때
When 사용자가 "pdf-tool resize doc.pdf --size B7" 명령을 실행하면
Then 시스템은 "지원되지 않는 크기: B7. 지원 목록: A3, A4, A5, Letter, Legal" 에러를 출력해야 한다
```

### TS-001.5: PDF 이미지 DPI 변경 (DPI Resize)

**시나리오 1: DPI 다운샘플링**

```gherkin
Given 300dpi 이미지가 포함된 PDF 파일 "highres.pdf"(10MB)가 존재할 때
When 사용자가 "pdf-tool resize highres.pdf --dpi 150 --output lowres.pdf" 명령을 실행하면
Then "lowres.pdf"의 파일 크기가 "highres.pdf"보다 작아야 한다
And 시스템은 "처리된 이미지: N개, 원본 DPI: 300, 변경 DPI: 150" 정보를 출력해야 한다
And 변경 전후 파일 크기 비교가 출력되어야 한다
```

**시나리오 2: DPI 프리셋 사용**

```gherkin
Given 이미지가 포함된 PDF 파일 "document.pdf"가 존재할 때
When 사용자가 "pdf-tool resize document.pdf --dpi-preset screen --output screen.pdf" 명령을 실행하면
Then "screen.pdf" 내 이미지들의 DPI가 72 이하여야 한다
```

**시나리오 3: 이미지 없는 PDF**

```gherkin
Given 텍스트만 포함된 PDF 파일 "textonly.pdf"가 존재할 때
When 사용자가 "pdf-tool resize textonly.pdf --dpi 150" 명령을 실행하면
Then 시스템은 "이미지가 포함되지 않은 PDF입니다" 메시지를 출력해야 한다
```

**시나리오 4: 업샘플링 경고**

```gherkin
Given 72dpi 이미지가 포함된 PDF 파일 "lowres.pdf"가 존재할 때
When 사용자가 "pdf-tool resize lowres.pdf --dpi 300" 명령을 실행하면
Then 시스템은 "업샘플링은 품질 향상 없이 파일 크기만 증가합니다" 경고를 출력해야 한다
```

### TS-002: PDF 압축 (Compress)

**시나리오 1: 기본 압축**

```gherkin
Given 이미지가 포함된 10MB PDF 파일 "heavy.pdf"가 존재할 때
When 사용자가 "pdf-tool compress heavy.pdf --output light.pdf" 명령을 실행하면
Then "light.pdf"의 파일 크기가 "heavy.pdf"보다 작거나 같아야 한다
And 시스템은 "원본: 10.0MB -> 압축: X.XMB (XX% 절감)" 형식의 결과를 출력해야 한다
And "light.pdf"의 텍스트 콘텐츠가 원본과 동일해야 한다
```

**시나리오 2: 이미 압축된 파일**

```gherkin
Given 이미 최대 압축된 PDF 파일 "compressed.pdf"가 존재할 때
When 사용자가 "pdf-tool compress compressed.pdf" 명령을 실행하면
Then 시스템은 "추가 압축 효과가 없습니다" 메시지를 출력해야 한다
```

### TS-003: 워터마크 (Watermark)

**시나리오 1: 텍스트 워터마크 적용**

```gherkin
Given 3페이지짜리 PDF 파일 "contract.pdf"가 존재할 때
When 사용자가 "pdf-tool watermark contract.pdf --text 'DRAFT' --opacity 0.3 --output draft.pdf" 명령을 실행하면
Then "draft.pdf"의 모든 3페이지에 "DRAFT" 워터마크가 표시되어야 한다
And 워터마크는 반투명(30%)이어야 한다
And 원본 텍스트가 읽을 수 있는 상태여야 한다
```

**시나리오 2: 이미지 워터마크 적용**

```gherkin
Given PDF 파일 "document.pdf"와 "logo.png" 이미지가 존재할 때
When 사용자가 "pdf-tool watermark document.pdf --image logo.png --position center --output branded.pdf" 명령을 실행하면
Then "branded.pdf"의 모든 페이지 중앙에 로고 이미지가 오버레이되어야 한다
```

**시나리오 3: 특정 페이지에만 워터마크**

```gherkin
Given 10페이지짜리 PDF 파일 "report.pdf"가 존재할 때
When 사용자가 "pdf-tool watermark report.pdf --text 'CONFIDENTIAL' --pages 1,3 --output marked.pdf" 명령을 실행하면
Then 1페이지와 3페이지에만 워터마크가 적용되어야 한다
And 나머지 페이지는 워터마크 없이 원본 상태여야 한다
```

### TS-004: 메타데이터 조회/수정 (Metadata)

**시나리오 1: 메타데이터 조회**

```gherkin
Given 메타데이터가 포함된 PDF 파일 "document.pdf"가 존재할 때
When 사용자가 "pdf-tool info document.pdf" 명령을 실행하면
Then 시스템은 제목, 저자, 생성일, 페이지 수, 파일 크기를 테이블 형식으로 출력해야 한다
```

**시나리오 2: 메타데이터 수정**

```gherkin
Given PDF 파일 "document.pdf"가 존재할 때
When 사용자가 "pdf-tool info document.pdf --set-title '새 제목' --set-author '작성자' --output updated.pdf" 명령을 실행하면
Then "updated.pdf"의 제목이 "새 제목"이어야 한다
And "updated.pdf"의 저자가 "작성자"여야 한다
```

**시나리오 3: JSON 형식 출력**

```gherkin
Given PDF 파일 "document.pdf"가 존재할 때
When 사용자가 "pdf-tool info document.pdf --json" 명령을 실행하면
Then 출력이 유효한 JSON 형식이어야 한다
And JSON에 "title", "author", "pages", "file_size" 키가 포함되어야 한다
```

## 품질 게이트 기준

| 기준 | 목표 |
|------|------|
| 테스트 커버리지 | >= 85% |
| 린터 경고 | 0건 (ruff) |
| 타입 체크 | mypy strict 통과 |
| 리사이즈 정확도 | 목표 크기 대비 +/- 1mm 이내 |
| 압축 텍스트 무결성 | 압축 전후 텍스트 추출 결과 100% 일치 |
| 워터마크 가독성 | 원본 텍스트 가려짐 없음 |

## 엣지 케이스

- 이미 A4인 PDF에 A4 리사이즈 요청
- 가로 방향(landscape) PDF 리사이즈
- 페이지마다 크기가 다른 혼합 PDF 리사이즈
- 이미 목표 DPI 이하인 이미지가 포함된 PDF에서 DPI 변경
- CMYK 이미지가 포함된 PDF에서 DPI 변경
- 한 PDF 내 서로 다른 DPI의 이미지 혼합 처리
- 텍스트가 없는(이미지만 있는) PDF 압축
- 매우 긴 워터마크 텍스트 (페이지에 들어가지 않는 경우)
- 투명 배경 PNG 워터마크
- 메타데이터가 전혀 없는 PDF에서 info 실행
- 유니코드 문자가 포함된 메타데이터

## Definition of Done

- [ ] 모든 EARS 요구사항에 대한 구현 완료
- [ ] 모든 테스트 시나리오 통과
- [ ] 테스트 커버리지 85% 이상
- [ ] ruff 린터 경고 0건
- [ ] SPEC-PDF-001의 기존 기능에 영향 없음 (회귀 테스트 통과)
- [ ] 모든 새 명령어 `--help` 정상 출력
- [ ] 리사이즈 후 PDF 열기 정상 동작 (뷰어 호환성)
