"""PDF 페이지 추출(Cut) 명령: 지정된 페이지만 추출하여 새 PDF를 생성한다."""

from pathlib import Path

from pypdf import PdfWriter

from pdf_tool.core.page_range import parse_page_range
from pdf_tool.core.pdf_handler import load_pdf, save_pdf
from pdf_tool.core.progress import ProgressCallback, safe_callback
from pdf_tool.utils.file_utils import generate_output_filename


def cut_pdf(
    input_file: Path,
    *,
    pages: str,
    output: Path | None = None,
    callback: ProgressCallback = None,
) -> Path:
    """PDF에서 지정된 페이지를 추출하여 새 파일을 생성한다.

    Args:
        input_file: 입력 PDF 파일 경로
        pages: 추출할 페이지 범위 문자열 (예: "1,3,5-10")
        output: 출력 파일 경로 (None이면 자동 생성)
        callback: 진행 상황 콜백 (current, total)

    Returns:
        생성된 출력 파일 경로

    Raises:
        FileValidationError: 파일 관련 에러
        PageRangeError: 페이지 범위 에러
    """
    reader = load_pdf(input_file)
    max_pages = len(reader.pages)
    page_indices = parse_page_range(pages, max_pages=max_pages)

    if output is None:
        output = generate_output_filename(input_file, "cut")

    total = len(page_indices)
    writer = PdfWriter()
    for i, idx in enumerate(page_indices):
        writer.add_page(reader.pages[idx])
        safe_callback(callback, i + 1, total)

    save_pdf(writer, output)
    return output
