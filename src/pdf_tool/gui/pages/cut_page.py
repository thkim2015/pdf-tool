"""Cut 페이지 모듈.

PDF의 특정 페이지를 잘라내어 새 파일로 저장한다.
"""

from __future__ import annotations

from pathlib import Path

from pdf_tool.commands.cut import cut_pdf
from pdf_tool.core.progress import ProgressCallback


def run_cut(
    input_path: Path,
    pages: str,
    output_path: Path,
    callback: ProgressCallback = None,
) -> Path:
    """PDF 잘라내기를 실행한다.

    Args:
        input_path: 입력 PDF 파일 경로
        pages: 페이지 범위 문자열 ("1-3, 5, 8-10")
        output_path: 출력 PDF 파일 경로
        callback: 진행 상황 콜백

    Returns:
        생성된 출력 파일 경로
    """
    return cut_pdf(input_path, pages=pages, output=output_path, callback=callback)
