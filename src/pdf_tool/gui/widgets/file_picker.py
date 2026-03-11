"""파일 선택 위젯 모듈.

PDF 파일 선택 및 드래그 앤 드롭을 지원하는 위젯이다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pypdf import PdfReader


def is_valid_pdf_extension(path: Path) -> bool:
    """파일 확장자가 PDF인지 검증한다.

    Args:
        path: 검증할 파일 경로

    Returns:
        PDF 확장자이면 True
    """
    return path.suffix.lower() == ".pdf"


def get_pdf_info(path: Path) -> dict[str, Any] | None:
    """PDF 파일의 기본 정보를 추출한다.

    Args:
        path: PDF 파일 경로

    Returns:
        파일 이름과 페이지 수를 담은 딕셔너리, 실패 시 None
    """
    try:
        reader = PdfReader(path)
        return {
            "name": path.name,
            "pages": len(reader.pages),
        }
    except Exception:
        return None
