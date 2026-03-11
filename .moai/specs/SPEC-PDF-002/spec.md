# SPEC-PDF-002: PDF 고급 조작 기능 (Resize, Compress, Watermark, Metadata)

## 메타데이터

| 항목 | 값 |
|------|-----|
| SPEC ID | SPEC-PDF-002 |
| 제목 | PDF Advanced Operations |
| 생성일 | 2026-03-11 |
| 상태 | Planned |
| 우선순위 | Medium |
| 담당 | expert-backend |
| 의존성 | SPEC-PDF-001 (Core 모듈 필요) |

## Environment (환경)

- **런타임**: Python 3.13+
- **핵심 라이브러리**: pypdf >= 6.8.0
- **추가 라이브러리**: reportlab >= 4.4.10 (워터마크 생성)
- **이미지 처리**: Pillow >= 12.1.1 (리사이즈 지원)
- **CLI 프레임워크**: typer >= 0.24.1
- **선행 조건**: SPEC-PDF-001의 Core 모듈 완성

## Assumptions (가정)

- A1: SPEC-PDF-001의 core/ 모듈(pdf_handler, validators, page_range)을 재사용한다
- A2: 리사이즈는 페이지 MediaBox 조정 및 콘텐츠 스케일링으로 구현한다
- A3: 압축은 pypdf의 내장 compress_content_streams 기능을 활용한다
- A4: 워터마크는 reportlab로 생성한 오버레이 PDF를 pypdf로 합성한다
- A5: 메타데이터 조회/수정은 pypdf의 metadata 속성을 활용한다

## Requirements (요구사항)

### R1: PDF 리사이즈 (Resize)

- **WHEN** 사용자가 PDF 파일과 목표 용지 크기(A4, Letter, A3 등)를 지정하여 resize 명령을 실행하면 **THEN** 시스템은 모든 페이지를 해당 크기로 조정한 새 PDF를 생성해야 한다
- **WHEN** 사용자가 너비와 높이를 직접 지정(예: `--width 210 --height 297` mm)하면 **THEN** 시스템은 해당 크기로 페이지를 조정해야 한다
- **WHEN** 리사이즈할 때 **THEN** 시스템은 콘텐츠의 가로세로 비율을 유지하면서 지정 크기에 맞추어야 한다 (fit 모드 기본)
- **가능하면** 사용자가 `--mode` 옵션으로 fit(비율 유지), stretch(늘리기), fill(채우기) 모드를 선택할 수 있도록 제공
- **IF** 지원되지 않는 용지 크기가 입력되면 **THEN** 시스템은 지원 가능한 크기 목록을 안내해야 한다

### R1.5: PDF 이미지 DPI 변경 (DPI Resize)

- **WHEN** 사용자가 PDF 파일과 목표 DPI(예: `--dpi 150`)를 지정하여 resize 명령을 실행하면 **THEN** 시스템은 PDF 내 모든 임베디드 이미지의 해상도를 해당 DPI로 리샘플링한 새 PDF를 생성해야 한다
- **WHEN** 사용자가 DPI를 낮추면(예: 300dpi -> 150dpi) **THEN** 시스템은 이미지를 다운샘플링하여 파일 크기를 줄여야 한다
- **WHEN** DPI 변경이 완료되면 **THEN** 시스템은 변경 전후 파일 크기, 처리된 이미지 수, 원본/변경 DPI를 출력해야 한다
- **IF** PDF에 임베디드 이미지가 없으면 **THEN** 시스템은 "이미지가 포함되지 않은 PDF입니다" 메시지를 출력해야 한다
- **IF** 목표 DPI가 원본 이미지 DPI보다 높으면 **THEN** 시스템은 "업샘플링은 품질 향상 없이 파일 크기만 증가합니다" 경고를 출력하고 사용자 확인을 요청해야 한다
- **가능하면** DPI 프리셋 옵션을 제공: `--dpi-preset screen`(72dpi), `--dpi-preset ebook`(150dpi), `--dpi-preset print`(300dpi)

### R2: PDF 압축 (Compress)

- **WHEN** 사용자가 PDF 파일에 대해 compress 명령을 실행하면 **THEN** 시스템은 콘텐츠 스트림을 압축하여 파일 크기를 줄인 새 PDF를 생성해야 한다
- 시스템은 **항상** 압축 전후 파일 크기를 비교하여 절감률(%)을 출력해야 한다
- **IF** 이미 최대로 압축된 PDF이면 **THEN** 시스템은 "추가 압축 효과가 없습니다" 메시지를 출력해야 한다
- **가능하면** 이미지 품질 옵션(`--quality low|medium|high`)을 통해 이미지 다운샘플링 기능을 제공
- 시스템은 압축 후에도 PDF 콘텐츠의 **가독성을 유지해야 한다** (텍스트 손실 불가)

