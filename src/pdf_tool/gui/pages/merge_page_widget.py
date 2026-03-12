"""Merge 페이지 GUI 위젯 모듈.

FileList 위젯을 사용하여 BasePage 레이아웃을 오버라이드한다.
"""

from __future__ import annotations

import threading
import tkinter.filedialog as fd
from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.app import format_exception_message
from pdf_tool.gui.pages.merge_page import run_merge
from pdf_tool.gui.widgets.file_list_widget import FileListWidget
from pdf_tool.gui.widgets.progress_bar_widget import ProgressBarWidget
from pdf_tool.gui.widgets.result_display_widget import ResultDisplayWidget


class MergePageWidget(ctk.CTkFrame):
    """Merge 페이지 위젯.

    단일 FilePicker 대신 FileList를 사용하여 다중 파일을 지원한다.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self._is_executing = False

        # 파일 목록
        self.file_list = FileListWidget(
            self,
            on_list_changed=self._on_list_changed,
        )
        self.file_list.pack(fill="both", expand=True, padx=10, pady=5)

        # 실행 버튼
        self.execute_btn = ctk.CTkButton(
            self,
            text="병합 실행",
            command=self._on_execute,
            state="disabled",
        )
        self.execute_btn.pack(pady=10, padx=10, fill="x")

        # 프로그레스 바
        self.progress_bar = ProgressBarWidget(self)

        # 결과 표시
        self.result_display = ResultDisplayWidget(self)
        self.result_display.pack(fill="x", padx=10, pady=5)

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
