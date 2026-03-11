"""결과 표시 GUI 위젯 모듈.

작업 결과(성공, 에러, 정보)를 GUI로 표시하는 위젯이다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import customtkinter as ctk

from pdf_tool.gui.widgets.result_display import ResultState


class ResultDisplayWidget(ctk.CTkFrame):
    """결과 표시 위젯.

    성공(초록), 에러(빨강), 정보(키-값) 결과를 표시한다.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self._state = ResultState()

        # 결과 메시지 레이블
        self.message_label = ctk.CTkLabel(self, text="", wraplength=500)
        self.message_label.pack(pady=5, padx=10, fill="x")

        # 경로 레이블 (성공 시 출력 경로 표시)
        self.path_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.path_label.pack(pady=2, padx=10, fill="x")

        # 정보 표시 프레임 (dict 결과용)
        self.info_frame = ctk.CTkFrame(self)
        self._info_labels: list[ctk.CTkLabel] = []

    def show_success(self, message: str, output_path: Path) -> None:
        """성공 결과를 표시한다."""
        self._state.show_success(message, output_path)
        self._clear_info()
        self.message_label.configure(text=message, text_color="green")
        self.path_label.configure(text=str(output_path))
        self.info_frame.pack_forget()

    def show_error(self, message: str) -> None:
        """에러 결과를 표시한다."""
        self._state.show_error(message)
        self._clear_info()
        self.message_label.configure(text=message, text_color="red")
        self.path_label.configure(text="")
        self.info_frame.pack_forget()

    def show_info(self, data: dict[str, Any]) -> None:
        """정보(dict)를 키-값 테이블로 표시한다."""
        self._state.show_info(data)
        self.message_label.configure(text="", text_color="gray")
        self.path_label.configure(text="")
        self._clear_info()

        self.info_frame.pack(pady=5, padx=10, fill="both", expand=True)
        for key, value in data.items():
            label = ctk.CTkLabel(
                self.info_frame,
                text=f"{key}: {value}",
                anchor="w",
            )
            label.pack(padx=10, pady=2, fill="x")
            self._info_labels.append(label)

    def clear(self) -> None:
        """결과를 초기화한다."""
        self._state.clear()
        self.message_label.configure(text="", text_color="gray")
        self.path_label.configure(text="")
        self._clear_info()
        self.info_frame.pack_forget()

    def _clear_info(self) -> None:
        """정보 레이블을 제거한다."""
        for label in self._info_labels:
            label.destroy()
        self._info_labels.clear()
