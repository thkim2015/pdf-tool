"""Resize 페이지 모듈.

PDF 페이지 크기를 변경한다.
"""

from __future__ import annotations

from pathlib import Path

from pdf_tool.commands.resize import resize_pdf
from pdf_tool.core.progress import ProgressCallback


def run_resize(
    input_path: Path,
    size: str,
    mode: str,
    output_path: Path,
    callback: ProgressCallback = None,
) -> Path:
    """PDF 크기 변경을 실행한다.

    Args:
        input_path: 입력 PDF 파일 경로
        size: 용지 크기 (A3, A4, A5, Letter, Legal)
        mode: 리사이즈 모드 (fit, stretch, fill)
        output_path: 출력 PDF 파일 경로
        callback: 진행 상황 콜백

    Returns:
        생성된 출력 파일 경로
    """
    return resize_pdf(input_path, size=size, mode=mode, output=output_path, callback=callback)
