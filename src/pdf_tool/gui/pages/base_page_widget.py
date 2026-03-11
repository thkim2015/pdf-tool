"""BasePage GUI 위젯 모듈.

모든 작업 페이지의 공통 GUI 레이아웃과 스레드 실행 패턴을 제공한다.
"""

from __future__ import annotations

import threading
from abc import abstractmethod
from pathlib import Path

import customtkinter as ctk

from pdf_tool.gui.app import format_exception_message
from pdf_tool.gui.pages.base_page import ExecutionState, generate_output_path, would_overwrite
from pdf_tool.gui.widgets.file_picker_widget import FilePickerWidget
from pdf_tool.gui.widgets.progress_bar_widget import ProgressBarWidget
from pdf_tool.gui.widgets.result_display_widget import ResultDisplayWidget


class BasePageWidget(ctk.CTkFrame):
    """작업 페이지의 기본 위젯 클래스.

    공통 레이아웃: 파일 입력 -> 파라미터 -> 실행 버튼 -> 프로그레스 바 -> 결과
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self._execution_state = ExecutionState()

        self._create_layout()

    def _create_layout(self) -> None:
        """공통 레이아웃을 생성한다."""
        # 파일 선택 영역
        self.file_picker = FilePickerWidget(
            self,
            on_file_selected=self._on_file_selected,
        )
        self.file_picker.pack(fill="x", padx=10, pady=5)

        # 파라미터 영역 (서브클래스에서 구현)
        self.params_frame = ctk.CTkFrame(self)
        self.params_frame.pack(fill="x", padx=10, pady=5)
        self.create_params_ui(self.params_frame)

        # 실행 버튼
        self.execute_btn = ctk.CTkButton(
            self,
            text="실행",
            command=self._on_execute,
            state="disabled",
        )
        self.execute_btn.pack(pady=10, padx=10, fill="x")

        # 프로그레스 바
        self.progress_bar = ProgressBarWidget(self)

        # 결과 영역
        self.result_display = ResultDisplayWidget(self)
        self.result_display.pack(fill="both", expand=True, padx=10, pady=5)

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
            self.after(0, lambda: self._on_error(exc))

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
