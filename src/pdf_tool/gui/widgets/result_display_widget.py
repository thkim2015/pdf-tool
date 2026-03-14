"""결과 표시 GUI 위젯 모듈.

작업 결과(성공, 에러, 정보)를 GUI로 표시하는 위젯이다.
PDF 결과물의 첫 페이지 미리보기 기능을 포함한다.
"""

from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import Any

import customtkinter as ctk

from pdf_tool.gui.constants import FONT_LABEL, FONT_SMALL, PADDING_MD
from pdf_tool.gui.theme import get_current_palette
from pdf_tool.gui.widgets.result_display import ResultState

try:
    from pdf_tool.gui.widgets.pdf_preview import (
        is_preview_available,
        render_first_page,
    )
    from pdf_tool.gui.widgets.pdf_preview_widget import PdfPreviewWidget

    _preview_enabled = True
except ImportError:
    _preview_enabled = False

logger = logging.getLogger(__name__)


class ResultDisplayWidget(ctk.CTkFrame):
    """결과 표시 위젯.

    성공(초록), 에러(빨강), 정보(키-값) 결과를 표시한다.
    PDF 결과물이면 첫 페이지 미리보기 썸네일을 표시한다.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        palette = get_current_palette()
        self._state = ResultState()

        # 결과 메시지 레이블
        self.message_label = ctk.CTkLabel(
            self,
            text="",
            wraplength=500,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        self.message_label.pack(pady=PADDING_MD, padx=PADDING_MD, fill="x")

        # 경로 레이블 (성공 시 출력 경로 표시)
        self.path_label = ctk.CTkLabel(
            self,
            text="",
            text_color=palette.text_tertiary,
            font=ctk.CTkFont(FONT_SMALL[0], FONT_SMALL[1], FONT_SMALL[2]),
        )
        self.path_label.pack(pady=PADDING_MD, padx=PADDING_MD, fill="x")

        # 정보 표시 프레임 (dict 결과용)
        self.info_frame = ctk.CTkFrame(self)
        self._info_labels: list[ctk.CTkLabel] = []

        # PDF 미리보기 위젯
        if _preview_enabled:
            self._preview_widget = PdfPreviewWidget(self)
        else:
            self._preview_widget = None

    def show_success(self, message: str, output_path: Path) -> None:
        """성공 결과를 표시한다.

        output_path가 PDF이면 미리보기 썸네일도 표시한다.
        """
        palette = get_current_palette()
        self._state.show_success(message, output_path)
        self._clear_info()
        self.message_label.configure(
            text=f"✓ {message}",
            text_color=palette.success,
        )
        self.path_label.configure(text=str(output_path))
        self.info_frame.pack_forget()
        self._start_preview(output_path)

    def show_error(self, message: str) -> None:
        """에러 결과를 표시한다."""
        palette = get_current_palette()
        self._state.show_error(message)
        self._clear_info()
        self.message_label.configure(
            text=f"✗ {message}",
            text_color=palette.error,
        )
        self.path_label.configure(text="")
        self.info_frame.pack_forget()
        self._clear_preview()

    def show_info(self, data: dict[str, Any]) -> None:
        """정보(dict)를 키-값 테이블로 표시한다."""
        palette = get_current_palette()
        self._state.show_info(data)
        self.message_label.configure(text="", text_color="gray")
        self.path_label.configure(text="")
        self._clear_info()
        self._clear_preview()

        self.info_frame.pack(pady=PADDING_MD, padx=PADDING_MD, fill="both", expand=True)
        for key, value in data.items():
            label = ctk.CTkLabel(
                self.info_frame,
                text=f"{key}: {value}",
                anchor="w",
                text_color=palette.text_secondary,
                font=ctk.CTkFont(FONT_SMALL[0], FONT_SMALL[1], FONT_SMALL[2]),
            )
            label.pack(padx=PADDING_MD, pady=PADDING_MD, fill="x")
            self._info_labels.append(label)

    def clear(self) -> None:
        """결과를 초기화한다."""
        self._state.clear()
        self.message_label.configure(text="", text_color="gray")
        self.path_label.configure(text="")
        self._clear_info()
        self.info_frame.pack_forget()
        self._clear_preview()

    def _clear_info(self) -> None:
        """정보 레이블을 제거한다."""
        for label in self._info_labels:
            label.destroy()
        self._info_labels.clear()

    def _start_preview(self, output_path: Path) -> None:
        """PDF 미리보기 렌더링을 백그라운드 스레드로 시작한다."""
        if self._preview_widget is None:
            return
        if not is_preview_available():
            return
        if not str(output_path).lower().endswith(".pdf"):
            return

        self._preview_widget.pack(pady=PADDING_MD, padx=PADDING_MD, fill="x")
        self._preview_widget.show_loading()
        render_id = self._preview_widget.next_render_id()

        thread = threading.Thread(
            target=self._render_preview,
            args=(output_path, render_id),
            daemon=True,
        )
        thread.start()

    def _render_preview(
        self,
        output_path: Path,
        render_id: int,
    ) -> None:
        """백그라운드 스레드에서 PDF 첫 페이지를 렌더링한다.

        렌더링 완료 후 GUI 스레드에서 위젯을 업데이트한다.
        render_id가 현재와 다르면 (새 요청이 들어왔으면) 무시한다.
        """
        try:
            pil_image = render_first_page(str(output_path))
        except Exception:
            logger.warning(
                "PDF 미리보기 렌더링 실패: %s",
                output_path,
                exc_info=True,
            )
            if self._preview_widget.render_id == render_id:
                self.after(0, self._preview_widget.show_fallback)
            return

        if self._preview_widget.render_id == render_id:
            self.after(
                0,
                lambda: self._preview_widget.show_preview(
                    pil_image, output_path
                ),
            )

    def _clear_preview(self) -> None:
        """미리보기 위젯을 초기화하고 숨긴다."""
        if self._preview_widget is not None:
            self._preview_widget.clear()
            self._preview_widget.pack_forget()
