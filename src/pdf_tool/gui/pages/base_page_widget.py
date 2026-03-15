"""BasePage GUI 위젯 모듈.

모든 작업 페이지의 공통 GUI 레이아웃과 스레드 실행 패턴을 제공한다.
3단 레이아웃: 상단 툴바 + 중앙 스크롤 컨텐츠 + 하단 액션 바.
"""

from __future__ import annotations

import threading
from abc import abstractmethod
from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.app import format_exception_message
from pdf_tool.gui.constants import (
    BORDER_RADIUS_DEFAULT,
    PADDING_MD,
)
from pdf_tool.gui.pages.base_page import (
    ExecutionState,
    generate_output_path,
    would_overwrite,
)
from pdf_tool.gui.theme import get_current_palette
from pdf_tool.gui.widgets.file_picker_widget import FilePickerWidget
from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle
from pdf_tool.gui.widgets.progress_bar_widget import ProgressBarWidget
from pdf_tool.gui.widgets.result_display_widget import ResultDisplayWidget

# ============================================================================
# 3단 레이아웃 상수
# ============================================================================

# 툴바 (상단)
TOOLBAR_HEIGHT = 52
TOOLBAR_PADX = 24

# 컨텐츠 (중앙)
CONTENT_PADX = 24
CONTENT_TOP_MARGIN = 20

# 액션 바 (하단)
ACTION_BAR_HEIGHT = 56
ACTION_BAR_PADDING = 8
ACTION_BAR_BUTTON_HEIGHT = 40
SEPARATOR_HEIGHT = 1
SEPARATOR_COLOR = "#48484A"  # systemGray3


# ============================================================================
# 스타일 함수
# ============================================================================


def get_toolbar_style() -> dict:
    """툴바 스타일 딕셔너리를 반환한다.

    Returns:
        height, title_font_size, title_weight 키를 포함하는 딕셔너리
    """
    return {
        "height": TOOLBAR_HEIGHT,
        "title_font_size": 22,
        "title_weight": "bold",
    }


def get_action_bar_style() -> dict:
    """액션 바 스타일 딕셔너리를 반환한다.

    Returns:
        height, separator_height, separator_color, button_height 키를 포함하는 딕셔너리
    """
    return {
        "height": ACTION_BAR_HEIGHT,
        "separator_height": SEPARATOR_HEIGHT,
        "separator_color": SEPARATOR_COLOR,
        "button_height": ACTION_BAR_BUTTON_HEIGHT,
    }