### R3: 워터마크 (Watermark)

- **WHEN** 사용자가 PDF 파일과 워터마크 텍스트를 지정하여 watermark 명령을 실행하면 **THEN** 시스템은 모든 페이지에 반투명 텍스트 워터마크가 적용된 새 PDF를 생성해야 한다
- **WHEN** 사용자가 이미지 파일을 워터마크로 지정하면 **THEN** 시스템은 해당 이미지를 모든 페이지에 오버레이해야 한다
- **가능하면** 워터마크 위치(`--position center|top|bottom`), 투명도(`--opacity 0.3`), 회전(`--rotation 45`) 옵션을 제공
- **가능하면** 워터마크 적용 페이지 범위(`--pages`)를 지정할 수 있도록 제공
- 시스템은 워터마크가 원본 콘텐츠의 가독성을 **심각하게 해치지 않아야 한다**

### R4: 메타데이터 조회/수정 (Metadata)

- **WHEN** 사용자가 PDF 파일에 대해 info 명령을 실행하면 **THEN** 시스템은 제목, 저자, 생성일, 페이지 수, 파일 크기 등 메타데이터를 출력해야 한다
- **WHEN** 사용자가 `--set-title`, `--set-author` 등의 옵션을 지정하면 **THEN** 시스템은 해당 메타데이터를 수정한 새 PDF를 생성해야 한다
- 시스템은 **항상** 메타데이터를 사람이 읽기 쉬운 형태(테이블)로 출력해야 한다
- **가능하면** JSON 형식 출력 옵션(`--json`)을 제공

## Specifications (세부 사양)

### 추가 모듈 구조

```
src/pdf_tool/
├── commands/
│   ├── resize.py       # 페이지 리사이즈
│   ├── compress.py     # 파일 압축
│   ├── watermark.py    # 워터마크 적용
│   └── info.py         # 메타데이터 조회/수정
├── core/
│   ├── page_sizes.py   # 용지 크기 상수 (A4, Letter 등)
│   ├── image_processor.py  # PDF 내 이미지 DPI 처리
│   └── watermark_generator.py  # ReportLab 워터마크 생성
```

### CLI 명령 설계

```
pdf-tool resize INPUT_FILE --size A4 --output resized.pdf
pdf-tool resize INPUT_FILE --width 210 --height 297 --mode fit --output resized.pdf
pdf-tool resize INPUT_FILE --dpi 150 --output lowres.pdf
pdf-tool resize INPUT_FILE --dpi-preset screen --output screen.pdf
pdf-tool compress INPUT_FILE --output compressed.pdf
pdf-tool compress INPUT_FILE --quality medium --output compressed.pdf
pdf-tool watermark INPUT_FILE --text "CONFIDENTIAL" --opacity 0.3 --rotation 45 --output marked.pdf
pdf-tool watermark INPUT_FILE --image logo.png --position center --output marked.pdf
pdf-tool info INPUT_FILE
pdf-tool info INPUT_FILE --set-title "새 제목" --set-author "작성자" --output updated.pdf
pdf-tool info INPUT_FILE --json
```

### 추가 기술 스택

| 라이브러리 | 버전 | 용도 |
|-----------|------|------|
| reportlab | >= 4.4.10 | 워터마크 PDF 오버레이 생성 |
| Pillow | >= 12.1.1 | 이미지 워터마크 처리 |

### 용지 크기 상수

| 이름 | 너비(mm) | 높이(mm) |
|------|---------|---------|
| A3 | 297 | 420 |
| A4 | 210 | 297 |
| A5 | 148 | 210 |
| Letter | 216 | 279 |
| Legal | 216 | 356 |

### Traceability (추적성)

- [SPEC-PDF-002-R1] -> Resize 기능 구현 (용지 크기 변경)
- [SPEC-PDF-002-R1.5] -> DPI Resize 기능 구현 (이미지 해상도 변경)
- [SPEC-PDF-002-R2] -> Compress 기능 구현
- [SPEC-PDF-002-R3] -> Watermark 기능 구현
- [SPEC-PDF-002-R4] -> Metadata 조회/수정 구현
