# pdf-tool

PDF 파일을 커맨드라인에서 조작할 수 있는 Python CLI 도구입니다. 페이지 추출, 병합, 분할, 회전, 크기 변경, 압축, 워터마크 적용, 메타데이터 관리 기능을 제공합니다.

## 기능

| 명령어 | 설명 |
|--------|------|
| `cut` | 지정한 페이지를 추출하여 새 PDF 생성 |
| `merge` | 여러 PDF 파일을 하나로 병합 |
| `split` | PDF를 페이지 단위로 분할 |
| `rotate` | 페이지를 시계 방향으로 회전 (90/180/270도) |
| `resize` | 페이지 크기 변경 (A4, Letter 등) 또는 이미지 DPI 조정 |
| `compress` | 콘텐츠 스트림 압축으로 파일 크기 축소 |
| `watermark` | 텍스트 또는 이미지 워터마크 적용 |
| `info` | 메타데이터 조회 및 수정 |

## 설치

**uv 사용 (권장):**

```bash
uv pip install pdf-tool
```

**pip 사용:**

```bash
pip install pdf-tool
```

**개발 환경 설치:**

```bash
git clone https://github.com/your-username/pdf_tool.git
cd pdf_tool
uv pip install -e ".[dev]"
```

## 사용법

### cut - 페이지 추출

```bash
# 특정 페이지 추출
pdf-tool cut input.pdf --pages "1,3,5"

# 범위와 개별 페이지 혼합
pdf-tool cut input.pdf --pages "1,3,5-10" --output extracted.pdf

# 상세 로그 출력
pdf-tool cut input.pdf --pages "2-5" --output result.pdf --verbose
```

### merge - PDF 병합

```bash
# 여러 파일 병합
pdf-tool merge file1.pdf file2.pdf file3.pdf --output merged.pdf

# glob 패턴으로 병합 (알파벳 순)
pdf-tool merge "*.pdf" --glob --output merged.pdf
```

### split - PDF 분할

```bash
# 페이지별로 분할
pdf-tool split input.pdf

# 5페이지 단위로 분할
pdf-tool split input.pdf --every 5 --output-dir ./output/
```

### rotate - 페이지 회전

```bash
# 전체 페이지 90도 회전
pdf-tool rotate input.pdf --angle 90

# 특정 페이지만 180도 회전
pdf-tool rotate input.pdf --angle 180 --pages "1-3" --output rotated.pdf
```

### resize - 페이지 크기 변경

```bash
# A4 크기로 변경
pdf-tool resize input.pdf --size A4 --output resized.pdf

# 커스텀 크기 지정 (mm 단위)
pdf-tool resize input.pdf --width 210 --height 297 --mode fit --output resized.pdf

# 이미지 DPI 변경 (파일 크기 줄이기)
pdf-tool resize input.pdf --dpi 150 --output lowres.pdf
```

지원 용지 크기: `A3`, `A4`, `A5`, `Letter`, `Legal`

리사이즈 모드: `fit` (비율 유지, 기본값), `stretch` (늘리기), `fill` (채우기)

### compress - PDF 압축

```bash
# 기본 압축
pdf-tool compress input.pdf --output compressed.pdf

# 압축 결과 상세 확인
pdf-tool compress input.pdf --verbose
```

### watermark - 워터마크 적용

```bash
# 텍스트 워터마크
pdf-tool watermark input.pdf --text "CONFIDENTIAL" --output marked.pdf

# 투명도와 회전 각도 조정
pdf-tool watermark input.pdf --text "DRAFT" --opacity 0.3 --rotation 45 --output marked.pdf

# 이미지 워터마크
pdf-tool watermark input.pdf --image logo.png --position center --output marked.pdf

# 특정 페이지에만 적용
pdf-tool watermark input.pdf --text "SAMPLE" --pages "1,3" --output marked.pdf
```

워터마크 위치: `center` (기본값), `top`, `bottom`

### info - 메타데이터 조회/수정

```bash
# 메타데이터 조회
pdf-tool info input.pdf

# JSON 형식으로 출력
pdf-tool info input.pdf --json

# 메타데이터 수정
pdf-tool info input.pdf --set-title "보고서" --set-author "홍길동" --output updated.pdf
```

### 공통 옵션

```bash
# 버전 확인
pdf-tool --version

# 도움말
pdf-tool --help
pdf-tool cut --help
```

모든 명령어는 `-o` / `--output` 옵션으로 출력 경로를 지정할 수 있습니다. 지정하지 않으면 입력 파일명 기반으로 자동 생성됩니다 (예: `input_cut.pdf`).

## 기술 스택

| 라이브러리 | 버전 | 용도 |
|-----------|------|------|
| pypdf | >= 6.8.0 | PDF 읽기/쓰기/조작 |
| typer | >= 0.24.1 | CLI 프레임워크 |
| rich | >= 13.0.0 | 터미널 출력 포맷팅 |
| reportlab | >= 4.4.10 | 워터마크 오버레이 생성 |
| Pillow | >= 12.1.1 | 이미지 워터마크 처리 |

- **Python**: 3.13+
- **패키지 관리**: uv 또는 pip (pyproject.toml)
- **플랫폼**: macOS, Linux, Windows

## 라이선스

MIT License
