"""GUI 공통 위젯 테스트.

customtkinter 위젯을 mock하여 순수 로직을 검증한다.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch


class Test_FilePicker_로직:
    """FilePicker 위젯의 파일 선택 로직을 검증한다."""

    def test_pdf_확장자_검증_성공(self):
        """PDF 파일 확장자는 유효하다."""
        from pdf_tool.gui.widgets.file_picker import is_valid_pdf_extension

        assert is_valid_pdf_extension(Path("test.pdf")) is True
        assert is_valid_pdf_extension(Path("test.PDF")) is True

    def test_pdf_확장자_검증_실패(self):
        """PDF가 아닌 확장자는 유효하지 않다."""
        from pdf_tool.gui.widgets.file_picker import is_valid_pdf_extension

        assert is_valid_pdf_extension(Path("test.txt")) is False
        assert is_valid_pdf_extension(Path("test.docx")) is False
        assert is_valid_pdf_extension(Path("test")) is False

    def test_파일_정보_추출(self):
        """PDF 파일의 기본 정보(이름, 페이지 수)를 추출한다."""
        from pdf_tool.gui.widgets.file_picker import get_pdf_info

        with patch("pdf_tool.gui.widgets.file_picker.PdfReader") as mock_reader:
            mock_instance = MagicMock()
            mock_instance.pages = [MagicMock()] * 5
            mock_reader.return_value = mock_instance

            info = get_pdf_info(Path("test.pdf"))
            assert info["name"] == "test.pdf"
            assert info["pages"] == 5

    def test_파일_정보_추출_실패(self):
        """유효하지 않은 PDF는 None을 반환한다."""
        from pdf_tool.gui.widgets.file_picker import get_pdf_info

        with patch("pdf_tool.gui.widgets.file_picker.PdfReader") as mock_reader:
            mock_reader.side_effect = Exception("파일 읽기 실패")
            info = get_pdf_info(Path("invalid.pdf"))
            assert info is None


class Test_ProgressBar_로직:
    """ProgressBar 위젯의 상태 관리 로직을 검증한다."""

    def test_초기_상태(self):
        """초기 상태는 정지 상태이다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        assert state.is_running is False
        assert state.message == ""

    def test_시작_상태(self):
        """start() 호출 시 실행 상태로 전환된다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        state.start("처리 중...")
        assert state.is_running is True
        assert state.message == "처리 중..."

    def test_정지_상태(self):
        """stop() 호출 시 정지 상태로 전환된다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        state.start("처리 중...")
        state.stop()
        assert state.is_running is False

    def test_리셋(self):
        """reset() 호출 시 초기 상태로 돌아간다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        state.start("처리 중...")
        state.reset()
        assert state.is_running is False
        assert state.message == ""


class Test_PageRangeInput_로직:
    """PageRangeInput 위젯의 페이지 범위 검증 로직을 검증한다."""

    def test_유효한_페이지_범위(self):
        """유효한 페이지 범위 문자열을 검증한다."""
        from pdf_tool.gui.widgets.page_range_input import validate_page_range_input

        assert validate_page_range_input("1-3, 5, 8-10") is True
        assert validate_page_range_input("1") is True
        assert validate_page_range_input("1,2,3") is True

    def test_빈_문자열(self):
        """빈 문자열은 유효하다 (선택적 입력)."""
        from pdf_tool.gui.widgets.page_range_input import validate_page_range_input

        assert validate_page_range_input("") is True
        assert validate_page_range_input("  ") is True

    def test_유효하지_않은_페이지_범위(self):
        """유효하지 않은 형식은 False를 반환한다."""
        from pdf_tool.gui.widgets.page_range_input import validate_page_range_input

        assert validate_page_range_input("abc") is False
        assert validate_page_range_input("1-2-3") is False
        assert validate_page_range_input("0") is False


class Test_FileList_로직:
    """FileList 위젯의 파일 목록 관리 로직을 검증한다."""

    def test_빈_목록_초기화(self):
        """초기 파일 목록은 비어있다."""
        from pdf_tool.gui.widgets.file_list import FileListState

        state = FileListState()
        assert state.get_files() == []

    def test_파일_추가(self):
        """파일을 목록에 추가할 수 있다."""
        from pdf_tool.gui.widgets.file_list import FileListState

        state = FileListState()
        state.add_files([Path("a.pdf"), Path("b.pdf")])
        assert len(state.get_files()) == 2

    def test_파일_제거(self):
        """인덱스로 파일을 제거할 수 있다."""
        from pdf_tool.gui.widgets.file_list import FileListState

        state = FileListState()
        state.add_files([Path("a.pdf"), Path("b.pdf"), Path("c.pdf")])
        state.remove_file(1)
        files = state.get_files()
        assert len(files) == 2
        assert files[0] == Path("a.pdf")
        assert files[1] == Path("c.pdf")

    def test_파일_위로_이동(self):
        """파일을 한 칸 위로 이동할 수 있다."""
        from pdf_tool.gui.widgets.file_list import FileListState

        state = FileListState()
        state.add_files([Path("a.pdf"), Path("b.pdf"), Path("c.pdf")])
        state.move_up(1)
        files = state.get_files()
        assert files[0] == Path("b.pdf")
        assert files[1] == Path("a.pdf")

    def test_파일_아래로_이동(self):
        """파일을 한 칸 아래로 이동할 수 있다."""
        from pdf_tool.gui.widgets.file_list import FileListState

        state = FileListState()
        state.add_files([Path("a.pdf"), Path("b.pdf"), Path("c.pdf")])
        state.move_down(0)
        files = state.get_files()
        assert files[0] == Path("b.pdf")
        assert files[1] == Path("a.pdf")

    def test_첫번째_파일_위로_이동_무시(self):
        """첫 번째 파일은 위로 이동할 수 없다."""
        from pdf_tool.gui.widgets.file_list import FileListState

        state = FileListState()
        state.add_files([Path("a.pdf"), Path("b.pdf")])
        state.move_up(0)
        files = state.get_files()
        assert files[0] == Path("a.pdf")

    def test_마지막_파일_아래로_이동_무시(self):
        """마지막 파일은 아래로 이동할 수 없다."""
        from pdf_tool.gui.widgets.file_list import FileListState

        state = FileListState()
        state.add_files([Path("a.pdf"), Path("b.pdf")])
        state.move_down(1)
        files = state.get_files()
        assert files[1] == Path("b.pdf")


class Test_ResultDisplay_로직:
    """ResultDisplay 위젯의 결과 데이터 관리 로직을 검증한다."""

    def test_초기_상태(self):
        """초기 상태는 빈 상태이다."""
        from pdf_tool.gui.widgets.result_display import ResultState

        state = ResultState()
        assert state.result_type is None
        assert state.message == ""

    def test_성공_결과(self):
        """성공 결과를 설정할 수 있다."""
        from pdf_tool.gui.widgets.result_display import ResultState

        state = ResultState()
        state.show_success("완료됨", Path("/output/result.pdf"))
        assert state.result_type == "success"
        assert state.message == "완료됨"
        assert state.output_path == Path("/output/result.pdf")

    def test_에러_결과(self):
        """에러 결과를 설정할 수 있다."""
        from pdf_tool.gui.widgets.result_display import ResultState

        state = ResultState()
        state.show_error("파일을 찾을 수 없습니다")
        assert state.result_type == "error"
        assert state.message == "파일을 찾을 수 없습니다"

    def test_정보_결과(self):
        """정보(dict) 결과를 설정할 수 있다."""
        from pdf_tool.gui.widgets.result_display import ResultState

        state = ResultState()
        data = {"title": "테스트", "pages": 10}
        state.show_info(data)
        assert state.result_type == "info"
        assert state.data == data

    def test_결과_초기화(self):
        """clear() 호출 시 초기 상태로 돌아간다."""
        from pdf_tool.gui.widgets.result_display import ResultState

        state = ResultState()
        state.show_success("완료됨", Path("/output/result.pdf"))
        state.clear()
        assert state.result_type is None
        assert state.message == ""
