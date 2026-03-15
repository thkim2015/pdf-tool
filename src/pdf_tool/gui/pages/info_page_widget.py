"""Info 페이지 GUI 위젯 모듈.

파일 로드 시 즉시 메타데이터를 표시한다.
3단 레이아웃을 직접 구성한다 (BasePageWidget 미사용).
"""

from __future__ import annotations

import threading
from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.app import format_exception_message
from pdf_tool.gui.constants import PADDING_MD
from pdf_tool.gui.pages.base_page_widget import (
    ACTION_BAR_PADDING,
    CONTENT_PADX,
    CONTENT_TOP_MARGIN,
    TOOLBAR_PADX,
    get_action_bar_style,
    get_toolbar_style,
)
from pdf_tool.gui.pages.info_page import load_metadata
from pdf_tool.gui.theme import get_current_palette
from pdf_tool.gui.widgets.file_picker_widget import FilePickerWidget
from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle
from pdf_tool.gui.widgets.result_display_widget import ResultDisplayWidget


class InfoPageWidget(ctk.CTkFrame):
    """Info 페이지 위젯.

    파일 선택 시 즉시 메타데이터를 로드하고 키-값 테이블로 표시한다.
    3단 레이아웃 (툴바, 컨텐츠, 액션바) 적용.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        palette = get_current_palette()
        toolbar_style = get_toolbar_style()
        action_style = get_action_bar_style()

        # ===== 상단: 툴바 =====
        self.toolbar_frame = ctk.CTkFrame(
            self,
            height=toolbar_style["height"],
            fg_color=palette.vibrancy_bg,
            corner_radius=0,
        )
        self.toolbar_frame.pack(fill="x", side="top")
        self.toolbar_frame.pack_propagate(False)

        ctk.CTkLabel(
            self.toolbar_frame,
            text="정보",
            text_color=palette.text_primary,
            font=ctk.CTkFont(
                "System",
                toolbar_style["title_font_size"],
                toolbar_style["title_weight"],
            ),
        ).pack(side="left", padx=TOOLBAR_PADX)

        # ===== 하단: 액션 바 =====
        self.action_bar_frame = ctk.CTkFrame(
            self,
            height=action_style["height"],
            fg_color=palette.surface,
            corner_radius=0,
        )
        self.action_bar_frame.pack(fill="x", side="bottom")
        self.action_bar_frame.pack_propagate(False)

        # 분리선
        ctk.CTkFrame(
            self.action_bar_frame,
            height=action_style["separator_height"],
            fg_color=action_style["separator_color"],
            corner_radius=0,
        ).pack(fill="x", side="top")

        # 새로고침 버튼
        button_style = MacOSButtonStyle.get_style("primary", "large")
        hover_color = MacOSButtonStyle.get_hover_color("primary")

        button_container = ctk.CTkFrame(
            self.action_bar_frame,
            fg_color="transparent",
        )
        button_container.pack(fill="both", expand=True, padx=CONTENT_PADX, pady=ACTION_BAR_PADDING)

        self.refresh_btn = ctk.CTkButton(
            button_container,
            text="새로고침",
            command=self._on_refresh,
            state="disabled",
            height=action_style["button_height"],
            fg_color=button_style["bg_color"],
            text_color=button_style["text_color"],
            hover_color=hover_color,
        )
        self.refresh_btn.pack(side="right")

        # ===== 중앙: 컨텐츠 =====
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=palette.surface,
        )
        self.content_frame.pack(fill="both", expand=True)

        # 파일 선택
        self.file_picker = FilePickerWidget(
            self.content_frame,
            on_file_selected=self._on_file_selected,
        )
        self.file_picker.pack(
            fill="x",
            padx=CONTENT_PADX,
            pady=(CONTENT_TOP_MARGIN, PADDING_MD),
        )

        # 결과 표시
        self.result_display = ResultDisplayWidget(self.content_frame)
        self.result_display.pack(
            fill="both",
            expand=True,
            padx=CONTENT_PADX,
            pady=PADDING_MD,
        )

        self._current_path: Path | None = None

    def _on_file_selected(self, path: Path) -> None:
        """파일이 선택되면 메타데이터를 로드한다."""
        self._current_path = path
        self.refresh_btn.configure(state="normal")
        self.result_display.clear()
        thread = threading.Thread(
            target=self._load_in_thread,
            args=(path,),
            daemon=True,
        )
        thread.start()

    def _on_refresh(self) -> None:
        """새로고침 버튼 클릭 핸들러."""
        if self._current_path is not None:
            self._on_file_selected(self._current_path)

    def _load_in_thread(self, path: Path) -> None:
        """백그라운드에서 메타데이터를 로드한다."""
        try:
            metadata = load_metadata(path)
            self.after(0, lambda: self.result_display.show_info(metadata))
        except Exception as exc:
            self.after(0, lambda e=exc: self.result_display.show_error(
                format_exception_message(e)
            ))
