"""GUI BasePage 테스트.

스레드 실행, 출력 경로 생성, 덮어쓰기 검증 등 순수 로직을 검증한다.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class Test_출력_경로_생성:
    """기본 출력 경로 생성 로직을 검증한다."""

    def test_기본_출력_경로(self):
        """입력 파일 이름에 _output 접미사를 붙인 경로를 생성한다."""
        from pdf_tool.gui.pages.base_page import generate_output_path

        result = generate_output_path(Path("/tmp/test.pdf"))
        assert result == Path("/tmp/test_output.pdf")

    def test_출력_경로_커스텀_접미사(self):
        """커스텀 접미사로 출력 경로를 생성한다."""
        from pdf_tool.gui.pages.base_page import generate_output_path

        result = generate_output_path(Path("/tmp/test.pdf"), suffix="_cut")
        assert result == Path("/tmp/test_cut.pdf")

    def test_출력_경로_확장자_유지(self):
        """원본 확장자(.pdf)를 유지한다."""
        from pdf_tool.gui.pages.base_page import generate_output_path

        result = generate_output_path(Path("/home/user/report.pdf"))
        assert result.suffix == ".pdf"


class Test_덮어쓰기_검증:
    """입력 파일과 출력 파일이 같을 때 덮어쓰기를 방지하는 로직을 검증한다."""

    def test_같은_경로_덮어쓰기_감지(self):
        """입력과 출력이 같은 경로이면 True를 반환한다."""
        from pdf_tool.gui.pages.base_page import would_overwrite

        assert would_overwrite(Path("/tmp/a.pdf"), Path("/tmp/a.pdf")) is True

    def test_다른_경로_정상(self):
        """입력과 출력이 다른 경로이면 False를 반환한다."""
        from pdf_tool.gui.pages.base_page import would_overwrite

        assert would_overwrite(Path("/tmp/a.pdf"), Path("/tmp/b.pdf")) is False

    def test_None_출력_경로_정상(self):
        """출력 경로가 None이면 False를 반환한다."""
        from pdf_tool.gui.pages.base_page import would_overwrite

        assert would_overwrite(Path("/tmp/a.pdf"), None) is False


class Test_커맨드_실행_상태:
    """커맨드 실행 상태 관리 로직을 검증한다."""

    def test_초기_상태(self):
        """초기 상태에서 실행 중이 아니다."""
        from pdf_tool.gui.pages.base_page import ExecutionState

        state = ExecutionState()
        assert state.is_executing is False
        assert state.input_file is None

    def test_실행_시작(self):
        """실행을 시작하면 상태가 변경된다."""
        from pdf_tool.gui.pages.base_page import ExecutionState

        state = ExecutionState()
        state.start(Path("/tmp/test.pdf"))
        assert state.is_executing is True
        assert state.input_file == Path("/tmp/test.pdf")

    def test_실행_완료(self):
        """실행이 완료되면 실행 상태가 False로 변경된다."""
        from pdf_tool.gui.pages.base_page import ExecutionState

        state = ExecutionState()
        state.start(Path("/tmp/test.pdf"))
        state.finish()
        assert state.is_executing is False

    def test_실행_가능_여부_파일_없음(self):
        """파일이 없으면 실행할 수 없다."""
        from pdf_tool.gui.pages.base_page import ExecutionState

        state = ExecutionState()
        assert state.can_execute is False

    def test_실행_가능_여부_파일_있음(self):
        """파일이 있고 실행 중이 아니면 실행할 수 있다."""
        from pdf_tool.gui.pages.base_page import ExecutionState

        state = ExecutionState()
        state.input_file = Path("/tmp/test.pdf")
        assert state.can_execute is True

    def test_실행_중_재실행_불가(self):
        """실행 중에는 재실행할 수 없다."""
        from pdf_tool.gui.pages.base_page import ExecutionState

        state = ExecutionState()
        state.start(Path("/tmp/test.pdf"))
        assert state.can_execute is False
