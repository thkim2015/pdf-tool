"""Compress 페이지 GUI 위젯 모듈."""

from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from pdf_tool.core.progress import ProgressCallback
from pdf_tool.gui.constants import FONT_SMALL, PADDING_MD
from pdf_tool.gui.pages.base_page_widget import BasePageWidget
from pdf_tool.gui.pages.compress_page import run_compress
from pdf_tool.gui.theme import get_current_palette


class CompressPageWidget(BasePageWidget):
    """Compress 페이지 위젯. 추가 파라미터 없음."""

    page_title = "압축"
    action_button_text = "압축"

    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """파라미터 UI 없음 (압축은 별도 설정 불필요)."""
        palette = get_current_palette()
        label = ctk.CTkLabel(
            parent,
            text="PDF를 압축합니다. (크기 감소, 품질 유지)",
            text_color=palette.text_secondary,
            font=ctk.CTkFont(FONT_SMALL[0], FONT_SMALL[1], FONT_SMALL[2]),
        )
        label.pack(pady=PADDING_MD)

    def execute_command(
        self, input_file: Path, output_path: Path, callback: ProgressCallback = None,
    ):
        """압축을 실행한다."""
        result = run_compress(input_file, output_path, callback=callback)
        return result

    def _on_success(self, result, output_path: Path) -> None:
        """압축 결과 통계를 표시한다."""
        self._execution_state.finish()
        self.progress_bar.stop()
        self._update_execute_button()

        if isinstance(result, dict):
            msg = (
                f"압축 완료! "
                f"원본: {result.get('original_size', 0):,} bytes -> "
                f"압축: {result.get('compressed_size', 0):,} bytes "
                f"({result.get('reduction_percent', 0):.1f}% 감소)"
            )
            actual_path = result.get("output_path", output_path)
            self.result_display.show_success(msg, actual_path)
        else:
            self.result_display.show_success("압축 완료!", output_path)
