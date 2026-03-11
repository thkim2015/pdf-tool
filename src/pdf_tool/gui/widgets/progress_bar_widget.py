"""프로그레스 바 GUI 위젯 모듈.

비결정적(indeterminate) 모드의 진행률 표시 위젯이다.
"""

from __future__ import annotations

import customtkinter as ctk

from pdf_tool.gui.widgets.progress_bar import ProgressState


class ProgressBarWidget(ctk.CTkFrame):
    """프로그레스 바 위젯.

    비결정적 모드의 프로그레스 바와 상태 메시지를 표시한다.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self._state = ProgressState()

        # 프로그레스 바
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.pack(pady=5, padx=10, fill="x")
        self.progress.set(0)

        # 상태 메시지
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=2, padx=10)

        # 초기에는 숨김
        self.pack_forget()

    def start(self, message: str = "처리 중...") -> None:
        """프로그레스 바를 시작한다."""
        self._state.start(message)
        self.status_label.configure(text=message)
        self.progress.start()
        self.pack(fill="x", padx=5, pady=5)

    def stop(self) -> None:
        """프로그레스 바를 정지한다."""
        self._state.stop()
        self.progress.stop()
        self.pack_forget()

    def reset(self) -> None:
        """프로그레스 바를 초기화한다."""
        self._state.reset()
        self.progress.stop()
        self.progress.set(0)
        self.status_label.configure(text="")
        self.pack_forget()
