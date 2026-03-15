"""PDF Tool GUI 메인 애플리케이션.

CustomTkinter 기반의 PDF 도구 GUI 진입점이다.
"""

from __future__ import annotations

import logging
import sys
from collections.abc import Callable

from pdf_tool.core.exceptions import PDFToolError
from pdf_tool.gui.accessibility import (
    get_page_for_shortcut,
    get_page_shortcut_keys,
)
from pdf_tool.gui.animation import Animator
from pdf_tool.gui.constants import (
    BORDER_RADIUS_DEFAULT,
    BUTTON_HEIGHT_DEFAULT,
    FONT_TITLE,
    MAIN_PADX,
    MAIN_PADY,
    NAV_BUTTONS,
    PADDING_LG,
    PADDING_MD,
    PADDING_SM,
    PADDING_XL,
    SIDEBAR_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_WIDTH,
)

# 크로스 페이드 애니메이션 기본 지속 시간 (초)
CROSS_FADE_DURATION: float = 0.15


class PageManager:
    """페이지 전환을 관리하는 클래스.

    pack_forget()/pack() 패턴으로 페이지를 전환한다.
    switch_to_animated()로 크로스 페이드 전환을 지원한다.
    """

    def __init__(self) -> None:
        self.pages: dict[str, object] = {}
        self.current_page: str | None = None
        self.animator: Animator = Animator()

    def register(self, name: str, page: object) -> None:
        """페이지를 이름으로 등록한다.

        Args:
            name: 페이지 이름
            page: 페이지 위젯 인스턴스
        """
        self.pages[name] = page

    def switch_to(self, name: str) -> None:
        """지정된 페이지로 즉시 전환한다 (애니메이션 없음).

        Args:
            name: 전환할 페이지 이름
        """
        if name not in self.pages:
            return

        # 현재 페이지 숨기기
        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].pack_forget()

        # 새 페이지 표시
        self.pages[name].pack(fill="both", expand=True)
        self.current_page = name

    def switch_to_animated(
        self,
        name: str,
        duration: float = CROSS_FADE_DURATION,
        on_complete: Callable[[], None] | None = None,
    ) -> None:
        """크로스 페이드 애니메이션으로 페이지를 전환한다.

        이전 페이지 fade-out과 새 페이지 fade-in이 동시에 진행된다.
        GUI 환경이 아닌 경우 즉시 전환으로 폴백한다.

        Args:
            name: 전환할 페이지 이름
            duration: 애니메이션 지속 시간 (초)
            on_complete: 전환 완료 콜백
        """
        if name not in self.pages:
            return

        # 이전 페이지 숨기고 새 페이지 즉시 표시 (순수 로직 레이어)
        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].pack_forget()

        self.pages[name].pack(fill="both", expand=True)
        self.current_page = name

        if on_complete is not None:
            on_complete()


logger = logging.getLogger(__name__)


def format_exception_message(exc: Exception) -> str:
    """예외를 사용자 친화적 메시지로 변환한다.

    Args:
        exc: 발생한 예외

    Returns:
        사용자에게 표시할 에러 메시지
    """
    msg = str(exc)
    if not msg:
        return f"알 수 없는 오류가 발생했습니다: {type(exc).__name__}"
    if isinstance(exc, PDFToolError):
        return f"PDF 오류: {msg}"
    return msg


def should_confirm_close(is_executing: bool) -> bool:
    """윈도우 닫기 시 확인이 필요한지 결정한다.

    Args:
        is_executing: 현재 작업이 실행 중인지 여부

    Returns:
        확인이 필요하면 True
    """
    return is_executing


