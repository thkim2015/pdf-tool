"""이미지→PDF 변환 페이지 모듈.

여러 이미지 파일을 단일 PDF로 변환한다.
"""

from __future__ import annotations

from pathlib import Path

from pdf_tool.core.image_converter import image_to_pdf


def run_image_to_pdf(
    image_paths: list[Path],
    output_path: Path,
    keep_aspect_ratio: bool = True,
) -> Path:
    """이미지를 PDF로 변환한다.

    Args:
        image_paths: 변환할 이미지 파일 경로 리스트
        output_path: 출력 PDF 파일 경로
        keep_aspect_ratio: 종횡비 유지 여부

    Returns:
        생성된 출력 파일 경로
    """
    image_to_pdf(
        image_paths=image_paths,
        output_path=output_path,
        keep_aspect_ratio=keep_aspect_ratio,
    )
    return output_path
