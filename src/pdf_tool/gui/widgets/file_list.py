"""파일 목록 위젯 모듈.

머지 기능을 위한 다중 파일 관리를 지원한다.
"""

from __future__ import annotations

from pathlib import Path


class FileListState:
    """파일 목록의 상태를 관리하는 클래스.

    파일 추가, 제거, 순서 변경 로직을 담당한다.
    """

    def __init__(self) -> None:
        self._files: list[Path] = []

    def get_files(self) -> list[Path]:
        """현재 파일 목록을 반환한다.

        Returns:
            파일 경로 리스트의 복사본
        """
        return list(self._files)

    def add_files(self, files: list[Path]) -> None:
        """파일을 목록에 추가한다.

        Args:
            files: 추가할 파일 경로 리스트
        """
        self._files.extend(files)

    def remove_file(self, index: int) -> None:
        """인덱스로 파일을 제거한다.

        Args:
            index: 제거할 파일의 인덱스
        """
        if 0 <= index < len(self._files):
            self._files.pop(index)

    def move_up(self, index: int) -> None:
        """파일을 한 칸 위로 이동한다.

        Args:
            index: 이동할 파일의 인덱스
        """
        if index > 0 and index < len(self._files):
            self._files[index - 1], self._files[index] = (
                self._files[index],
                self._files[index - 1],
            )

    def move_down(self, index: int) -> None:
        """파일을 한 칸 아래로 이동한다.

        Args:
            index: 이동할 파일의 인덱스
        """
        if index >= 0 and index < len(self._files) - 1:
            self._files[index], self._files[index + 1] = (
                self._files[index + 1],
                self._files[index],
            )