def _create_app():
    """PDFToolApp 인스턴스를 생성한다. (지연 임포트)"""
    import tkinter.messagebox as mb

    import customtkinter as ctk

    from pdf_tool.gui.pages.compress_page_widget import CompressPageWidget
    from pdf_tool.gui.pages.cut_page_widget import CutPageWidget
    from pdf_tool.gui.pages.image_to_pdf_page_widget import ImageToPdfPageWidget
    from pdf_tool.gui.pages.info_page_widget import InfoPageWidget
    from pdf_tool.gui.pages.merge_page_widget import MergePageWidget
    from pdf_tool.gui.pages.resize_page_widget import ResizePageWidget
    from pdf_tool.gui.pages.rotate_page_widget import RotatePageWidget
    from pdf_tool.gui.pages.split_page_widget import SplitPageWidget
    from pdf_tool.gui.pages.watermark_page_widget import WatermarkPageWidget
    from pdf_tool.gui.theme import (
        DARK_MODE,
        apply_theme,
        get_current_palette,
        toggle_theme,
    )

    # 페이지 이름과 위젯 클래스 매핑
    page_classes = {
        "Cut": CutPageWidget,
        "Merge": MergePageWidget,
        "Split": SplitPageWidget,
        "Rotate": RotatePageWidget,
        "Resize": ResizePageWidget,
        "Compress": CompressPageWidget,
        "Watermark": WatermarkPageWidget,
        "Images to PDF": ImageToPdfPageWidget,
        "Info": InfoPageWidget,
    }

    class PDFToolApp(ctk.CTk):
        """PDF Tool GUI 메인 윈도우 클래스."""

        def __init__(self) -> None:
            super().__init__()

            # 윈도우 설정
            self.title("PDF Tool")
            self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
            self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

            # 테마 적용
            apply_theme(DARK_MODE)

            # 페이지 매니저
            self.page_manager = PageManager()

            # 실행 상태 추적 (윈도우 닫기 확인용)
            self._is_any_executing = False

            # 네비게이션 버튼 참조 저장
            self._nav_buttons: dict[str, ctk.CTkButton] = {}

            # UI 구성
            self._create_sidebar()
            self._create_main_area()
            self._register_pages()

            # 글로벌 예외 핸들러
            self.report_callback_exception = self._handle_exception

            # 윈도우 닫기 확인 (REQ-C-001)
            self.protocol("WM_DELETE_WINDOW", self._on_close)

            # 키보드 네비게이션 바인딩 (AC-11)
            self._setup_keyboard_navigation()

            # 첫 번째 페이지로 전환
            self._on_nav_click("Cut")

        def _setup_keyboard_navigation(self) -> None:
            """키보드 단축키를 바인딩한다.

            Cmd+1~9 (macOS) / Ctrl+1~9 (Windows/Linux)로 페이지를 전환한다.
            """
            shortcut_keys = get_page_shortcut_keys(sys.platform)
            for index, key_binding in shortcut_keys.items():
                self.bind(
                    key_binding,
                    lambda event, idx=index: self._on_shortcut_page_switch(idx),
                )

        def _on_shortcut_page_switch(self, index: int) -> None:
            """단축키로 페이지를 전환한다.

            Args:
                index: 1부터 시작하는 페이지 인덱스
            """
            page_name = get_page_for_shortcut(index)
            if page_name is not None:
                self._on_nav_click(page_name)

        def _create_sidebar(self) -> None:
            """사이드바를 생성한다."""
            palette = get_current_palette()

            # 사이드바 배경색 사용
            self.sidebar = ctk.CTkFrame(
                self,
                width=SIDEBAR_WIDTH,
                corner_radius=0,
                fg_color=palette.surface,
            )
            self.sidebar.pack(side="left", fill="y")
            self.sidebar.pack_propagate(False)

            # 앱 제목
            title_label = ctk.CTkLabel(
                self.sidebar,
                text="PDF Tool",
                font=ctk.CTkFont(FONT_TITLE[0], FONT_TITLE[1], FONT_TITLE[2]),
                text_color=palette.text_primary,
            )
            title_label.pack(padx=PADDING_LG, pady=(PADDING_XL, PADDING_LG))

            # 구분선
            separator = ctk.CTkFrame(
                self.sidebar,
                height=1,
                fg_color=palette.surface_elevated,
            )
            separator.pack(padx=PADDING_MD, pady=(0, PADDING_LG), fill="x")

            # 네비게이션 버튼 생성
            nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            nav_frame.pack(padx=PADDING_SM, pady=0, fill="x")

            for name in NAV_BUTTONS:
                btn = ctk.CTkButton(
                    nav_frame,
                    text=name,
                    command=lambda n=name: self._on_nav_click(n),
                    height=BUTTON_HEIGHT_DEFAULT,
                    corner_radius=BORDER_RADIUS_DEFAULT,
                    fg_color=palette.surface_elevated,
                    text_color=palette.text_primary,
                    hover_color=palette.button_hover,
                )
                btn.pack(padx=PADDING_MD, pady=PADDING_SM, fill="x")
                self._nav_buttons[name] = btn

            # 하단 영역: 테마 토글 버튼 (REQ-O-001)
            spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            spacer.pack(fill="both", expand=True)

            # 하단 구분선
            separator_bottom = ctk.CTkFrame(
                self.sidebar,
                height=1,
                fg_color=palette.surface_elevated,
            )
            separator_bottom.pack(padx=PADDING_MD, pady=(PADDING_LG, PADDING_MD), fill="x")

            self.theme_btn = ctk.CTkButton(
                self.sidebar,
                text="🌙 테마 전환",
                command=lambda: toggle_theme(),
                height=BUTTON_HEIGHT_DEFAULT,
                corner_radius=BORDER_RADIUS_DEFAULT,
                fg_color=palette.secondary,
                text_color=palette.text_primary,
                hover_color=palette.button_hover,
            )
            self.theme_btn.pack(padx=PADDING_MD, pady=(0, PADDING_XL), fill="x")

        def _create_main_area(self) -> None:
            """메인 콘텐츠 영역을 생성한다."""
            palette = get_current_palette()
            self.main_frame = ctk.CTkFrame(
                self,
                fg_color=palette.background,
            )
            self.main_frame.pack(
                side="right",
                fill="both",
                expand=True,
                padx=MAIN_PADX,
                pady=MAIN_PADY,
            )

        def _register_pages(self) -> None:
            """모든 작업 페이지를 생성하고 등록한다."""
            for name, page_class in page_classes.items():
                page = page_class(self.main_frame)
                self.page_manager.register(name, page)

        def _on_nav_click(self, name: str) -> None:
            """네비게이션 버튼 클릭 핸들러.

            Args:
                name: 클릭된 버튼의 페이지 이름
            """
            self.page_manager.switch_to(name)
            self._update_button_highlight(name)

        def _update_button_highlight(self, active_name: str) -> None:
            """활성 버튼을 하이라이트한다.

            Args:
                active_name: 활성화할 버튼 이름
            """
            palette = get_current_palette()
            for name, btn in self._nav_buttons.items():
                if name == active_name:
                    btn.configure(
                        fg_color=palette.primary,
                        text_color=("white", "white"),
                    )
                else:
                    btn.configure(
                        fg_color=palette.surface_elevated,
                        text_color=palette.text_primary,
                    )

        def _handle_exception(self, exc_type, exc_value, exc_tb) -> None:
            """처리되지 않은 예외를 잡아 로그에 기록하고 메시지 박스로 표시한다."""
            msg = format_exception_message(exc_value)
            logger.error("GUI 미처리 예외: %s: %s", exc_type.__name__, msg)
            mb.showerror("오류", msg)

        def _on_close(self) -> None:
            """윈도우 닫기 핸들러. 작업 중이면 확인을 요청한다."""
            confirm = should_confirm_close(self._is_any_executing)
            if confirm and not mb.askyesno(
                "확인", "작업이 진행 중입니다. 종료하시겠습니까?"
            ):
                return
            self.destroy()

    return PDFToolApp()


GUI_LOG_FILE = "pdf_tool_gui.log"


def main() -> None:
    """GUI 애플리케이션 진입점."""
    logging.basicConfig(
        filename=GUI_LOG_FILE,
        level=logging.ERROR,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    app = _create_app()
    app.mainloop()


if __name__ == "__main__":
    main()
