"""GUI 작업 페이지 테스트.

각 페이지가 올바른 커맨드 함수를 올바른 인자로 호출하는지 검증한다.
GUI 위젯은 mock하고 커맨드 호출 로직만 테스트한다.
"""

from pathlib import Path
from unittest.mock import patch

import pytest


# --- InfoPage ---
class Test_InfoPage_로직:
    """InfoPage의 메타데이터 로드 로직을 검증한다."""

    def test_메타데이터_로드(self):
        """get_metadata를 올바르게 호출한다."""
        from pdf_tool.gui.pages.info_page import load_metadata

        with patch("pdf_tool.gui.pages.info_page.get_metadata") as mock_cmd:
            mock_cmd.return_value = {"title": "Test", "pages": 5}
            result = load_metadata(Path("/tmp/test.pdf"))
            mock_cmd.assert_called_once_with(Path("/tmp/test.pdf"))
            assert result["title"] == "Test"
            assert result["pages"] == 5

    def test_메타데이터_로드_실패(self):
        """잘못된 파일에서 예외를 전파한다."""
        from pdf_tool.gui.pages.info_page import load_metadata

        with patch("pdf_tool.gui.pages.info_page.get_metadata") as mock_cmd:
            mock_cmd.side_effect = Exception("파일 읽기 실패")
            with pytest.raises(Exception, match="파일 읽기 실패"):
                load_metadata(Path("/tmp/bad.pdf"))


# --- CompressPage ---
class Test_CompressPage_로직:
    """CompressPage의 압축 실행 로직을 검증한다."""

    def test_압축_실행(self):
        """compress_pdf를 올바르게 호출한다."""
        from pdf_tool.gui.pages.compress_page import run_compress

        with patch("pdf_tool.gui.pages.compress_page.compress_pdf") as mock_cmd:
            mock_cmd.return_value = {
                "output_path": Path("/tmp/test_compressed.pdf"),
                "original_size": 1000,
                "compressed_size": 500,
                "reduction_percent": 50.0,
            }
            result = run_compress(Path("/tmp/test.pdf"), Path("/tmp/test_compressed.pdf"))
            mock_cmd.assert_called_once_with(
                Path("/tmp/test.pdf"), output=Path("/tmp/test_compressed.pdf")
            )
            assert result["reduction_percent"] == 50.0


# --- CutPage ---
class Test_CutPage_로직:
    """CutPage의 잘라내기 실행 로직을 검증한다."""

    def test_잘라내기_실행(self):
        """cut_pdf를 올바른 인자로 호출한다."""
        from pdf_tool.gui.pages.cut_page import run_cut

        with patch("pdf_tool.gui.pages.cut_page.cut_pdf") as mock_cmd:
            mock_cmd.return_value = Path("/tmp/test_cut.pdf")
            result = run_cut(Path("/tmp/test.pdf"), "1-3,5", Path("/tmp/test_cut.pdf"))
            mock_cmd.assert_called_once_with(
                Path("/tmp/test.pdf"),
                pages="1-3,5",
                output=Path("/tmp/test_cut.pdf"),
            )
            assert result == Path("/tmp/test_cut.pdf")


# --- RotatePage ---
class Test_RotatePage_로직:
    """RotatePage의 회전 실행 로직을 검증한다."""

    def test_전체_회전_실행(self):
        """rotate_pdf를 각도와 함께 호출한다."""
        from pdf_tool.gui.pages.rotate_page import run_rotate

        with patch("pdf_tool.gui.pages.rotate_page.rotate_pdf") as mock_cmd:
            mock_cmd.return_value = Path("/tmp/test_rotated.pdf")
            run_rotate(
                Path("/tmp/test.pdf"), 90, None, Path("/tmp/test_rotated.pdf")
            )
            mock_cmd.assert_called_once_with(
                Path("/tmp/test.pdf"),
                angle=90,
                pages=None,
                output=Path("/tmp/test_rotated.pdf"),
            )

    def test_특정_페이지_회전(self):
        """특정 페이지만 회전한다."""
        from pdf_tool.gui.pages.rotate_page import run_rotate

        with patch("pdf_tool.gui.pages.rotate_page.rotate_pdf") as mock_cmd:
            mock_cmd.return_value = Path("/tmp/test_rotated.pdf")
            run_rotate(
                Path("/tmp/test.pdf"), 180, "1,3", Path("/tmp/test_rotated.pdf")
            )
            mock_cmd.assert_called_once_with(
                Path("/tmp/test.pdf"),
                angle=180,
                pages="1,3",
                output=Path("/tmp/test_rotated.pdf"),
            )


