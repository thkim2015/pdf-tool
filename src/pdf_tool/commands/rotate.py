"""PDF 회전(Rotate) 명령: 지정된 페이지를 시계 방향으로 회전한다."""

from pathlib import Path

from pypdf import PdfWriter

from pdf_tool.core.exceptions import PDFToolError
from pdf_tool.core.page_range import parse_page_range
from pdf_tool.core.pdf_handler import load_pdf, save_pdf
from pdf_tool.core.progress import ProgressCallback, safe_callback
from pdf_tool.utils.file_utils import generate_output_filename

# 지원하는 회전 각도
VALID_ANGLES = {90, 180, 270}


def rotate_pdf(
    input_file: Path,
    *,
    angle: int,
    pages: str | None = None,
    output: Path | None = None,
    callback: ProgressCallback = None,
) -> Path:
    """PDF 페이지를 시계 방향으로 회전한다.

    Args:
        input_file: 입력 PDF 파일 경로
        angle: 회전 각도 (90, 180, 270)
        pages: 회전할 페이지 범위 (None이면 전체 페이지)
        output: 출력 파일 경로 (None이면 자동 생성)
        callback: 진행 상황 콜백 (current, total)

    Returns:
        생성된 출력 파일 경로

    Raises:
        PDFToolError: 지원하지 않는 각도일 때
        FileValidationError: 파일 관련 에러
        PageRangeError: 페이지 범위 에러
    """
    if angle not in VALID_ANGLES:
        raise PDFToolError(f"지원되지 않는 각도: {angle}. 사용 가능한 값: 90, 180, 270")

    reader = load_pdf(input_file)
    total_pages = len(reader.pages)

    # 회전 대상 페이지 결정
    if pages is not None:
        target_indices = set(parse_page_range(pages, max_pages=total_pages))
    else:
        target_indices = set(range(total_pages))

    if output is None:
        output = generate_output_filename(input_file, "rotate")

    writer = PdfWriter()
    for i in range(total_pages):
        page = reader.pages[i]
        if i in target_indices:
            page = page.rotate(angle)
        writer.add_page(page)
        safe_callback(callback, i + 1, total_pages)

    save_pdf(writer, output)
    return output
