"""Watermark 페이지 GUI 위젯 모듈."""

from __future__ import annotations

import tkinter.filedialog as fd
from pathlib import Path

import customtkinter as ctk

from pdf_tool.core.progress import ProgressCallback
from pdf_tool.gui.constants import (
    BUTTON_HEIGHT_DEFAULT,
    FONT_LABEL,
    INPUT_HEIGHT_DEFAULT,
    OPTIONMENU_HEIGHT_DEFAULT,
    PADDING_MD,
    RADIOBUTTON_PADX,
    RADIOBUTTON_PADY,
    SECTION_LABEL_PADDING,
    SECTION_SPACING,
)
from pdf_tool.gui.pages.base_page_widget import BasePageWidget
from pdf_tool.gui.pages.watermark_page import run_watermark
from pdf_tool.gui.theme import get_current_palette
from pdf_tool.gui.widgets.page_range_input_widget import PageRangeInputWidget


class WatermarkPageWidget(BasePageWidget):
    """Watermark 페이지 위젯.

    텍스트/이미지 전환, 투명도, 회전, 위치, 페이지 범위를 포함한다.
    """

    page_title = "워터마크"
    action_button_text = "추가"

    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """워터마크 파라미터 UI를 생성한다."""
        palette = get_current_palette()

        # ===== Section 1: 워터마크 유형 선택 =====
        type_label = ctk.CTkLabel(
            parent,
            text="워터마크 유형:",
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        type_label.pack(pady=SECTION_LABEL_PADDING, padx=PADDING_MD, anchor="w")

        self.type_var = ctk.StringVar(value="text")
        type_frame = ctk.CTkFrame(parent, fg_color="transparent")
        type_frame.pack(fill="x", padx=PADDING_MD, pady=(0, SECTION_SPACING))

        self.text_radio = ctk.CTkRadioButton(
            type_frame,
            text="텍스트",
            variable=self.type_var,
            value="text",
            command=self._on_type_changed,
        )
        self.text_radio.pack(side="left", padx=RADIOBUTTON_PADX, pady=RADIOBUTTON_PADY)

        self.image_radio = ctk.CTkRadioButton(
            type_frame,
            text="이미지",
            variable=self.type_var,
            value="image",
            command=self._on_type_changed,
        )
        self.image_radio.pack(side="left", padx=RADIOBUTTON_PADX, pady=RADIOBUTTON_PADY)

        # ===== Section 2: 콘텐츠 입력 (텍스트/이미지) =====
        # 텍스트 입력
        self.text_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.text_frame.pack(fill="x", padx=PADDING_MD, pady=(0, SECTION_SPACING))

        text_label = ctk.CTkLabel(
            self.text_frame,
            text="텍스트:",
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        text_label.pack(pady=SECTION_LABEL_PADDING, anchor="w")

        self.text_entry = ctk.CTkEntry(
            self.text_frame,
            placeholder_text="워터마크 텍스트 입력",
            height=INPUT_HEIGHT_DEFAULT,
            fg_color=palette.surface_elevated,
            text_color=palette.text_primary,
            placeholder_text_color=palette.text_tertiary,
        )
        self.text_entry.pack(pady=SECTION_LABEL_PADDING, fill="x")

        # 이미지 선택 (초기에는 숨김)
        self.image_frame = ctk.CTkFrame(parent, fg_color="transparent")

        image_label = ctk.CTkLabel(
            self.image_frame,
            text="이미지 파일:",
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        image_label.pack(pady=SECTION_LABEL_PADDING, anchor="w")

        self._image_path: Path | None = None
        self.image_btn = ctk.CTkButton(
            self.image_frame,
            text="이미지 선택...",
            command=self._select_image,
            height=BUTTON_HEIGHT_DEFAULT,
        )
        self.image_btn.pack(pady=SECTION_LABEL_PADDING, fill="x")

        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="",
            text_color=palette.text_tertiary,
        )
        self.image_label.pack(padx=PADDING_MD, pady=SECTION_LABEL_PADDING)

        # ===== Section 3: 외관 설정 =====
        # 투명도 슬라이더
        opacity_label = ctk.CTkLabel(
            parent,
            text="투명도:",
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        opacity_label.pack(pady=SECTION_LABEL_PADDING, padx=PADDING_MD, anchor="w")

        self.opacity_var = ctk.DoubleVar(value=0.3)
        self.opacity_slider = ctk.CTkSlider(
            parent,
            from_=0.0,
            to=1.0,
            variable=self.opacity_var,
        )
        self.opacity_slider.pack(pady=(0, SECTION_SPACING), padx=PADDING_MD, fill="x")

        # 회전 슬라이더
        rotation_label = ctk.CTkLabel(
            parent,
            text="회전 (도):",
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        rotation_label.pack(pady=SECTION_LABEL_PADDING, padx=PADDING_MD, anchor="w")

        self.rotation_var = ctk.DoubleVar(value=45.0)
        self.rotation_slider = ctk.CTkSlider(
            parent,
            from_=0.0,
            to=360.0,
            variable=self.rotation_var,
        )
        self.rotation_slider.pack(pady=(0, SECTION_SPACING), padx=PADDING_MD, fill="x")

        # ===== Section 4: 배치 설정 =====
        # 위치 선택
        position_label = ctk.CTkLabel(
            parent,
            text="위치:",
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        position_label.pack(pady=SECTION_LABEL_PADDING, padx=PADDING_MD, anchor="w")

        self.position_var = ctk.StringVar(value="center")
        self.position_menu = ctk.CTkOptionMenu(
            parent,
            values=["center", "top-left", "top-right", "bottom-left", "bottom-right"],
            variable=self.position_var,
            height=OPTIONMENU_HEIGHT_DEFAULT,
        )
        self.position_menu.pack(pady=(0, SECTION_SPACING), padx=PADDING_MD, fill="x")

        # ===== Section 5: 페이지 범위 =====
        self.page_range_input = PageRangeInputWidget(
            parent,
            label_text="페이지 범위 (선택):",
            placeholder="비워두면 전체 페이지",
        )
        self.page_range_input.pack(fill="x", padx=PADDING_MD, pady=(0, SECTION_SPACING))

    def _on_type_changed(self) -> None:
        """워터마크 유형 변경 핸들러."""
        if self.type_var.get() == "text":
            self.text_frame.pack(fill="x", padx=PADDING_MD, pady=(0, SECTION_SPACING))
            self.image_frame.pack_forget()
        else:
            self.text_frame.pack_forget()
            self.image_frame.pack(fill="x", padx=PADDING_MD, pady=(0, SECTION_SPACING))

    def _select_image(self) -> None:
        """이미지 파일 선택 다이얼로그."""
        file_path = fd.askopenfilename(
            filetypes=[("이미지 파일", "*.png *.jpg *.jpeg *.bmp")],
        )
        if file_path:
            self._image_path = Path(file_path)
            self.image_label.configure(text=self._image_path.name)

    def execute_command(
        self, input_file: Path, output_path: Path, callback: ProgressCallback = None,
    ):
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
            callback=callback,
        )
