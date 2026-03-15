"""PDF 미리보기 GUI 위젯 모듈.

결과 PDF의 첫 번째 페이지를 썸네일로 표시한다.
Quick Look 스타일 (둥근 모서리, 그림자) 적용.
"""

from __future__ import annotations

import contextlib
from pathlib import Path

import customtkinter as ctk
from PIL import Image

from pdf_tool.gui.constants import FONT_SMALL, PADDING_MD
from pdf_tool.gui.theme import get_current_palette

try:
    from pdf_tool.gui.widgets.pdf_preview import open_pdf_in_viewer

    _preview_module_available = True
except ImportError:
    _preview_module_available = False


# ============================================================================
# Quick Look 스타일 상수
# ============================================================================

QUICK_LOOK_CORNER_RADIUS = 8


def get_quick_look_style() -> dict:
    """Quick Look 스타일 딕셔너리를 반환한다.

    Returns:
        corner_radius, shadow 키를 포함하는 딕셔너리
    """
    return {
        "corner_radius": QUICK_LOOK_CORNER_RADIUS,
        "shadow": "light",
    }


class PdfPreviewWidget(ctk.CTkFrame):
    """PDF 첫 페이지 미리보기 위젯.

    썸네일 이미지를 표시하고 클릭 시 시스템 뷰어로 PDF를 연다.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        # Quick Look 스타일 적용
        quick_look = get_quick_look_style()
        kwargs.setdefault("corner_radius", quick_look["corner_radius"])
        super().__init__(master, **kwargs)

        palette = get_current_palette()
        self._render_id: int = 0
        self._ctk_image: ctk.CTkImage | None = None
        self._pdf_path: str | Path | None = None

        # 로딩 텍스트 레이블
        self._loading_label = ctk.CTkLabel(
            self,
            text="",
            text_color=palette.text_tertiary,
            font=ctk.CTkFont(FONT_SMALL[0], FONT_SMALL[1], FONT_SMALL[2]),
        )

        # 이미지 표시 레이블
        self._image_label = ctk.CTkLabel(self, text="")

    def show_loading(self) -> None:
        """'미리보기 로딩 중...' 텍스트를 표시한다."""
        self._loading_label.configure(text="⏳ 미리보기 로딩 중...")
        self._loading_label.pack(pady=PADDING_MD)
        self._image_label.pack_forget()

    def show_preview(
        self,
        pil_image: Image.Image,
        pdf_path: str | Path,
    ) -> None:
        """썸네일 이미지를 표시한다.

        Args:
            pil_image: 렌더링된 PIL Image.
            pdf_path: 클릭 시 열 PDF 경로.
        """
        self._pdf_path = pdf_path
        self._loading_label.pack_forget()

        # CTkImage 생성 (light/dark 모드 모두 동일 이미지)
        self._ctk_image = ctk.CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=(pil_image.width, pil_image.height),
        )

        self._image_label.configure(image=self._ctk_image, text="")
        self._image_label.pack(pady=PADDING_MD)

        # 클릭 시 시스템 뷰어로 열기
        if _preview_module_available:
            self._image_label.bind(
                "<Button-1>",
                lambda _e: open_pdf_in_viewer(self._pdf_path),
            )
            # 커서를 손 모양으로 변경
            self._image_label.configure(cursor="hand2")

    def show_fallback(self) -> None:
        """미리보기 불가 시 아무것도 표시하지 않는다 (graceful fallback)."""
        self._loading_label.pack_forget()
        self._image_label.pack_forget()

    def clear(self) -> None:
        """위젯을 초기 상태로 리셋한다."""
        self._render_id += 1
        self._loading_label.configure(text="")
        self._loading_label.pack_forget()
        # CTkImage 해제 전에 내부 tkinter Label의 이미지 참조를 제거한다.
        # CTkLabel.configure(image=None)은 내부 Label의 참조를 제거하지 않으므로
        # 직접 내부 _label 위젯의 이미지를 빈 문자열로 설정한다.
        if self._ctk_image is not None:
            with contextlib.suppress(AttributeError, Exception):
                self._image_label._label.configure(image="")
        self._image_label.pack_forget()
        self._ctk_image = None
        self._pdf_path = None

    @property
    def render_id(self) -> int:
        """현재 렌더 ID (경합 조건 방지용)."""
        return self._render_id

    def next_render_id(self) -> int:
        """새 렌더 ID를 발급한다."""
        self._render_id += 1
        return self._render_id
