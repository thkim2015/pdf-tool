"""Rotate 페이지 GUI 위젯 모듈."""

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
from pdf_tool.gui.pages.rotate_page import run_rotate
from pdf_tool.gui.widgets.page_range_input_widget import PageRangeInputWidget


class RotatePageWidget(BasePageWidget):
    """Rotate 페이지 위젯. 각도 선택과 선택적 페이지 범위를 포함한다."""

    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """회전 파라미터 UI를 생성한다."""
        # 각도 선택
        angle_label = ctk.CTkLabel(parent, text="회전 각도:")
        angle_label.pack(pady=(5, 0), padx=10, anchor="w")

        self.angle_var = ctk.StringVar(value="90")
        self.angle_menu = ctk.CTkOptionMenu(
            parent,
            values=["90", "180", "270"],
            variable=self.angle_var,
        )
        self.angle_menu.pack(pady=5, padx=10, fill="x")

        # 선택적 페이지 범위
        self.page_range_input = PageRangeInputWidget(
            parent,
            label_text="페이지 범위 (선택):",
            placeholder="비워두면 전체 페이지",
        )
        self.page_range_input.pack(fill="x")

    def execute_command(self, input_file: Path, output_path: Path):
        """회전을 실행한다."""
        angle = int(self.angle_var.get())
        pages = self.page_range_input.get_value() or None
        return run_rotate(input_file, angle, pages, output_path)