# --- SplitPage ---
class Test_SplitPage_로직:
    """SplitPage의 분할 실행 로직을 검증한다."""

    def test_분할_실행(self):
        """split_pdf를 올바르게 호출한다."""
        from pdf_tool.gui.pages.split_page import run_split

        with patch("pdf_tool.gui.pages.split_page.split_pdf") as mock_cmd:
            mock_cmd.return_value = [
                Path("/tmp/out/part_1.pdf"),
                Path("/tmp/out/part_2.pdf"),
            ]
            result = run_split(Path("/tmp/test.pdf"), 2, Path("/tmp/out"))
            mock_cmd.assert_called_once_with(
                Path("/tmp/test.pdf"),
                every=2,
                output_dir=Path("/tmp/out"),
            )
            assert len(result) == 2


# --- ResizePage ---
class Test_ResizePage_로직:
    """ResizePage의 크기 변경 실행 로직을 검증한다."""

    def test_용지_크기로_리사이즈(self):
        """resize_pdf를 용지 크기와 모드로 호출한다."""
        from pdf_tool.gui.pages.resize_page import run_resize

        with patch("pdf_tool.gui.pages.resize_page.resize_pdf") as mock_cmd:
            mock_cmd.return_value = Path("/tmp/test_resized.pdf")
            run_resize(
                Path("/tmp/test.pdf"), "A4", "fit", Path("/tmp/test_resized.pdf")
            )
            mock_cmd.assert_called_once_with(
                Path("/tmp/test.pdf"),
                size="A4",
                mode="fit",
                output=Path("/tmp/test_resized.pdf"),
            )


# --- MergePage ---
class Test_MergePage_로직:
    """MergePage의 병합 실행 로직을 검증한다."""

    def test_병합_실행(self):
        """merge_pdfs를 올바르게 호출한다."""
        from pdf_tool.gui.pages.merge_page import run_merge

        with patch("pdf_tool.gui.pages.merge_page.merge_pdfs") as mock_cmd:
            mock_cmd.return_value = Path("/tmp/merged.pdf")
            files = [Path("/tmp/a.pdf"), Path("/tmp/b.pdf")]
            result = run_merge(files, Path("/tmp/merged.pdf"))
            mock_cmd.assert_called_once_with(
                files,
                output=Path("/tmp/merged.pdf"),
            )
            assert result == Path("/tmp/merged.pdf")


# --- WatermarkPage ---
class Test_WatermarkPage_로직:
    """WatermarkPage의 워터마크 실행 로직을 검증한다."""

    def test_텍스트_워터마크(self):
        """텍스트 워터마크를 올바르게 호출한다."""
        from pdf_tool.gui.pages.watermark_page import run_watermark

        with patch("pdf_tool.gui.pages.watermark_page.watermark_pdf") as mock_cmd:
            mock_cmd.return_value = Path("/tmp/test_watermarked.pdf")
            run_watermark(
                input_path=Path("/tmp/test.pdf"),
                output_path=Path("/tmp/test_watermarked.pdf"),
                text="SAMPLE",
                image=None,
                opacity=0.3,
                rotation=45.0,
                position="center",
                pages=None,
            )
            mock_cmd.assert_called_once_with(
                Path("/tmp/test.pdf"),
                output=Path("/tmp/test_watermarked.pdf"),
                text="SAMPLE",
                image=None,
                opacity=0.3,
                rotation=45.0,
                position="center",
                pages=None,
            )

    def test_이미지_워터마크(self):
        """이미지 워터마크를 올바르게 호출한다."""
        from pdf_tool.gui.pages.watermark_page import run_watermark

        with patch("pdf_tool.gui.pages.watermark_page.watermark_pdf") as mock_cmd:
            mock_cmd.return_value = Path("/tmp/test_watermarked.pdf")
            run_watermark(
                input_path=Path("/tmp/test.pdf"),
                output_path=Path("/tmp/test_watermarked.pdf"),
                text=None,
                image=Path("/tmp/logo.png"),
                opacity=0.5,
                rotation=0.0,
                position="center",
                pages="1-3",
            )
            mock_cmd.assert_called_once_with(
                Path("/tmp/test.pdf"),
                output=Path("/tmp/test_watermarked.pdf"),
                text=None,
                image=Path("/tmp/logo.png"),
                opacity=0.5,
                rotation=0.0,
                position="center",
                pages="1-3",
            )
