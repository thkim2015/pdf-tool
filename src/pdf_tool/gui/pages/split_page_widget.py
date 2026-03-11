"""Split 페이지 GUI 위젯 모듈."""

from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.pages.base_page_widget import BasePageWidget
from pdf_tool.gui.pages.split_page import run_split


class SplitPageWidget(BasePageWidget):
    """Split 페이지 위젯. N페이지 단위 분할 입력을 포함한다."""

    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """분할 파라미터 UI를 생성한다."""
        label = ctk.CTkLabel(parent, text="N페이지마다 분할:")
        label.pack(pady=(5, 0), padx=10, anchor="w")

        self.every_entry = ctk.CTkEntry(parent, placeholder_text="1")
        self.every_entry.pack(pady=5, padx=10, fill="x")
        self.every_entry.insert(0, "1")

    def execute_command(self, input_file: Path, output_path: Path):
        """분할을 실행한다."""
        every = int(self.every_entry.get() or "1")
        output_dir = input_file.parent
        return run_split(input_file, every, output_dir)

    def _on_success(self, result, output_path: Path) -> None:
        """분할 결과 파일 목록을 표시한다."""
        self._execution_state.finish()
        self.progress_bar.stop()
        self._update_execute_button()

        if isinstance(result, list):
            msg = f"분할 완료! {len(result)}개 파일 생성"
            self.result_display.show_success(msg, result[0].parent if result else output_path)
        else:
            self.result_display.show_success("분할 완료!", output_path)
