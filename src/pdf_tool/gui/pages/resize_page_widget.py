"""Resize 페이지 GUI 위젯 모듈."""

from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.constants import (
    BORDER_RADIUS_DEFAULT,
    BUTTON_HEIGHT_DEFAULT,
    PADDING_LG,
    PADDING_MD,
)
from pdf_tool.gui.theme import get_current_palette

from pdf_tool.gui.pages.base_page_widget import BasePageWidget
from pdf_tool.gui.pages.resize_page import run_resize


class ResizePageWidget(BasePageWidget):
    """Resize 페이지 위젯. 용지 크기와 모드 선택을 포함한다."""

    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """리사이즈 파라미터 UI를 생성한다."""
        # 용지 크기 선택
        size_label = ctk.CTkLabel(parent, text="용지 크기:")
        size_label.pack(pady=(5, 0), padx=10, anchor="w")

        self.size_var = ctk.StringVar(value="A4")
        self.size_menu = ctk.CTkOptionMenu(
            parent,
            values=["A3", "A4", "A5", "Letter", "Legal"],
            variable=self.size_var,
        )
        self.size_menu.pack(pady=5, padx=10, fill="x")

        # 모드 선택
        mode_label = ctk.CTkLabel(parent, text="모드:")
        mode_label.pack(pady=(5, 0), padx=10, anchor="w")

        self.mode_var = ctk.StringVar(value="fit")
        self.mode_menu = ctk.CTkOptionMenu(
            parent,
            values=["fit", "stretch", "fill"],
            variable=self.mode_var,
        )
        self.mode_menu.pack(pady=5, padx=10, fill="x")

    def execute_command(self, input_file: Path, output_path: Path):
        """크기 변경을 실행한다."""
        return run_resize(input_file, self.size_var.get(), self.mode_var.get(), output_path)
