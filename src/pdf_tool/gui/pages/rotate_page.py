"""Rotate 페이지 모듈.

PDF 페이지를 회전한다.
"""

from __future__ import annotations

from pathlib import Path

from pdf_tool.commands.rotate import rotate_pdf
from pdf_tool.core.progress import ProgressCallback


def run_rotate(
    input_path: Path,
    angle: int,
    pages: str | None,
    output_path: Path,
    callback: ProgressCallback = None,
) -> Path:
    """PDF 회전을 실행한다.

    Args:
        input_path: 입력 PDF 파일 경로
        angle: 회전 각도 (90, 180, 270)
        pages: 회전할 페이지 범위 (None이면 전체)
        output_path: 출력 PDF 파일 경로
        callback: 진행 상황 콜백

    Returns:
        생성된 출력 파일 경로
    """
    return rotate_pdf(input_path, angle=angle, pages=pages, output=output_path, callback=callback)
