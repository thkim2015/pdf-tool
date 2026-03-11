"""페이지 범위 입력 GUI 위젯 모듈.

"1-3, 5, 8-10" 형식의 페이지 범위 입력 위젯이다.
"""

from __future__ import annotations

import customtkinter as ctk

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

        # 레이블
        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.pack(pady=(5, 0), padx=10, anchor="w")

        # 입력 필드
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder)
        self.entry.pack(pady=5, padx=10, fill="x")

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
