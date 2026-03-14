"""페이지 범위 입력 GUI 위젯 모듈.

"1-3, 5, 8-10" 형식의 페이지 범위 입력 위젯이다.
"""

from __future__ import annotations

import customtkinter as ctk

from pdf_tool.gui.constants import (
    BORDER_RADIUS_DEFAULT,
    FONT_LABEL,
    INPUT_HEIGHT_DEFAULT,
    PADDING_MD,
)
from pdf_tool.gui.theme import get_current_palette
from pdf_tool.gui.widgets.page_range_input import validate_page_range_input


class PageRangeInputWidget(ctk.CTkFrame):
    """페이지 범위 입력 위젯.

    페이지 범위 문자열을 입력받고 실시간 검증한다.
    """

    def __init__(
        self,
        master: ctk.CTkFrame,
        label_text: str = "페이지 범위:",
        placeholder: str = "예: 1-3, 5, 8-10",
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)

        palette = get_current_palette()

        # 레이블
        self.label = ctk.CTkLabel(
            self,
            text=label_text,
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        self.label.pack(pady=(PADDING_MD, 0), padx=PADDING_MD, anchor="w")

        # 입력 필드
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            height=INPUT_HEIGHT_DEFAULT,
            corner_radius=BORDER_RADIUS_DEFAULT,
            fg_color=palette.surface_elevated,
            text_color=palette.text_primary,
            placeholder_text_color=palette.text_tertiary,
        )
        self.entry.pack(pady=PADDING_MD, padx=PADDING_MD, fill="x")

    def get_value(self) -> str:
        """입력된 페이지 범위 문자열을 반환한다.

        Returns:
            페이지 범위 문자열 (빈 문자열 가능)
        """
        return self.entry.get().strip()

    def is_valid(self) -> bool:
        """현재 입력값이 유효한지 확인한다.

        Returns:
            유효하면 True
        """
        return validate_page_range_input(self.get_value())
