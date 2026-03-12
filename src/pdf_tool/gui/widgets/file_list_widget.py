"""파일 목록 GUI 위젯 모듈.

머지 기능을 위한 다중 파일 선택 및 순서 관리 위젯이다.
"""

from __future__ import annotations

import tkinter.filedialog as fd
from collections.abc import Callable
from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.widgets.file_list import FileListState


class FileListWidget(ctk.CTkFrame):
    """파일 목록 위젯.

    파일 추가, 제거, 순서 변경을 지원한다.
    """

    def __init__(
        self,
        master: ctk.CTkFrame,
        on_list_changed: Callable[[], None] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)

        self._state = FileListState()
        self._on_list_changed = on_list_changed
        self._item_widgets: list[ctk.CTkFrame] = []

        self._create_ui()

    def _create_ui(self) -> None:
        """UI 컴포넌트를 생성한다."""
        # 파일 추가 버튼
        self.add_btn = ctk.CTkButton(
            self,
            text="파일 추가...",
            command=self._add_files,
        )
        self.add_btn.pack(pady=5, padx=10, fill="x")

        # 파일 목록 스크롤 프레임
        self.list_frame = ctk.CTkScrollableFrame(self, height=200)
        self.list_frame.pack(pady=5, padx=10, fill="both", expand=True)

    def _add_files(self) -> None:
        """파일 선택 다이얼로그로 파일을 추가한다."""
        files = fd.askopenfilenames(filetypes=[("PDF 파일", "*.pdf")])
        if files:
            self._state.add_files([Path(f) for f in files])
            self._refresh_list()

    def _refresh_list(self) -> None:
        """파일 목록 UI를 갱신한다."""
        # 기존 위젯 제거
        for widget in self._item_widgets:
            widget.destroy()
        self._item_widgets.clear()

        # 새 위젯 생성
        for i, file_path in enumerate(self._state.get_files()):
            item = self._create_item(i, file_path)
            self._item_widgets.append(item)

        if self._on_list_changed:
            self._on_list_changed()

    def _create_item(self, index: int, file_path: Path) -> ctk.CTkFrame:
        """파일 목록 항목 위젯을 생성한다."""
        frame = ctk.CTkFrame(self.list_frame)
        frame.pack(fill="x", pady=2)

        # 파일 이름 레이블
        label = ctk.CTkLabel(frame, text=file_path.name, anchor="w")
        label.pack(side="left", padx=5, fill="x", expand=True)

        # 위로 이동 버튼
        up_btn = ctk.CTkButton(
            frame, text="^", width=30,
            command=lambda: self._move_up(index),
        )
        up_btn.pack(side="left", padx=2)

        # 아래로 이동 버튼
        down_btn = ctk.CTkButton(
            frame, text="v", width=30,
            command=lambda: self._move_down(index),
        )
        down_btn.pack(side="left", padx=2)

        # 제거 버튼
        remove_btn = ctk.CTkButton(
            frame, text="X", width=30, fg_color="red",
            command=lambda: self._remove(index),
        )
        remove_btn.pack(side="left", padx=2)

        return frame

    def _move_up(self, index: int) -> None:
        """파일을 위로 이동한다."""
        self._state.move_up(index)
        self._refresh_list()

    def _move_down(self, index: int) -> None:
        """파일을 아래로 이동한다."""
        self._state.move_down(index)
        self._refresh_list()

    def _remove(self, index: int) -> None:
        """파일을 제거한다."""
        self._state.remove_file(index)
        self._refresh_list()

    def get_files(self) -> list[Path]:
        """현재 파일 목록을 반환한다."""
        return self._state.get_files()
