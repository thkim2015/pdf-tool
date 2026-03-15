"""이미지->PDF 변환 페이지 GUI 위젯 모듈."""

from __future__ import annotations

import tkinter.filedialog as fd
from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.constants import (
    BORDER_RADIUS_DEFAULT,
    BUTTON_HEIGHT_DEFAULT,
    FONT_LABEL,
    INPUT_HEIGHT_DEFAULT,
    PADDING_MD,
    PADDING_SM,
    RADIOBUTTON_PADX,
    RADIOBUTTON_PADY,
    SECTION_LABEL_PADDING,
    SECTION_SPACING,
)
from pdf_tool.gui.pages.base_page_widget import BasePageWidget
from pdf_tool.gui.pages.image_to_pdf_page import run_image_to_pdf
from pdf_tool.gui.theme import get_current_palette


class ImageListFrame(ctk.CTkFrame):
    """이미지 파일 목록을 관리하는 프레임."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        palette = get_current_palette()
        self.image_paths: list[Path] = []

        # 헤더
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, PADDING_SM))

        ctk.CTkLabel(
            header_frame,
            text="파일명",
            text_color=palette.text_tertiary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1] - 1, "bold"),
        ).pack(side="left", padx=PADDING_MD, fill="x", expand=True)

        ctk.CTkLabel(
            header_frame,
            text="작업",
            text_color=palette.text_tertiary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1] - 1, "bold"),
            width=100,
        ).pack(side="right", padx=PADDING_SM)

        # 스크롤 가능한 리스트 영역
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # 파일 항목 저장용
        self._file_items: list[ctk.CTkFrame] = []

    def add_image(self, path: Path) -> None:
        """이미지를 목록에 추가한다."""
        if path not in self.image_paths:
            self.image_paths.append(path)
            self._refresh_list()

    def add_images(self, paths: list[Path]) -> None:
        """여러 이미지를 목록에 추가한다."""
        for path in paths:
            if path not in self.image_paths:
                self.image_paths.append(path)
        self._refresh_list()

    def remove_image(self, path: Path) -> None:
        """이미지를 목록에서 제거한다."""
        if path in self.image_paths:
            self.image_paths.remove(path)
            self._refresh_list()

    def move_up(self, path: Path) -> None:
        """이미지를 위로 이동한다."""
        if path in self.image_paths:
            idx = self.image_paths.index(path)
            if idx > 0:
                self.image_paths[idx], self.image_paths[idx - 1] = (
                    self.image_paths[idx - 1],
                    self.image_paths[idx],
                )
                self._refresh_list()

    def move_down(self, path: Path) -> None:
        """이미지를 아래로 이동한다."""
        if path in self.image_paths:
            idx = self.image_paths.index(path)
            if idx < len(self.image_paths) - 1:
                self.image_paths[idx], self.image_paths[idx + 1] = (
                    self.image_paths[idx + 1],
                    self.image_paths[idx],
                )
                self._refresh_list()

    def clear(self) -> None:
        """목록을 모두 지운다."""
        self.image_paths.clear()
        self._refresh_list()

    def get_images(self) -> list[Path]:
        """현재 이미지 목록을 반환한다."""
        return self.image_paths.copy()

    def _refresh_list(self) -> None:
        """목록을 다시 그린다."""
        palette = get_current_palette()

        # 기존 항목 제거
        for item in self._file_items:
            item.destroy()
        self._file_items.clear()

        # 새 항목 추가
        for path in self.image_paths:
            item_frame = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color=palette.surface_elevated,
                corner_radius=BORDER_RADIUS_DEFAULT,
            )
            item_frame.pack(fill="x", padx=0, pady=PADDING_SM)

            # 파일명
            ctk.CTkLabel(
                item_frame,
                text=path.name,
                text_color=palette.text_primary,
            ).pack(side="left", padx=PADDING_MD, pady=PADDING_SM, fill="x", expand=True)

            # 버튼 영역
            button_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            button_frame.pack(side="right", padx=PADDING_SM, pady=PADDING_SM)

            # 위로 이동 버튼
            if self.image_paths.index(path) > 0:
                up_btn = ctk.CTkButton(
                    button_frame,
                    text="^",
                    width=32,
                    height=BUTTON_HEIGHT_DEFAULT,
                    command=lambda p=path: self.move_up(p),
                )
                up_btn.pack(side="left", padx=PADDING_SM)

            # 아래로 이동 버튼
            if self.image_paths.index(path) < len(self.image_paths) - 1:
                down_btn = ctk.CTkButton(
                    button_frame,
                    text="v",
                    width=32,
                    height=BUTTON_HEIGHT_DEFAULT,
                    command=lambda p=path: self.move_down(p),
                )
                down_btn.pack(side="left", padx=PADDING_SM)

            # 제거 버튼
            remove_btn = ctk.CTkButton(
                button_frame,
                text="X",
                width=32,
                height=BUTTON_HEIGHT_DEFAULT,
                fg_color="#E84C3D",
                hover_color="#C73629",
                command=lambda p=path: self.remove_image(p),
            )
            remove_btn.pack(side="left", padx=PADDING_SM)

            self._file_items.append(item_frame)


class ImageToPdfPageWidget(BasePageWidget):
    """이미지->PDF 변환 페이지 위젯.

    여러 이미지 파일을 드래그드롭 또는 파일 선택으로 추가하고,
    순서를 정렬한 후 PDF로 변환한다.
    """

    page_title = "이미지 -> PDF"
    action_button_text = "변환"

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        self._image_paths: list[Path] = []
        super().__init__(master, **kwargs)

        # FilePickerWidget 숨김 (이미지 리스트 사용하므로 불필요)
        self.file_picker.pack_forget()

    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """이미지 변환 파라미터 UI를 생성한다."""
        palette = get_current_palette()

        # ===== Section 1: 이미지 파일 선택 =====
        file_label = ctk.CTkLabel(
            parent,
            text="이미지 파일 선택:",
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        file_label.pack(pady=SECTION_LABEL_PADDING, padx=PADDING_MD, anchor="w")

        # 파일 추가 버튼 및 설명
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", padx=PADDING_MD, pady=(0, PADDING_SM))

        self.add_files_btn = ctk.CTkButton(
            button_frame,
            text="이미지 추가...",
            command=self._select_images,
            height=BUTTON_HEIGHT_DEFAULT,
        )
        self.add_files_btn.pack(side="left", fill="x", expand=True, padx=(0, PADDING_SM))

        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="모두 제거",
            command=self._clear_images,
            height=BUTTON_HEIGHT_DEFAULT,
            fg_color=palette.surface_elevated,
            text_color=palette.text_primary,
        )
        self.clear_btn.pack(side="left", fill="x", expand=True)

        # 이미지 목록
        self.image_list = ImageListFrame(
            parent,
            fg_color=palette.surface,
            corner_radius=BORDER_RADIUS_DEFAULT,
        )
        self.image_list.pack(fill="both", expand=True, padx=PADDING_MD, pady=(0, SECTION_SPACING))

        # ===== Section 2: 페이지 크기 설정 =====
        page_size_label = ctk.CTkLabel(
            parent,
            text="페이지 크기:",
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1], FONT_LABEL[2]),
        )
        page_size_label.pack(pady=SECTION_LABEL_PADDING, padx=PADDING_MD, anchor="w")

        self.page_size_var = ctk.StringVar(value="A4")
        page_size_frame = ctk.CTkFrame(parent, fg_color="transparent")
        page_size_frame.pack(fill="x", padx=PADDING_MD, pady=(0, SECTION_SPACING))

        for size in ["A4", "Letter", "Custom"]:
            radio = ctk.CTkRadioButton(
                page_size_frame,
                text=size,
                variable=self.page_size_var,
                value=size,
                command=self._on_page_size_changed,
            )
            radio.pack(side="left", padx=RADIOBUTTON_PADX, pady=RADIOBUTTON_PADY)

        # Custom 크기 입력 (초기에는 숨김)
        self.custom_size_frame = ctk.CTkFrame(parent, fg_color="transparent")

        custom_label = ctk.CTkLabel(
            self.custom_size_frame,
            text="커스텀 크기 (너비 x 높이, mm):",
            text_color=palette.text_primary,
            font=ctk.CTkFont(FONT_LABEL[0], FONT_LABEL[1] - 1),
        )
        custom_label.pack(pady=SECTION_LABEL_PADDING, anchor="w")

        size_input_frame = ctk.CTkFrame(self.custom_size_frame, fg_color="transparent")
        size_input_frame.pack(fill="x", padx=0, pady=(0, SECTION_SPACING))

        self.custom_width = ctk.CTkEntry(
            size_input_frame,
            placeholder_text="너비",
            height=INPUT_HEIGHT_DEFAULT,
            width=100,
        )
        self.custom_width.pack(side="left", padx=(0, PADDING_SM))

        ctk.CTkLabel(
            size_input_frame,
            text="x",
            text_color=palette.text_primary,
        ).pack(side="left", padx=PADDING_SM)

        self.custom_height = ctk.CTkEntry(
            size_input_frame,
            placeholder_text="높이",
            height=INPUT_HEIGHT_DEFAULT,
            width=100,
        )
        self.custom_height.pack(side="left", padx=(PADDING_SM, 0))

        # ===== Section 3: 옵션 =====
        self.aspect_ratio_var = ctk.BooleanVar(value=True)
        aspect_ratio_check = ctk.CTkCheckBox(
            parent,
            text="종횡비 유지",
            variable=self.aspect_ratio_var,
        )
        aspect_ratio_check.pack(pady=PADDING_SM, padx=PADDING_MD, anchor="w")

    def _select_images(self) -> None:
        """이미지 파일 선택 다이얼로그."""
        file_paths = fd.askopenfilenames(
            filetypes=[
                ("이미지 파일", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif"),
                ("모든 파일", "*.*"),
            ],
        )
        if file_paths:
            self.image_list.add_images([Path(p) for p in file_paths])
            self._update_execute_button()

    def _clear_images(self) -> None:
        """이미지 목록을 모두 지운다."""
        self.image_list.clear()
        self._update_execute_button()

    def _on_page_size_changed(self) -> None:
        """페이지 크기 변경 시 호출된다."""
        if self.page_size_var.get() == "Custom":
            self.custom_size_frame.pack(fill="x", padx=PADDING_MD, pady=(0, SECTION_SPACING))
        else:
            self.custom_size_frame.pack_forget()

    def _update_execute_button(self) -> None:
        """실행 버튼 상태를 갱신한다.

        이미지가 선택되었을 때만 실행 가능하도록 설정한다.
        """
        can_execute = len(self.image_list.get_images()) > 0
        self.execute_btn.configure(
            state="normal" if can_execute else "disabled"
        )

    def _on_execute(self) -> None:
        """실행 버튼 클릭 핸들러. BasePageWidget 오버라이드."""
        import threading

        images = self.image_list.get_images()
        if not images:
            return

        output_path = self._get_output_path()

        # 실행 상태 업데이트
        self._execution_state.input_file = images[0]  # 첫 번째 이미지를 기준으로
        self._execution_state.start(images[0])
        self.execute_btn.configure(state="disabled")
        self.result_display.clear()
        self.progress_bar.start("처리 중...")

        # 데몬 스레드에서 커맨드 실행
        thread = threading.Thread(
            target=self._execute_in_thread,
            args=(images[0], output_path),
            daemon=True,
        )
        thread.start()

    def execute_command(self, input_file: Path, output_path: Path):
        """이미지를 PDF로 변환한다.

        Note: input_file 파라미터는 BasePageWidget 호환성을 위해 받지만,
              실제로는 self.image_list의 이미지들을 변환한다.
        """
        images = self.image_list.get_images()
        if not images:
            raise ValueError("변환할 이미지가 없습니다")

        result = run_image_to_pdf(
            image_paths=images,
            output_path=output_path,
            keep_aspect_ratio=self.aspect_ratio_var.get(),
        )
        return result

    def _get_output_path(self) -> Path:
        """기본 출력 경로를 생성한다."""
        # 첫 번째 이미지를 기준으로 경로 생성
        images = self.image_list.get_images()
        if images:
            first_image = images[0]
            # 이미지 파일명 -> PDF 파일명으로 변환
            pdf_name = first_image.stem + ".pdf"
            return first_image.parent / pdf_name
        # 이미지가 없으면 기본 경로
        return Path.home() / "images.pdf"
