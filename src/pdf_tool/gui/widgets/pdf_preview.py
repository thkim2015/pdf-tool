"""PDF 미리보기 렌더링 모듈.

pypdfium2를 이용하여 PDF 첫 번째 페이지를 PIL Image로 렌더링한다.
GUI 의존성 없이 순수 렌더링 로직만 포함한다.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image

try:
    import pypdfium2 as pdfium

    _pdfium_available = True
except ImportError:
    _pdfium_available = False


def render_first_page(
    pdf_path: str | Path,
    max_width: int = 300,
) -> Image.Image:
    """PDF 첫 번째 페이지를 PIL Image로 렌더링한다.

    Args:
        pdf_path: PDF 파일 경로.
        max_width: 썸네일 최대 너비 (픽셀).

    Returns:
        첫 페이지의 PIL Image 썸네일.

    Raises:
        ValueError: PDF에 페이지가 없을 때.
        RuntimeError: PDF 열기 또는 렌더링 실패 시.
    """
    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        if len(pdf) == 0:
            raise ValueError("PDF에 페이지가 없습니다")

        page = pdf[0]
        bitmap = page.render()
        pil_image = bitmap.to_pil()
    finally:
        pdf.close()

    # 종횡비를 유지하며 썸네일 리사이즈
    max_height = int(max_width * 1.4)
    pil_image.thumbnail((max_width, max_height))
    return pil_image


def is_preview_available() -> bool:
    """pypdfium2가 설치되어 미리보기 가능한지 확인한다.

    Returns:
        pypdfium2 import 가능 시 True, 아니면 False.
    """
    return _pdfium_available


def open_pdf_in_viewer(pdf_path: str | Path) -> None:
    """시스템 기본 PDF 뷰어로 파일을 연다.

    Args:
        pdf_path: 열 PDF 파일 경로.
    """
    path_str = str(pdf_path)

    if sys.platform == "darwin":
        subprocess.Popen(["open", path_str])
    elif sys.platform == "win32":
        subprocess.Popen(["start", "", path_str], shell=True)  # noqa: S603
    else:
        subprocess.Popen(["xdg-open", path_str])