class BasePageWidget(ctk.CTkFrame):
    """작업 페이지의 기본 위젯 클래스.

    3단 레이아웃: 상단 툴바 -> 중앙 스크롤 컨텐츠 -> 하단 액션 바
    """

    # 서브클래스에서 오버라이드하여 툴바 제목과 액션 버튼 텍스트를 설정한다.
    page_title: str = ""
    action_button_text: str = "실행"

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self._execution_state = ExecutionState()

        self._create_layout()

    def _create_layout(self) -> None:
        """3단 레이아웃을 생성한다."""
        palette = get_current_palette()

        # ===== 상단: 툴바 (52pt) =====
        self._create_toolbar(palette)

        # ===== 중앙: 스크롤 컨텐츠 =====
        self._create_content_area(palette)

        # ===== 하단: 액션 바 =====
        self._create_action_bar(palette)

    def _create_toolbar(self, palette) -> None:
        """상단 툴바를 생성한다."""
        toolbar_style = get_toolbar_style()

        self.toolbar_frame = ctk.CTkFrame(
            self,
            height=toolbar_style["height"],
            fg_color=palette.vibrancy_bg,
            corner_radius=0,
        )
        self.toolbar_frame.pack(fill="x", side="top")
        self.toolbar_frame.pack_propagate(False)

        # 제목 레이블
        self.title_label = ctk.CTkLabel(
            self.toolbar_frame,
            text=self.page_title,
            text_color=palette.text_primary,
            font=ctk.CTkFont(
                "System",
                toolbar_style["title_font_size"],
                toolbar_style["title_weight"],
            ),
        )
        self.title_label.pack(
            side="left",
            padx=TOOLBAR_PADX,
            pady=0,
        )

    def _create_content_area(self, palette) -> None:
        """중앙 컨텐츠 영역을 생성한다."""
        # 스크롤 가능한 컨테이너
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=palette.surface,
        )
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0,
        )

        # 파일 선택 영역
        self.file_picker = FilePickerWidget(
            self.content_frame,
            on_file_selected=self._on_file_selected,
        )
        self.file_picker.pack(
            fill="x",
            padx=CONTENT_PADX,
            pady=(CONTENT_TOP_MARGIN, PADDING_MD),
        )

        # 파라미터 영역 (서브클래스에서 구현)
        self.params_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent",
        )
        self.params_frame.pack(fill="x", padx=CONTENT_PADX, pady=PADDING_MD)
        self.create_params_ui(self.params_frame)

        # 프로그레스 바
        self.progress_bar = ProgressBarWidget(self.content_frame)

        # 결과 영역
        self.result_display = ResultDisplayWidget(self.content_frame)
        self.result_display.pack(
            fill="both",
            expand=True,
            padx=CONTENT_PADX,
            pady=PADDING_MD,
        )

    def _create_action_bar(self, palette) -> None:
        """하단 액션 바를 생성한다."""
        action_style = get_action_bar_style()
        button_style = MacOSButtonStyle.get_style("primary", "large")
        hover_color = MacOSButtonStyle.get_hover_color("primary")

        # 액션 바 컨테이너
        self.action_bar_frame = ctk.CTkFrame(
            self,
            height=action_style["height"],
            fg_color=palette.surface,
            corner_radius=0,
        )
        self.action_bar_frame.pack(fill="x", side="bottom")
        self.action_bar_frame.pack_propagate(False)

        # 상단 분리선
        self.separator = ctk.CTkFrame(
            self.action_bar_frame,
            height=action_style["separator_height"],
            fg_color=action_style["separator_color"],
            corner_radius=0,
        )
        self.separator.pack(fill="x", side="top")

        # 버튼 영역 (우측 정렬)
        button_container = ctk.CTkFrame(
            self.action_bar_frame,
            fg_color="transparent",
        )
        button_container.pack(
            fill="both",
            expand=True,
            padx=CONTENT_PADX,
            pady=ACTION_BAR_PADDING,
        )

        # 실행 버튼 (우측 정렬)
        self.execute_btn = ctk.CTkButton(
            button_container,
            text=self.action_button_text,
            command=self._on_execute,
            state="disabled",
            height=action_style["button_height"],
            corner_radius=BORDER_RADIUS_DEFAULT,
            fg_color=button_style["bg_color"],
            text_color=button_style["text_color"],
            hover_color=hover_color,
        )
        self.execute_btn.pack(side="right")

    def _on_file_selected(self, path: Path) -> None:
        """파일이 선택되었을 때 호출된다."""
        self._execution_state.input_file = path
        self._update_execute_button()

    def _update_execute_button(self) -> None:
        """실행 버튼 상태를 갱신한다."""
        if self._execution_state.can_execute:
            self.execute_btn.configure(state="normal")
        else:
            self.execute_btn.configure(state="disabled")

    def _on_execute(self) -> None:
        """실행 버튼 클릭 핸들러."""
        if not self._execution_state.can_execute:
            return

        input_file = self._execution_state.input_file
        output_path = self._get_output_path()

        # 덮어쓰기 검증 (REQ-N-001)
        if would_overwrite(input_file, output_path):
            output_path = generate_output_path(input_file)

        self._execution_state.start(input_file)
        self.execute_btn.configure(state="disabled")  # REQ-S-001
        self.result_display.clear()
        self.progress_bar.start("처리 중...")

        # 데몬 스레드에서 커맨드 실행
        thread = threading.Thread(
            target=self._execute_in_thread,
            args=(input_file, output_path),
            daemon=True,
        )
        thread.start()

    def _execute_in_thread(self, input_file: Path, output_path: Path) -> None:
        """백그라운드 스레드에서 커맨드를 실행한다."""
        try:
            result = self.execute_command(input_file, output_path)
            self.after(0, lambda: self._on_success(result, output_path))
        except Exception as exc:
            self.after(0, lambda e=exc: self._on_error(e))

    def _on_success(self, result, output_path: Path) -> None:
        """메인 스레드에서 성공 결과를 처리한다."""
        self._execution_state.finish()
        self.progress_bar.stop()
        self._update_execute_button()
        self.result_display.show_success("완료!", output_path)

    def _on_error(self, exc: Exception) -> None:
        """메인 스레드에서 에러를 처리한다."""
        self._execution_state.finish()
        self.progress_bar.stop()
        self._update_execute_button()
        self.result_display.show_error(format_exception_message(exc))

    def _get_output_path(self) -> Path:
        """기본 출력 경로를 생성한다. 서브클래스에서 오버라이드 가능."""
        return generate_output_path(self._execution_state.input_file)

    @abstractmethod
    def create_params_ui(self, parent: ctk.CTkFrame) -> None:
        """파라미터 UI를 생성한다. 서브클래스에서 구현한다."""

    @abstractmethod
    def execute_command(self, input_file: Path, output_path: Path):
        """커맨드를 실행한다. 서브클래스에서 구현한다."""
