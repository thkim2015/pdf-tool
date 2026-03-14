"""Image to PDF 변환 기능: 이미지 파일을 PDF로 변환한다."""

from pathlib import Path
from typing import List, Union

from PIL import Image
from pypdf import PdfReader, PdfWriter

from pdf_tool.core.exceptions import FileValidationError, PDFProcessingError
from pdf_tool.core.validators import validate_output_path


# 지원하는 이미지 포맷
SUPPORTED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}


def validate_image_file(path: Path) -> None:
    """이미지 파일이 존재하고 지원되는 포맷인지 검증한다.

    Args:
        path: 검증할 이미지 파일 경로

    Raises:
        FileValidationError: 파일이 존재하지 않거나 지원하지 않는 포맷일 때
    """
    if not path.is_file():
        raise FileValidationError(f"'{path}' 파일을 찾을 수 없습니다")

    if path.suffix.lower() not in SUPPORTED_IMAGE_FORMATS:
        raise FileValidationError(
            f"'{path}'는 지원하지 않는 이미지 포맷입니다. "
            f"지원 포맷: {', '.join(SUPPORTED_IMAGE_FORMATS)}"
        )

    try:
        with Image.open(path) as img:
            # 이미지가 유효한지 확인 (포맷 검증)
            img.verify()
    except Exception as exc:
        raise FileValidationError(f"'{path}'는 유효한 이미지 파일이 아닙니다") from exc


def image_to_pdf(
    image_paths: Union[Path, List[Path]],
    output_path: Path,
    keep_aspect_ratio: bool = True,
) -> None:
    """단일 또는 여러 이미지 파일을 PDF로 변환한다.

    각 이미지는 PDF의 한 페이지가 된다. 컬러 이미지는 RGB로 변환되고,
    그레이스케일 이미지는 그대로 유지된다.

    Args:
        image_paths: 변환할 이미지 파일 경로 (Path 객체 또는 경로 리스트)
        output_path: 출력 PDF 파일 경로
        keep_aspect_ratio: 종횡비 유지 여부 (기본값: True)

    Raises:
        FileValidationError: 이미지 파일이 유효하지 않을 때
        PDFProcessingError: PDF 생성 중 오류가 발생할 때
    """
    # 입력 경로 정규화
    if isinstance(image_paths, Path):
        image_paths = [image_paths]

    # 입력 검증
    if not image_paths:
        raise FileValidationError("변환할 이미지가 없습니다")

    for image_path in image_paths:
        validate_image_file(Path(image_path))

    validate_output_path(output_path)

    try:
        # PDF Writer 생성
        pdf_writer = PdfWriter()

        # 이미지를 PDF에 추가
        for image_path in image_paths:
            _add_image_to_pdf(pdf_writer, Path(image_path), keep_aspect_ratio)

        # PDF 저장
        with open(output_path, "wb") as f:
            pdf_writer.write(f)

    except PDFProcessingError:
        raise
    except Exception as exc:
        raise PDFProcessingError(f"PDF 생성 중 오류 발생: {exc}") from exc


def _add_image_to_pdf(
    pdf_writer: PdfWriter,
    image_path: Path,
    keep_aspect_ratio: bool,
) -> None:
    """이미지를 PDF에 페이지로 추가한다.

    Args:
        pdf_writer: 대상 PdfWriter 인스턴스
        image_path: 이미지 파일 경로
        keep_aspect_ratio: 종횡비 유지 여부

    Raises:
        PDFProcessingError: 이미지 추가 중 오류가 발생할 때
    """
    try:
        from io import BytesIO

        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        with Image.open(image_path) as img:
            # RGBA를 RGB로 변환 (PDF에서 투명도 미지원)
            if img.mode in ("RGBA", "LA", "P"):
                # 투명도 없는 이미지로 변환
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background
            elif img.mode not in ("RGB", "L"):
                img = img.convert("RGB")

            # A4 크기로 정렬 (약 210mm x 297mm, 72dpi 기준)
            a4_width = 595  # 포인트 단위
            a4_height = 842

            # 이미지 크기에 맞춘 페이지 크기 계산
            if keep_aspect_ratio:
                page_width, page_height = _calculate_page_size(
                    img.width, img.height, a4_width, a4_height
                )
            else:
                page_width, page_height = a4_width, a4_height

            # 임시 PDF로 이미지 변환
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

            # 이미지를 페이지 크기에 맞게 그리기
            img_width = page_width
            img_height = page_height

            if keep_aspect_ratio:
                # 이미지를 페이지 중앙에 배치
                x = 0
                y = 0
                c.drawImage(
                    image_path,
                    x,
                    y,
                    width=img_width,
                    height=img_height,
                    preserveAspectRatio=True,
                )
            else:
                c.drawImage(
                    image_path,
                    0,
                    0,
                    width=page_width,
                    height=page_height,
                    preserveAspectRatio=False,
                )

            c.save()
            buffer.seek(0)

            # 생성된 PDF를 메인 PDF에 추가
            temp_pdf = PdfReader(buffer)
            pdf_writer.add_page(temp_pdf.pages[0])

    except Exception as exc:
        raise PDFProcessingError(f"이미지 처리 중 오류 발생 ({image_path}): {exc}") from exc


def _calculate_page_size(
    img_width: int, img_height: int, max_width: float, max_height: float
) -> tuple[float, float]:
    """이미지 크기를 기반으로 페이지 크기를 계산한다.

    이미지의 종횡비를 유지하면서 최대 페이지 크기 내에 맞춘다.

    Args:
        img_width: 이미지 너비 (픽셀)
        img_height: 이미지 높이 (픽셀)
        max_width: 최대 페이지 너비 (포인트)
        max_height: 최대 페이지 높이 (포인트)

    Returns:
        계산된 페이지 너비와 높이
    """
    img_ratio = img_width / img_height
    max_ratio = max_width / max_height

    if img_ratio > max_ratio:
        # 이미지가 더 넓음
        page_width = max_width
        page_height = max_width / img_ratio
    else:
        # 이미지가 더 좁음
        page_height = max_height
        page_width = max_height * img_ratio

    return page_width, page_height
