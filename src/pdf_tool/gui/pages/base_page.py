"""BasePage 모듈.

모든 작업 페이지의 공통 로직을 제공한다.
순수 로직(경로 생성, 실행 상태)은 GUI 없이 테스트 가능하다.
"""

from __future__ import annotations

from pathlib import Path


def generate_output_path(input_path: Path, suffix: str = "_output") -> Path:
    """입력 파일 경로에 접미사를 붙인 출력 경로를 생성한다.

    Args:
        input_path: 입력 파일 경로
        suffix: 파일 이름에 추가할 접미사 (기본값: "_output")

    Returns:
        접미사가 추가된 출력 파일 경로
    """
    return input_path.with_stem(input_path.stem + suffix)


def would_overwrite(input_path: Path, output_path: Path | None) -> bool:
    """출력 파일이 입력 파일을 덮어쓰는지 확인한다.

    Args:
        input_path: 입력 파일 경로
        output_path: 출력 파일 경로 (None이면 덮어쓰기 없음)

    Returns:
        같은 경로이면 True
    """
    if output_path is None:
        return False
    return input_path.resolve() == output_path.resolve()


class ExecutionState:
    """커맨드 실행 상태를 관리하는 클래스.

    파일 로드 여부와 실행 중 상태를 추적하여
    실행 버튼 활성화/비활성화를 결정한다.
    """

    def __init__(self) -> None:
        self.is_executing: bool = False
        self.input_file: Path | None = None

    @property
    def can_execute(self) -> bool:
        """현재 실행 가능한 상태인지 반환한다.

        파일이 로드되어 있고 실행 중이 아닐 때만 실행 가능하다.

        Returns:
            실행 가능하면 True
        """
        return self.input_file is not None and not self.is_executing

    def start(self, input_file: Path) -> None:
        """실행을 시작한다.

        Args:
            input_file: 실행할 입력 파일 경로
        """
        self.is_executing = True
        self.input_file = input_file

    def finish(self) -> None:
        """실행을 완료한다."""
        self.is_executing = False
