# pdf-tool 사용 가이드

## 1. Cut - 페이지 추출

PDF에서 원하는 페이지만 추출하여 새 파일로 저장합니다.

```bash
pdf-tool cut input.pdf -p "1-10"                    # 1~10페이지 추출
pdf-tool cut input.pdf -p "1,3,5"                   # 특정 페이지 추출
pdf-tool cut input.pdf -p "1,3,5-10" -o output.pdf  # 범위+개별 혼합
```

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--pages` | `-p` | 추출할 페이지 범위 (예: `1,3,5-10`) |
| `--output` | `-o` | 출력 파일 경로 |
| `--verbose` | `-v` | 상세 로그 출력 |

---

## 2. Merge - PDF 병합

여러 PDF 파일을 하나로 합칩니다.

```bash
pdf-tool merge file1.pdf file2.pdf file3.pdf         # 여러 파일 병합
pdf-tool merge file1.pdf file2.pdf -o merged.pdf     # 출력 파일 지정
pdf-tool merge "*.pdf" --glob                        # glob 패턴 사용
```

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--output` | `-o` | 출력 파일 경로 |
| `--glob` | | glob 패턴 사용 |
| `--verbose` | `-v` | 상세 로그 출력 |

---

## 3. Split - PDF 분할

PDF를 페이지 단위로 나눕니다.

```bash
pdf-tool split input.pdf                             # 1페이지씩 분할
pdf-tool split input.pdf -e 5                        # 5페이지 단위 분할
pdf-tool split input.pdf -e 10 -d ./output_dir       # 출력 디렉토리 지정
```

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--every` | `-e` | 분할 단위 (페이지 수, 기본값: 1) |
| `--output-dir` | `-d` | 출력 디렉토리 경로 |
| `--verbose` | `-v` | 상세 로그 출력 |

---

## 4. Rotate - 페이지 회전

PDF 페이지를 시계 방향으로 회전합니다.

```bash
pdf-tool rotate input.pdf -a 90                      # 전체 90도 회전
pdf-tool rotate input.pdf -a 180 -p "1,3"            # 특정 페이지만 회전
pdf-tool rotate input.pdf -a 270 -o rotated.pdf      # 출력 파일 지정
```

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--angle` | `-a` | 회전 각도 (`90`, `180`, `270`) |
| `--pages` | `-p` | 회전할 페이지 범위 |
| `--output` | `-o` | 출력 파일 경로 |
| `--verbose` | `-v` | 상세 로그 출력 |

---

## 5. Resize - 페이지 크기 변경

PDF 페이지를 다른 용지 크기로 변환합니다.

```bash
pdf-tool resize input.pdf -s A4                      # A4로 변경
pdf-tool resize input.pdf -s Letter -m stretch       # Letter로 늘리기
pdf-tool resize input.pdf --width 200 --height 300   # 커스텀 크기 (mm)
```

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--size` | `-s` | 용지 크기 (`A3`, `A4`, `A5`, `Letter`, `Legal`) |
| `--width` | | 커스텀 너비 (mm) |
| `--height` | | 커스텀 높이 (mm) |
| `--mode` | `-m` | 리사이즈 모드 (`fit`, `stretch`, `fill`) |
| `--output` | `-o` | 출력 파일 경로 |
| `--verbose` | `-v` | 상세 로그 출력 |

**리사이즈 모드:**
- `fit` - 비율 유지하며 맞춤 (기본값)
- `stretch` - 용지에 맞게 늘리기
- `fill` - 용지를 채우도록 확대

---

## 6. Compress - PDF 압축

PDF 파일 크기를 줄입니다.

```bash
pdf-tool compress input.pdf                          # 기본 압축
pdf-tool compress input.pdf -o compressed.pdf        # 출력 파일 지정
pdf-tool compress input.pdf -v                       # 상세 로그
```

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--output` | `-o` | 출력 파일 경로 |
| `--verbose` | `-v` | 상세 로그 출력 |

---

## 7. Watermark - 워터마크 적용

PDF에 텍스트 또는 이미지 워터마크를 추가합니다.

```bash
# 텍스트 워터마크
pdf-tool watermark input.pdf -t "CONFIDENTIAL"
pdf-tool watermark input.pdf -t "DRAFT" --opacity 0.5 --rotation 30

# 이미지 워터마크
pdf-tool watermark input.pdf -i logo.png

# 특정 페이지 + 위치 지정
pdf-tool watermark input.pdf -t "SECRET" -p "1,3,5-10" --position top
```

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--text` | `-t` | 워터마크 텍스트 |
| `--image` | `-i` | 워터마크 이미지 경로 |
| `--opacity` | | 투명도 (`0.0`~`1.0`, 기본값: `0.3`) |
| `--rotation` | | 회전 각도 (텍스트 전용, 기본값: `45`) |
| `--position` | | 위치 (`center`, `top`, `bottom`) |
| `--pages` | `-p` | 적용할 페이지 범위 |
| `--output` | `-o` | 출력 파일 경로 |
| `--verbose` | `-v` | 상세 로그 출력 |

---

## 8. Info - 메타데이터 조회/수정

PDF 파일의 메타데이터를 확인하거나 변경합니다.

```bash
# 조회
pdf-tool info input.pdf                              # 기본 출력
pdf-tool info input.pdf --json                       # JSON 형식

# 수정
pdf-tool info input.pdf --set-title "보고서"
pdf-tool info input.pdf --set-author "홍길동" -o updated.pdf
```

| 옵션 | 단축 | 설명 |
|------|------|------|
| `--set-title` | | 제목 설정 |
| `--set-author` | | 저자 설정 |
| `--json` | | JSON 형식 출력 |
| `--output` | `-o` | 출력 파일 경로 (수정 시) |
| `--verbose` | `-v` | 상세 로그 출력 |

---

## 공통 옵션

```bash
pdf-tool --version                                   # 버전 확인
pdf-tool --help                                      # 전체 도움말
pdf-tool cut --help                                  # 명령어별 도움말
```

- 모든 명령어에 `-o` / `--output` 옵션으로 출력 경로를 지정할 수 있습니다.
- 출력 경로를 지정하지 않으면 입력 파일명 기반으로 자동 생성됩니다 (예: `input_cut.pdf`).
- `-v` / `--verbose` 옵션으로 상세한 실행 로그를 확인할 수 있습니다.

---

## Windows EXE 사용 시

`pdf-tool` 대신 `pdf-tool.exe`를 사용합니다.

```bash
pdf-tool.exe cut input.pdf -p "1-10"
pdf-tool.exe merge file1.pdf file2.pdf -o merged.pdf
```
