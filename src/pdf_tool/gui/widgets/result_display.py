"""결과 표시 위젯 모듈.

작업 결과(성공, 에러, 정보)를 표시하는 위젯의 상태를 관리한다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class ResultState:
    """결과 표시 상태를 관리하는 클래스.

    성공, 에러, 정보 결과를 저장하고 표시 데이터를 제공한다.
    """

    def __init__(self) -> None:
        self.result_type: str | None = None
        self.message: str = ""
        self.output_path: Path | None = None
        self.data: dict[str, Any] | None = None

    def show_success(self, message: str, output_path: Path) -> None:
        """성공 결과를 설정한다.

        Args:
            message: 성공 메시지
            output_path: 출력 파일 경로
        """
        self.result_type = "success"
        self.message = message
        self.output_path = output_path
        self.data = None

    def show_error(self, message: str) -> None:
        """에러 결과를 설정한다.

        Args:
            message: 에러 메시지
        """
        self.result_type = "error"
        self.message = message
        self.output_path = None
        self.data = None

    def show_info(self, data: dict[str, Any]) -> None:
        """정보 결과를 설정한다.

        Args:
            data: 표시할 키-값 데이터
        """
        self.result_type = "info"
        self.data = data
        self.message = ""
        self.output_path = None

    def clear(self) -> None:
        """결과를 초기화한다."""
        self.result_type = None
        self.message = ""
        self.output_path = None
        self.data = None
