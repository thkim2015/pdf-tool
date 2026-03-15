"""PDF 분할(Split) 명령: PDF를 페이지별 또는 단위별로 나누어 여러 파일을 생성한다."""

import math
from pathlib import Path

from pypdf import PdfWriter

from pdf_tool.core.pdf_handler import load_pdf
from pdf_tool.core.progress import ProgressCallback, safe_callback
from pdf_tool.utils.logging import print_warning


def split_pdf(
    input_file: Path,
    *,
    every: int = 1,
    output_dir: Path | None = None,
    callback: ProgressCallback = None,
) -> list[Path]:
    """PDF 파일을 지정된 단위로 분할한다.

    Args:
        input_file: 입력 PDF 파일 경로
        every: 분할 단위 (기본값: 1, 페이지별 분할)
        output_dir: 출력 디렉토리 경로 (None이면 입력 파일과 같은 디렉토리)
        callback: 진행 상황 콜백 (current, total)

    Returns:
        생성된 출력 파일 경로 목록

    Raises:
        FileValidationError: 파일 관련 에러
    """
    reader = load_pdf(input_file)
    total_pages = len(reader.pages)
    stem = input_file.stem

    if output_dir is None:
        output_dir = input_file.parent

    # 출력 디렉토리가 없으면 생성
    output_dir.mkdir(parents=True, exist_ok=True)

    # 분할 단위가 총 페이지보다 크면 경고
    if every > total_pages:
        print_warning(f"분할 단위({every})가 총 페이지({total_pages})보다 큽니다")

    total_chunks = math.ceil(total_pages / every)
    result_files: list[Path] = []
    file_num = 1

    for start in range(0, total_pages, every):
        end = min(start + every, total_pages)
        writer = PdfWriter()

        for page_idx in range(start, end):
            writer.add_page(reader.pages[page_idx])

        output_path = output_dir / f"{stem}_{file_num:03d}.pdf"
        with open(output_path, "wb") as f:
            writer.write(f)

        result_files.append(output_path)
        safe_callback(callback, file_num, total_chunks)
        file_num += 1

    return result_files
