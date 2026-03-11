"""Split 페이지 모듈.

PDF를 N페이지 단위로 분할한다.
"""

from __future__ import annotations

from pathlib import Path

from pdf_tool.commands.split import split_pdf


def run_split(input_path: Path, every: int, output_dir: Path) -> list[Path]:
    """PDF 분할을 실행한다.

    Args:
        input_path: 입력 PDF 파일 경로
        every: 분할 단위 (N페이지마다)
        output_dir: 출력 디렉토리 경로

    Returns:
        생성된 파일 경로 리스트
    """
    return split_pdf(input_path, every=every, output_dir=output_dir)
