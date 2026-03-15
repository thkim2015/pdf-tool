"""Watermark 페이지 모듈.

PDF에 텍스트 또는 이미지 워터마크를 추가한다.
"""

from __future__ import annotations

from pathlib import Path

from pdf_tool.commands.watermark import watermark_pdf
from pdf_tool.core.progress import ProgressCallback


def run_watermark(
    input_path: Path,
    output_path: Path,
    text: str | None = None,
    image: Path | None = None,
    opacity: float = 0.3,
    rotation: float = 45.0,
    position: str = "center",
    pages: str | None = None,
    callback: ProgressCallback = None,
) -> Path:
    """워터마크를 추가한다.

    Args:
        input_path: 입력 PDF 파일 경로
        output_path: 출력 PDF 파일 경로
        text: 텍스트 워터마크 (image와 배타적)
        image: 이미지 워터마크 파일 경로 (text와 배타적)
        opacity: 투명도 (0.0~1.0)
        rotation: 회전 각도 (0~360)
        position: 위치 (center 등)
        pages: 적용할 페이지 범위 (None이면 전체)
        callback: 진행 상황 콜백

    Returns:
        생성된 출력 파일 경로
    """
    return watermark_pdf(
        input_path,
        output=output_path,
        text=text,
        image=image,
        opacity=opacity,
        rotation=rotation,
        position=position,
        pages=pages,
        callback=callback,
    )
