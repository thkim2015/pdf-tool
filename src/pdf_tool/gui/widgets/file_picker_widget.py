"""파일 선택 GUI 위젯 모듈.

CustomTkinter 기반의 PDF 파일 선택 위젯이다.
드래그 앤 드롭과 파일 다이얼로그를 지원한다.
"""

from __future__ import annotations

import tkinter.filedialog as fd
from collections.abc import Callable
from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.widgets.file_picker import get_pdf_info, is_valid_pdf_extension


class FilePickerWidget(ctk.CTkFrame):
    """PDF 파일 선택 위젯.

    파일 선택 버튼과 선택된 파일 정보를 표시한다.
    """

    def __init__(
        self,
        master: ctk.CTkFrame,
        on_file_selected: Callable[[Path], None] | None = None,
        file_types: list[tuple[str, str]] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)

        self._on_file_selected = on_file_selected
        self._file_types = file_types or [("PDF 파일", "*.pdf")]
        self._selected_file: Path | None = None

        self._create_ui()
        self._setup_drag_and_drop()

    def _create_ui(self) -> None:
        """UI 컴포넌트를 생성한다."""
        # 파일 선택 버튼
        self.select_btn = ctk.CTkButton(
            self,
            text="파일 선택...",
            command=self._open_dialog,
        )
        self.select_btn.pack(pady=5, padx=10, fill="x")

        # 파일 정보 레이블
        self.info_label = ctk.CTkLabel(
            self,
            text="파일을 선택하거나 드래그 앤 드롭하세요",
            text_color="gray",
        )
        self.info_label.pack(pady=5, padx=10)

    def _setup_drag_and_drop(self) -> None:
        """드래그 앤 드롭을 설정한다. tkinterdnd2가 없으면 무시한다."""
        try:
            self.drop_target_register("DND_Files")  # type: ignore[attr-defined]
            self.dnd_bind("<<Drop>>", self._on_drop)  # type: ignore[attr-defined]
        except (AttributeError, Exception):
            # tkinterdnd2가 없거나 지원하지 않는 경우 무시
            pass

    def _on_drop(self, event) -> None:
        """드래그 앤 드롭 이벤트 핸들러."""
        file_path = Path(event.data.strip().strip("{}"))
        self._try_select_file(file_path)

    def _open_dialog(self) -> None:
        """파일 선택 다이얼로그를 열고 파일을 선택한다."""
        file_path = fd.askopenfilename(filetypes=self._file_types)
        if file_path:
            self._try_select_file(Path(file_path))

    def _try_select_file(self, path: Path) -> None:
        """파일을 선택하고 유효성을 검증한다."""
        if not is_valid_pdf_extension(path):
            self.info_label.configure(
                text="PDF 파일만 선택할 수 있습니다",
                text_color="red",
            )
            return

        info = get_pdf_info(path)
        if info is None:
            self.info_label.configure(
                text="PDF 파일을 읽을 수 없습니다",
                text_color="red",
            )
            return

        self._selected_file = path
        self.info_label.configure(
            text=f"{info['name']} ({info['pages']}페이지)",
            text_color=("gray10", "gray90"),
        )

        if self._on_file_selected:
            self._on_file_selected(path)

    @property
    def selected_file(self) -> Path | None:
        """현재 선택된 파일 경로를 반환한다."""
        return self._selected_file
