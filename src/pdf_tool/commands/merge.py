"""PDF 병합(Merge) 명령: 여러 PDF 파일을 순서대로 결합하여 하나의 파일로 만든다."""

import glob as glob_module
from pathlib import Path

from pypdf import PdfWriter

from pdf_tool.core.pdf_handler import load_pdf, save_pdf
from pdf_tool.core.progress import ProgressCallback, safe_callback
from pdf_tool.utils.file_utils import generate_output_filename


def merge_pdfs(
    input_files: list[Path],
    *,
    output: Path | None = None,
    use_glob: bool = False,
    callback: ProgressCallback = None,
) -> Path:
    """여러 PDF 파일을 하나로 병합한다.

    Args:
        input_files: 입력 PDF 파일 경로 목록 (또는 glob 패턴)
        output: 출력 파일 경로 (None이면 자동 생성)
        use_glob: True이면 입력을 glob 패턴으로 처리
        callback: 진행 상황 콜백 (current, total)

    Returns:
        생성된 출력 파일 경로

    Raises:
        FileValidationError: 파일 관련 에러
    """
    # glob 패턴 확장
    if use_glob:
        expanded: list[Path] = []
        for pattern in input_files:
            matches = sorted(glob_module.glob(str(pattern)))
            expanded.extend(Path(m) for m in matches)
        input_files = expanded

    # 모든 파일을 먼저 검증하고 로드한다
    readers = []
    for file_path in input_files:
        readers.append(load_pdf(file_path))

    if output is None:
        output = generate_output_filename(input_files[0], "merge")

    # 전체 페이지 수 계산
    total_pages = sum(len(r.pages) for r in readers)
    current_page = 0

    writer = PdfWriter()
    for reader in readers:
        for page in reader.pages:
            writer.add_page(page)
            current_page += 1
            safe_callback(callback, current_page, total_pages)

    save_pdf(writer, output)
    return output
