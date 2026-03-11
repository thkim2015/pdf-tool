"""Cut 페이지 GUI 위젯 모듈."""

from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.pages.base_page_widget import BasePageWidget
from pdf_tool.gui.pages.cut_page import run_cut
from pdf_tool.gui.widgets.page_range_input_widget import PageRangeInputWidget


class CutPageWidget(BasePageWidget):
    """Cut 페이지 위젯. 페이지 범위 입력을 포함한다."""

    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """페이지 범위 입력 UI를 생성한다."""
        self.page_range_input = PageRangeInputWidget(parent)
        self.page_range_input.pack(fill="x")

    def execute_command(self, input_file: Path, output_path: Path):
        """잘라내기를 실행한다."""
        pages = self.page_range_input.get_value()
        return run_cut(input_file, pages, output_path)
