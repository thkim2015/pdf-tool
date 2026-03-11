"""Merge 페이지 모듈.

여러 PDF 파일을 하나로 병합한다.
"""

from __future__ import annotations

from pathlib import Path

from pdf_tool.commands.merge import merge_pdfs


def run_merge(input_files: list[Path], output_path: Path) -> Path:
    """PDF 병합을 실행한다.

    Args:
        input_files: 입력 PDF 파일 경로 리스트
        output_path: 출력 PDF 파일 경로

    Returns:
        생성된 출력 파일 경로
    """
    return merge_pdfs(input_files, output=output_path)
