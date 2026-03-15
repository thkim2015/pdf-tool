"""PDF 미리보기 렌더링 로직 테스트.

pypdfium2를 mock하여 pdf_preview 모듈의 순수 로직을 검증한다.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image


@pytest.fixture(autouse=True)
def _inject_mock_pdfium():
    """pypdfium2가 미설치일 때 mock pdfium을 모듈에 주입한다."""
    import pdf_tool.gui.widgets.pdf_preview as mod

    if not mod._pdfium_available:
        mock_pdfium = MagicMock()
        mod.pdfium = mock_pdfium
        mod._pdfium_available = True
        yield
        del mod.pdfium
        mod._pdfium_available = False
    else:
        yield


class Test_render_first_page_정상:
    """render_first_page가 정상 PDF를 렌더링하는지 검증한다."""

    def test_render_first_page_정상_PDF(self):
        """정상 PDF의 첫 페이지를 PIL Image로 반환한다."""
        from pdf_tool.gui.widgets.pdf_preview import render_first_page

        # 가짜 PIL Image (100x140)
        fake_image = Image.new("RGB", (100, 140))

        mock_bitmap = MagicMock()
        mock_bitmap.to_pil.return_value = fake_image

        mock_page = MagicMock()
        mock_page.render.return_value = mock_bitmap
        mock_page.get_width.return_value = 612.0
        mock_page.get_height.return_value = 792.0

        mock_pdf = MagicMock()
        mock_pdf.__len__ = MagicMock(return_value=5)
        mock_pdf.__getitem__ = MagicMock(return_value=mock_page)

        with patch(
            "pdf_tool.gui.widgets.pdf_preview.pdfium.PdfDocument",
            return_value=mock_pdf,
        ):
            result = render_first_page("/tmp/test.pdf", max_width=300)

        assert isinstance(result, Image.Image)
        # 썸네일 리사이즈로 원본보다 작거나 같아야 한다
        assert result.width <= 300
        mock_pdf.__getitem__.assert_called_once_with(0)
        mock_pdf.close.assert_called_once()

    def test_render_first_page_리사이즈(self):
        """max_width에 맞게 썸네일 리사이즈된다."""
        from pdf_tool.gui.widgets.pdf_preview import render_first_page

        # 큰 이미지 생성 (800x1120)
        fake_image = Image.new("RGB", (800, 1120))

        mock_bitmap = MagicMock()
        mock_bitmap.to_pil.return_value = fake_image

        mock_page = MagicMock()
        mock_page.render.return_value = mock_bitmap
        mock_page.get_width.return_value = 612.0
        mock_page.get_height.return_value = 792.0

        mock_pdf = MagicMock()
        mock_pdf.__len__ = MagicMock(return_value=1)
        mock_pdf.__getitem__ = MagicMock(return_value=mock_page)

        with patch(
            "pdf_tool.gui.widgets.pdf_preview.pdfium.PdfDocument",
            return_value=mock_pdf,
        ):
            result = render_first_page("/tmp/test.pdf", max_width=200)

        assert result.width <= 200
        assert result.height <= int(200 * 1.4)

    def test_render_first_page_Path_객체(self):
        """Path 객체도 인자로 받을 수 있다."""
        from pdf_tool.gui.widgets.pdf_preview import render_first_page

        fake_image = Image.new("RGB", (100, 140))
        mock_bitmap = MagicMock()
        mock_bitmap.to_pil.return_value = fake_image

        mock_page = MagicMock()
        mock_page.render.return_value = mock_bitmap
        mock_page.get_width.return_value = 612.0
        mock_page.get_height.return_value = 792.0

        mock_pdf = MagicMock()
        mock_pdf.__len__ = MagicMock(return_value=1)
        mock_pdf.__getitem__ = MagicMock(return_value=mock_page)

        with patch(
            "pdf_tool.gui.widgets.pdf_preview.pdfium.PdfDocument",
            return_value=mock_pdf,
        ):
            result = render_first_page(Path("/tmp/test.pdf"))

        assert isinstance(result, Image.Image)


class Test_render_first_page_에러:
    """render_first_page의 에러 처리를 검증한다."""

    def test_render_first_page_빈_PDF(self):
        """0페이지 PDF는 ValueError를 발생시킨다."""
        from pdf_tool.gui.widgets.pdf_preview import render_first_page

        mock_pdf = MagicMock()
        mock_pdf.__len__ = MagicMock(return_value=0)

        with patch(
            "pdf_tool.gui.widgets.pdf_preview.pdfium.PdfDocument",
            return_value=mock_pdf,
        ), pytest.raises(ValueError, match="페이지가 없습니다"):
            render_first_page("/tmp/empty.pdf")

        mock_pdf.close.assert_called_once()

    def test_render_first_page_손상_PDF(self):
        """렌더링 중 예외가 발생하면 그대로 전파한다."""
        from pdf_tool.gui.widgets.pdf_preview import render_first_page

        with patch(
            "pdf_tool.gui.widgets.pdf_preview.pdfium.PdfDocument",
            side_effect=RuntimeError("손상된 PDF"),
        ), pytest.raises(RuntimeError, match="손상된 PDF"):
            render_first_page("/tmp/broken.pdf")


class Test_is_preview_available:
    """pypdfium2 설치 여부에 따른 미리보기 가용성을 검증한다."""

    def test_is_preview_available_설치됨(self):
        """_pdfium_available이 True이면 True를 반환한다."""
        import pdf_tool.gui.widgets.pdf_preview as mod

        # fixture가 _pdfium_available = True로 설정해 줌
        assert mod.is_preview_available() is True

    def test_is_preview_available_미설치(self):
        """pypdfium2가 없으면 False를 반환한다."""
        import pdf_tool.gui.widgets.pdf_preview as mod

        # _pdfium_available 플래그를 직접 변경하여 미설치 시뮬레이션
        original = mod._pdfium_available
        try:
            mod._pdfium_available = False
            assert mod.is_preview_available() is False
        finally:
            mod._pdfium_available = original


class Test_open_pdf_in_viewer:
    """시스템 기본 뷰어로 PDF를 여는 기능을 검증한다."""

    def test_open_pdf_in_viewer_macos(self):
        """macOS에서는 open 명령을 사용한다."""
        from pdf_tool.gui.widgets.pdf_preview import open_pdf_in_viewer

        with (
            patch("pdf_tool.gui.widgets.pdf_preview.sys") as mock_sys,
            patch("pdf_tool.gui.widgets.pdf_preview.subprocess") as mock_sub,
        ):
            mock_sys.platform = "darwin"
            open_pdf_in_viewer("/tmp/test.pdf")
            mock_sub.Popen.assert_called_once_with(["open", "/tmp/test.pdf"])

    def test_open_pdf_in_viewer_windows(self):
        """Windows에서는 start 명령을 사용한다."""
        from pdf_tool.gui.widgets.pdf_preview import open_pdf_in_viewer

        with (
            patch("pdf_tool.gui.widgets.pdf_preview.sys") as mock_sys,
            patch("pdf_tool.gui.widgets.pdf_preview.subprocess") as mock_sub,
        ):
            mock_sys.platform = "win32"
            open_pdf_in_viewer("C:\\test.pdf")
            mock_sub.Popen.assert_called_once_with(
                ["start", "", "C:\\test.pdf"], shell=True
            )

    def test_open_pdf_in_viewer_linux(self):
        """Linux에서는 xdg-open 명령을 사용한다."""
        from pdf_tool.gui.widgets.pdf_preview import open_pdf_in_viewer

        with (
            patch("pdf_tool.gui.widgets.pdf_preview.sys") as mock_sys,
            patch("pdf_tool.gui.widgets.pdf_preview.subprocess") as mock_sub,
        ):
            mock_sys.platform = "linux"
            open_pdf_in_viewer("/home/user/test.pdf")
            mock_sub.Popen.assert_called_once_with(
                ["xdg-open", "/home/user/test.pdf"]
            )

    def test_open_pdf_in_viewer_Path_객체(self):
        """Path 객체도 인자로 받을 수 있다."""
        from pdf_tool.gui.widgets.pdf_preview import open_pdf_in_viewer

        with (
            patch("pdf_tool.gui.widgets.pdf_preview.sys") as mock_sys,
            patch("pdf_tool.gui.widgets.pdf_preview.subprocess") as mock_sub,
        ):
            mock_sys.platform = "darwin"
            open_pdf_in_viewer(Path("/tmp/test.pdf"))
            mock_sub.Popen.assert_called_once_with(
                ["open", "/tmp/test.pdf"]
            )
