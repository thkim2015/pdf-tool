"""Merge 페이지 GUI 위젯 모듈.

FileList 위젯을 사용하여 다중 파일 병합을 지원한다.
3단 레이아웃 (툴바, 컨텐츠, 액션바) 직접 구성.
"""

from __future__ import annotations

import threading
import tkinter.filedialog as fd
from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.app import format_exception_message
from pdf_tool.gui.constants import (
    BORDER_RADIUS_DEFAULT,
    PADDING_MD,
)
from pdf_tool.gui.pages.base_page_widget import (
    ACTION_BAR_PADDING,
    CONTENT_PADX,
    CONTENT_TOP_MARGIN,
    TOOLBAR_PADX,
    get_action_bar_style,
    get_toolbar_style,
)
from pdf_tool.gui.pages.merge_page import run_merge
from pdf_tool.gui.theme import get_current_palette
from pdf_tool.gui.widgets.file_list_widget import FileListWidget
from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle
from pdf_tool.gui.widgets.progress_bar_widget import ProgressBarWidget
from pdf_tool.gui.widgets.result_display_widget import ResultDisplayWidget


class MergePageWidget(ctk.CTkFrame):
    """Merge 페이지 위젯.

    단일 FilePicker 대신 FileList를 사용하여 다중 파일을 지원한다.
    3단 레이아웃 (툴바, 컨텐츠, 액션바) 적용.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        palette = get_current_palette()
        toolbar_style = get_toolbar_style()
        action_style = get_action_bar_style()
        self._is_executing = False

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
            text="병합",
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

        # 병합 버튼
        button_style = MacOSButtonStyle.get_style("primary", "large")
        hover_color = MacOSButtonStyle.get_hover_color("primary")

        button_container = ctk.CTkFrame(
            self.action_bar_frame,
            fg_color="transparent",
        )
        button_container.pack(fill="both", expand=True, padx=CONTENT_PADX, pady=ACTION_BAR_PADDING)

        self.execute_btn = ctk.CTkButton(
            button_container,
            text="병합",
            command=self._on_execute,
            state="disabled",
            height=action_style["button_height"],
            corner_radius=BORDER_RADIUS_DEFAULT,
            fg_color=button_style["bg_color"],
            text_color=button_style["text_color"],
            hover_color=hover_color,
        )
        self.execute_btn.pack(side="right")

        # ===== 중앙: 컨텐츠 =====
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=palette.surface,
        )
        self.content_frame.pack(fill="both", expand=True)

        # 파일 목록
        self.file_list = FileListWidget(
            self.content_frame,
            on_list_changed=self._on_list_changed,
        )
        self.file_list.pack(
            fill="both",
            expand=True,
            padx=CONTENT_PADX,
            pady=(CONTENT_TOP_MARGIN, PADDING_MD),
        )

        # 프로그레스 바
        self.progress_bar = ProgressBarWidget(self.content_frame)

        # 결과 표시
        self.result_display = ResultDisplayWidget(self.content_frame)
        self.result_display.pack(
            fill="x",
            padx=CONTENT_PADX,
            pady=PADDING_MD,
        )

    def _on_list_changed(self) -> None:
        """파일 목록이 변경되면 실행 버튼 상태를 갱신한다."""
        files = self.file_list.get_files()
        if len(files) >= 2 and not self._is_executing:
            self.execute_btn.configure(state="normal")
        else:
            self.execute_btn.configure(state="disabled")

    def _on_execute(self) -> None:
        """병합을 실행한다."""
        files = self.file_list.get_files()
        if len(files) < 2:
            return

        # 출력 경로를 사용자에게 선택하게 함
        output_path = fd.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF 파일", "*.pdf")],
            initialfile="merged.pdf",
        )
        if not output_path:
            return

        self._is_executing = True
        self.execute_btn.configure(state="disabled")
        self.result_display.clear()
        self.progress_bar.start("병합 중...")

        thread = threading.Thread(
            target=self._merge_in_thread,
            args=(files, Path(output_path)),
            daemon=True,
        )
        thread.start()

    def _merge_in_thread(self, files: list[Path], output_path: Path) -> None:
        """백그라운드에서 병합을 실행한다."""
        try:
            result = run_merge(files, output_path)
            self.after(0, lambda: self._on_success(result))
        except Exception as exc:
            self.after(0, lambda e=exc: self._on_error(e))

    def _on_success(self, result: Path) -> None:
        """병합 성공 처리."""
        self._is_executing = False
        self.progress_bar.stop()
        self._on_list_changed()
        self.result_display.show_success("병합 완료!", result)

    def _on_error(self, exc: Exception) -> None:
        """병합 에러 처리."""
        self._is_executing = False
        self.progress_bar.stop()
        self._on_list_changed()
        self.result_display.show_error(format_exception_message(exc))
