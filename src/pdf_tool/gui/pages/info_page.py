"""Info 페이지 모듈.

PDF 메타데이터를 조회하여 표시한다.
파일 로드 시 즉시 get_metadata()를 호출하고 결과를 키-값 테이블로 표시한다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pdf_tool.commands.info import get_metadata


def load_metadata(input_path: Path) -> dict[str, Any]:
    """PDF 메타데이터를 로드한다.

    Args:
        input_path: PDF 파일 경로

    Returns:
        메타데이터 딕셔너리

    Raises:
        Exception: 파일을 읽을 수 없을 때
    """
    return get_metadata(input_path)
