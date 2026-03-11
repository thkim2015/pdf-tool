"""워터마크 명령어: 텍스트 또는 이미지 워터마크를 PDF에 적용한다."""

import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_tool.core.exceptions import PDFProcessingError
from pdf_tool.core.page_range import parse_page_range
from pdf_tool.core.pdf_handler import load_pdf
from pdf_tool.core.validators import validate_output_path
from pdf_tool.core.watermark_generator import (
    create_image_watermark,
    create_text_watermark,
)
from pdf_tool.utils.file_utils import generate_output_filename


def watermark_pdf(
    input_path: Path,
    *,
    output: Path | None = None,
    text: str | None = None,
    image: Path | None = None,
    opacity: float = 0.3,
    rotation: float = 45,
    position: str = "center",
    pages: str | None = None,
) -> Path:
    """PDF에 워터마크를 적용한다.

    Args:
        input_path: 입력 PDF 파일 경로
        output: 출력 파일 경로 (None이면 자동 생성)
        text: 텍스트 워터마크 (image와 동시 사용 불가)
        image: 이미지 워터마크 경로 (text와 동시 사용 불가)
        opacity: 투명도 (0.0~1.0, 기본값 0.3)
        rotation: 회전 각도 (기본값 45도, 텍스트만 적용)
        position: 위치 ("center", "top", "bottom")
        pages: 적용할 페이지 범위 (예: "1,3,5-10")

    Returns:
        출력 파일 경로

    Raises:
        FileValidationError: PDF 파일이 존재하지 않거나 유효하지 않을 때
        FileNotFoundError: 이미지 파일이 존재하지 않을 때
        PDFProcessingError: 워터마크 처리 중 에러
    """
    if text is None and image is None:
        raise PDFProcessingError(
            "텍스트 또는 이미지 중 하나를 지정해야 합니다"
        )

    reader = load_pdf(input_path)

    if output is None:
        output = generate_output_filename(input_path, "watermark")

    validate_output_path(output)

    # 적용할 페이지 인덱스 결정
    total_pages = len(reader.pages)
    if pages is not None:
        target_indices = set(parse_page_range(pages, max_pages=total_pages))
    else:
        target_indices = set(range(total_pages))

    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if i in target_indices:
            # 이 페이지에 워터마크 적용
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)

            # 임시 파일에 워터마크 오버레이 PDF 생성
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                wm_path = Path(tmp.name)

            if text is not None:
                create_text_watermark(
                    text=text,
                    output_path=wm_path,
                    page_width=page_width,
                    page_height=page_height,
                    opacity=opacity,
                    rotation=rotation,
                    position=position,
                )
            else:
                assert image is not None
                create_image_watermark(
                    image_path=image,
                    output_path=wm_path,
                    page_width=page_width,
                    page_height=page_height,
                    opacity=opacity,
                    position=position,
                )

            # 워터마크 오버레이를 원본 페이지에 병합
            wm_reader = PdfReader(wm_path)
            wm_page = wm_reader.pages[0]
            page.merge_page(wm_page)

            # 임시 파일 정리
            wm_path.unlink(missing_ok=True)

        writer.add_page(page)

    # 메타데이터 복사
    if reader.metadata:
        writer.add_metadata(
            {k: v for k, v in reader.metadata.items() if v is not None}
        )

    with open(output, "wb") as f:
        writer.write(f)

    return output
