"""file_utils 모듈의 명세 테스트."""

from pathlib import Path

from pdf_tool.utils.file_utils import generate_output_filename


class TestGenerateOutputFilename:
    """출력 파일명 자동 생성 기능을 검증한다."""

    def test_cut_명령의_출력_파일명을_생성한다(self):
        """cut 명령에 대해 _cut 접미사가 붙은 파일명을 생성한다."""
        result = generate_output_filename(Path("report.pdf"), "cut")
        assert result == Path("report_cut.pdf")

    def test_merge_명령의_출력_파일명을_생성한다(self):
        """merge 명령에 대해 _merged 접미사가 붙은 파일명을 생성한다."""
        result = generate_output_filename(Path("report.pdf"), "merge")
        assert result == Path("report_merged.pdf")

    def test_split_명령의_출력_파일명을_생성한다(self):
        """split 명령에 대해 번호가 포함된 패턴을 생성한다."""
        result = generate_output_filename(Path("report.pdf"), "split")
        assert result == Path("report_{num:03d}.pdf")

    def test_rotate_명령의_출력_파일명을_생성한다(self):
        """rotate 명령에 대해 _rotated 접미사가 붙은 파일명을 생성한다."""
        result = generate_output_filename(Path("report.pdf"), "rotate")
        assert result == Path("report_rotated.pdf")

    def test_경로가_포함된_파일명을_처리한다(self):
        """디렉토리 경로가 포함된 입력에서도 올바르게 생성한다."""
        result = generate_output_filename(Path("/tmp/docs/report.pdf"), "cut")
        assert result == Path("/tmp/docs/report_cut.pdf")
