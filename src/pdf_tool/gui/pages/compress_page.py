"""Compress 페이지 모듈.

PDF 파일을 압축하고 결과 통계를 표시한다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pdf_tool.commands.compress import compress_pdf


def run_compress(input_path: Path, output_path: Path) -> dict[str, Any]:
    """PDF 압축을 실행한다.

    Args:
        input_path: 입력 PDF 파일 경로
        output_path: 출력 PDF 파일 경로

    Returns:
        압축 결과 딕셔너리 (output_path, original_size, compressed_size, reduction_percent)
    """
    return compress_pdf(input_path, output=output_path)
