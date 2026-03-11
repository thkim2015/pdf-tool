"""Compress 페이지 GUI 위젯 모듈."""

from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.pages.base_page import generate_output_path
from pdf_tool.gui.pages.base_page_widget import BasePageWidget
from pdf_tool.gui.pages.compress_page import run_compress


class CompressPageWidget(BasePageWidget):
    """Compress 페이지 위젯. 추가 파라미터 없음."""

    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """파라미터 UI 없음 (압축은 별도 설정 불필요)."""
        label = ctk.CTkLabel(parent, text="PDF를 압축합니다.")
        label.pack(pady=5)

    def execute_command(self, input_file: Path, output_path: Path):
        """압축을 실행한다."""
        result = run_compress(input_file, output_path)
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
