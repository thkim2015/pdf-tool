# SPEC-PDF-002 구현 계획

## 관련 SPEC

- SPEC ID: SPEC-PDF-002
- 제목: PDF 고급 조작 기능 (Resize, Compress, Watermark, Metadata)
- 의존성: SPEC-PDF-001 (Core 모듈 완성 필요)

## 마일스톤

### Primary Goal: Metadata 조회 및 Compress 기능

**복잡도**: 낮음

의존성: SPEC-PDF-001 Core 모듈

- `commands/info.py`: 메타데이터 조회/수정
  - pypdf의 metadata 속성 활용
  - Rich 테이블 형식 출력
  - JSON 출력 옵션
  - `--set-title`, `--set-author` 등 수정 옵션
  - 단위 테스트 작성
- `commands/compress.py`: PDF 압축
  - pypdf의 `compress_content_streams()` 활용
  - 압축 전후 파일 크기 비교 출력
  - 단위 테스트 작성

### Secondary Goal: Resize 기능 (용지 크기 + DPI)

**복잡도**: 높음

의존성: Primary Goal 완료

- `core/page_sizes.py`: 표준 용지 크기 상수 정의
  - A3, A4, A5, Letter, Legal 등
  - mm -> points 변환 유틸리티
- `core/image_processor.py`: PDF 내 이미지 DPI 처리
  - 임베디드 이미지 추출 (pypdf 이미지 객체 접근)
  - Pillow를 활용한 이미지 리샘플링
  - DPI 프리셋 정의 (screen: 72, ebook: 150, print: 300)
  - 이미지 재삽입 로직
- `commands/resize.py`: 페이지 리사이즈 + DPI 변경
  - MediaBox/CropBox 조정 (용지 크기 모드)
  - 콘텐츠 스케일링 (transformation matrix 활용)
  - fit/stretch/fill 모드 구현
  - 가로세로 비율 유지 로직
  - `--dpi` / `--dpi-preset` 옵션: 이미지 DPI 변경 모드
  - 변경 전후 파일 크기/이미지 수/DPI 리포트 출력
  - 단위 테스트 작성

### Final Goal: Watermark 기능

**복잡도**: 높음

의존성: Primary Goal 완료

- `core/watermark_generator.py`: 워터마크 PDF 생성
  - ReportLab Canvas로 텍스트 워터마크 PDF 생성
  - Pillow로 이미지 워터마크 처리
  - 투명도, 회전, 위치 제어
- `commands/watermark.py`: 워터마크 적용
  - pypdf의 `merge_page()` 활용하여 오버레이
  - 텍스트/이미지 워터마크 분기 처리
  - 페이지 범위 선택 지원
  - 단위 테스트 작성

### Optional Goal: 이미지 품질 압축

**복잡도**: 높음

- Pillow를 활용한 PDF 내 이미지 다운샘플링
- `--quality` 옵션 (low: 72dpi, medium: 150dpi, high: 300dpi)
- 이미지 추출 -> 리사이즈 -> 재삽입 파이프라인

## 기술 접근 방식

### Resize 구현 전략

**용지 크기 변경 (Page Size Resize)**:

pypdf의 페이지 변환 기능 활용:

1. 원본 페이지의 MediaBox에서 현재 크기 계산
2. 목표 크기와의 비율 계산
3. `page.add_transformation()` 으로 스케일링 적용
4. MediaBox를 목표 크기로 재설정

**fit 모드**: 가로세로 비율 중 작은 쪽에 맞춤 (여백 발생 가능)
**stretch 모드**: 비율 무시하고 목표 크기에 강제 맞춤
**fill 모드**: 가로세로 비율 중 큰 쪽에 맞춤 (잘림 발생 가능)

**이미지 DPI 변경 (DPI Resize)**:

pypdf + Pillow를 활용한 이미지 리샘플링:

1. pypdf로 PDF 내 모든 이미지 객체 탐색 (`page['/Resources']['/XObject']`)
2. 각 이미지의 현재 DPI 계산 (이미지 픽셀 크기 / PDF 표시 크기)
3. 목표 DPI에 맞게 Pillow로 이미지 리사이즈 (`Image.resize()` with `LANCZOS`)
4. 리사이즈된 이미지를 PDF에 재삽입
5. 처리 결과 리포트 출력 (이미지 수, 원본/변경 DPI, 파일 크기 변화)

### Watermark 구현 전략

**텍스트 워터마크**:
1. ReportLab Canvas로 임시 PDF 생성
  - 투명도: `canvas.setFillAlpha(opacity)`
  - 회전: `canvas.rotate(angle)`
  - 폰트 크기: 페이지 크기 기반 자동 조정
2. pypdf로 원본 페이지에 merge

**이미지 워터마크**:
1. Pillow로 이미지 로드 및 크기 조정
2. ReportLab Canvas에 이미지 삽입
3. pypdf로 원본 페이지에 merge

### Compress 구현 전략

1. pypdf의 `PdfWriter.compress_identical_objects()` 활용
2. `page.compress_content_streams()` 로 스트림 압축
3. 중복 객체 제거
4. 압축 전후 크기 비교

## 리스크 및 대응 방안

| 리스크 | 영향도 | 대응 방안 |
|--------|--------|-----------|
| 리사이즈 시 콘텐츠 깨짐 | 높음 | transformation matrix 정확한 계산, 다양한 PDF 테스트 |
| DPI 변경 시 이미지 품질 손실 | 중간 | LANCZOS 리샘플링 사용, 프리셋 DPI로 안전한 기본값 제공 |
| 특수 이미지 형식(JBIG2 등) 미지원 | 낮음 | 지원 불가 이미지 스킵 후 경고, 처리 가능 이미지만 변환 |
| ReportLab 한글 폰트 미지원 | 중간 | 시스템 폰트 탐색, 기본 영문 폰트 폴백 |
| 이미지 압축 시 품질 저하 | 중간 | 압축 전 미리보기 옵션, 원본 백업 안내 |
| 특수 PDF 구조에서 워터마크 실패 | 중간 | 예외 처리, 실패 시 원본 반환 |
