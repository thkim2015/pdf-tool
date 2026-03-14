"""Info 페이지 GUI 위젯 모듈.

파일 로드 시 즉시 메타데이터를 표시한다. 실행 버튼 없음.
"""

from __future__ import annotations

import threading
from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.app import format_exception_message
from pdf_tool.gui.constants import PADDING_MD
from pdf_tool.gui.pages.info_page import load_metadata
from pdf_tool.gui.widgets.file_picker_widget import FilePickerWidget
from pdf_tool.gui.widgets.result_display_widget import ResultDisplayWidget


class InfoPageWidget(ctk.CTkFrame):
    """Info 페이지 위젯.

    파일 선택 시 즉시 메타데이터를 로드하고 키-값 테이블로 표시한다.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        # 파일 선택
        self.file_picker = FilePickerWidget(
            self,
            on_file_selected=self._on_file_selected,
        )
        self.file_picker.pack(fill="x", padx=PADDING_MD, pady=PADDING_MD)

        # 결과 표시
        self.result_display = ResultDisplayWidget(self)
        self.result_display.pack(fill="both", expand=True, padx=PADDING_MD, pady=PADDING_MD)

    def _on_file_selected(self, path: Path) -> None:
        """파일이 선택되면 메타데이터를 로드한다."""
        self.result_display.clear()
        thread = threading.Thread(
            target=self._load_in_thread,
            args=(path,),
            daemon=True,
        )
        thread.start()

    def _load_in_thread(self, path: Path) -> None:
        """백그라운드에서 메타데이터를 로드한다."""
        try:
            metadata = load_metadata(path)
            self.after(0, lambda: self.result_display.show_info(metadata))
        except Exception as exc:
            self.after(0, lambda e=exc: self.result_display.show_error(
                format_exception_message(e)
            ))
