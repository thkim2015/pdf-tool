"""Rotate 페이지 GUI 위젯 모듈."""

from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.constants import (
    FONT_LABEL,
    OPTIONMENU_HEIGHT_DEFAULT,
    PADDING_MD,
    SECTION_LABEL_PADDING,
    SECTION_SPACING,
)
from pdf_tool.gui.pages.base_page_widget import BasePageWidget
from pdf_tool.gui.pages.rotate_page import run_rotate
from pdf_tool.gui.theme import get_current_palette
from pdf_tool.gui.widgets.page_range_input_widget import PageRangeInputWidget


class RotatePageWidget(BasePageWidget):
    """Rotate 페이지 위젯. 각도 선택과 선택적 페이지 범위를 포함한다."""

    page_title = "회전"
    action_button_text = "회전"

    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """회전 파라미터 UI를 생성한다."""
        palette = get_current_palette()

        # 각도 선택
        angle_label = ctk.CTkLabel(
            parent,
            text="회전 각도:",
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        angle_label.pack(pady=SECTION_LABEL_PADDING, padx=PADDING_MD, anchor="w")

        self.angle_var = ctk.StringVar(value="90")
        self.angle_menu = ctk.CTkOptionMenu(
            parent,
            values=["90", "180", "270"],
            variable=self.angle_var,
            height=OPTIONMENU_HEIGHT_DEFAULT,
        )
        self.angle_menu.pack(pady=(0, SECTION_SPACING), padx=PADDING_MD, fill="x")

        # 선택적 페이지 범위
        self.page_range_input = PageRangeInputWidget(
            parent,
            label_text="페이지 범위 (선택):",
            placeholder="비워두면 전체 페이지",
        )
        self.page_range_input.pack(fill="x", padx=PADDING_MD, pady=(0, SECTION_SPACING))

    def execute_command(self, input_file: Path, output_path: Path):
        """회전을 실행한다."""
        angle = int(self.angle_var.get())
        pages = self.page_range_input.get_value() or None
        return run_rotate(input_file, angle, pages, output_path)
