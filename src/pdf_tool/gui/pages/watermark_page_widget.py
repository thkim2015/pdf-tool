"""Watermark 페이지 GUI 위젯 모듈."""

from __future__ import annotations

import tkinter.filedialog as fd
from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.constants import (
    BORDER_RADIUS_DEFAULT,
    BUTTON_HEIGHT_DEFAULT,
    PADDING_LG,
    PADDING_MD,
)
from pdf_tool.gui.theme import get_current_palette

from pdf_tool.gui.pages.base_page_widget import BasePageWidget
from pdf_tool.gui.pages.watermark_page import run_watermark
from pdf_tool.gui.widgets.page_range_input_widget import PageRangeInputWidget


class WatermarkPageWidget(BasePageWidget):
    """Watermark 페이지 위젯.

    텍스트/이미지 전환, 투명도, 회전, 위치, 페이지 범위를 포함한다.
    """

    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """워터마크 파라미터 UI를 생성한다."""
        # 타입 선택 (텍스트 / 이미지)
        type_label = ctk.CTkLabel(parent, text="워터마크 유형:")
        type_label.pack(pady=(5, 0), padx=10, anchor="w")

        self.type_var = ctk.StringVar(value="text")
        type_frame = ctk.CTkFrame(parent)
        type_frame.pack(fill="x", padx=10, pady=5)

        self.text_radio = ctk.CTkRadioButton(
            type_frame, text="텍스트", variable=self.type_var,
            value="text", command=self._on_type_changed,
        )
        self.text_radio.pack(side="left", padx=10)

        self.image_radio = ctk.CTkRadioButton(
            type_frame, text="이미지", variable=self.type_var,
            value="image", command=self._on_type_changed,
        )
        self.image_radio.pack(side="left", padx=10)

        # 텍스트 입력
        self.text_frame = ctk.CTkFrame(parent)
        self.text_frame.pack(fill="x", padx=10, pady=5)
        text_label = ctk.CTkLabel(self.text_frame, text="텍스트:")
        text_label.pack(pady=(5, 0), padx=10, anchor="w")
        self.text_entry = ctk.CTkEntry(
            self.text_frame, placeholder_text="워터마크 텍스트 입력",
        )
        self.text_entry.pack(pady=5, padx=10, fill="x")

        # 이미지 선택 (초기에는 숨김)
        self.image_frame = ctk.CTkFrame(parent)
        image_label = ctk.CTkLabel(self.image_frame, text="이미지 파일:")
        image_label.pack(pady=(5, 0), padx=10, anchor="w")
        self._image_path: Path | None = None
        self.image_btn = ctk.CTkButton(
            self.image_frame,
            text="이미지 선택...",
            command=self._select_image,
        )
        self.image_btn.pack(pady=5, padx=10, fill="x")
        self.image_label = ctk.CTkLabel(self.image_frame, text="", text_color="gray")
        self.image_label.pack(padx=10)

        # 투명도 슬라이더
        opacity_label = ctk.CTkLabel(parent, text="투명도:")
        opacity_label.pack(pady=(5, 0), padx=10, anchor="w")
        self.opacity_var = ctk.DoubleVar(value=0.3)
        self.opacity_slider = ctk.CTkSlider(
            parent, from_=0.0, to=1.0, variable=self.opacity_var,
        )
        self.opacity_slider.pack(pady=5, padx=10, fill="x")

        # 회전 슬라이더
        rotation_label = ctk.CTkLabel(parent, text="회전 (도):")
        rotation_label.pack(pady=(5, 0), padx=10, anchor="w")
        self.rotation_var = ctk.DoubleVar(value=45.0)
        self.rotation_slider = ctk.CTkSlider(
            parent, from_=0.0, to=360.0, variable=self.rotation_var,
        )
        self.rotation_slider.pack(pady=5, padx=10, fill="x")

        # 위치 선택
        position_label = ctk.CTkLabel(parent, text="위치:")
        position_label.pack(pady=(5, 0), padx=10, anchor="w")
        self.position_var = ctk.StringVar(value="center")
        self.position_menu = ctk.CTkOptionMenu(
            parent,
            values=["center", "top-left", "top-right", "bottom-left", "bottom-right"],
            variable=self.position_var,
        )
        self.position_menu.pack(pady=5, padx=10, fill="x")

        # 선택적 페이지 범위
        self.page_range_input = PageRangeInputWidget(
            parent,
            label_text="페이지 범위 (선택):",
            placeholder="비워두면 전체 페이지",
        )
        self.page_range_input.pack(fill="x")

    def _on_type_changed(self) -> None:
        """워터마크 유형 변경 핸들러."""
        if self.type_var.get() == "text":
            self.text_frame.pack(fill="x", padx=10, pady=5)
            self.image_frame.pack_forget()
        else:
            self.text_frame.pack_forget()
            self.image_frame.pack(fill="x", padx=10, pady=5)

    def _select_image(self) -> None:
        """이미지 파일 선택 다이얼로그."""
        file_path = fd.askopenfilename(
            filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.bmp")],
        )
        if file_path:
            self._image_path = Path(file_path)
            self.image_label.configure(text=self._image_path.name)

    def execute_command(self, input_file: Path, output_path: Path):
        """워터마크를 적용한다."""
        wm_type = self.type_var.get()
        text = self.text_entry.get() if wm_type == "text" else None
        image = self._image_path if wm_type == "image" else None
        pages = self.page_range_input.get_value() or None

        return run_watermark(
            input_path=input_file,
            output_path=output_path,
            text=text,
            image=image,
            opacity=self.opacity_var.get(),
            rotation=self.rotation_var.get(),
            position=self.position_var.get(),
            pages=pages,
        )
