"""프로그레스 바 GUI 위젯 모듈.

비결정적(indeterminate) 모드의 진행률 표시 위젯이다.
"""

from __future__ import annotations

import customtkinter as ctk

from pdf_tool.gui.constants import FONT_SMALL, PADDING_MD
from pdf_tool.gui.theme import get_current_palette
from pdf_tool.gui.widgets.progress_bar import ProgressState


class ProgressBarWidget(ctk.CTkFrame):
    """프로그레스 바 위젯.

    비결정적 모드의 프로그레스 바와 상태 메시지를 표시한다.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        palette = get_current_palette()
        self._state = ProgressState()

        # 프로그레스 바
        self.progress = ctk.CTkProgressBar(
            self,
            mode="indeterminate",
            fg_color=palette.surface_elevated,
            progress_color=palette.primary,
        )
        self.progress.pack(pady=PADDING_MD, padx=PADDING_MD, fill="x")
        self.progress.set(0)

        # 상태 메시지
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            text_color=palette.text_secondary,
            font=ctk.CTkFont(FONT_SMALL[0], FONT_SMALL[1], FONT_SMALL[2]),
        )
        self.status_label.pack(pady=PADDING_MD, padx=PADDING_MD)

        # 초기에는 숨김
        self.pack_forget()

    def start(self, message: str = "처리 중...") -> None:
        """indeterminate 모드로 프로그레스 바를 시작한다."""
        self._state.start(message)
        self.progress.configure(mode="indeterminate")
        self.status_label.configure(text=message)
        self.progress.start()
        self.pack(fill="x", padx=PADDING_MD, pady=PADDING_MD)

    def start_determinate(self, total: int, message: str = "처리 중...") -> None:
        """determinate 모드로 프로그레스 바를 시작한다.

        Args:
            total: 전체 항목 수
            message: 표시할 상태 메시지
        """
        self._state.start_determinate(total, message)
        self.progress.configure(mode="determinate")
        self.progress.set(0)
        self.status_label.configure(text=message)
        self.pack(fill="x", padx=PADDING_MD, pady=PADDING_MD)

    def update_progress(self, current: int, total: int) -> None:
        """determinate 모드에서 진행률을 갱신한다.

        Args:
            current: 현재 처리된 항목 수
            total: 전체 항목 수
        """
        self._state.update_progress(current, total)
        self.progress.set(self._state.fraction)
        pct = int(self._state.fraction * 100)
        self.status_label.configure(text=f"{self._state.message} ({pct}%)")

    def stop(self) -> None:
        """프로그레스 바를 정지한다."""
        self._state.stop()
        self.progress.stop()
        self.pack_forget()

    def reset(self) -> None:
        """프로그레스 바를 초기화한다."""
        self._state.reset()
        self.progress.stop()
        self.progress.configure(mode="indeterminate")
        self.progress.set(0)
        self.status_label.configure(text="")
        self.pack_forget()
