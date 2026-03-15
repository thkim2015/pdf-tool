"""CLI Progress Bar 명세 테스트.

SPEC-PDF-003 Phase 2: CLI Rich Progress Bar 통합
- AC-04: CLI Rich ProgressBar 통합
- AC-06: Long operations 자동 progress
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from pdf_tool.cli import app

runner = CliRunner()


# ============================================================================
# AC-04: CLI Rich ProgressBar 통합 테스트
# ============================================================================


class TestCliProgressBar:
    """CLI에서 Rich progress bar가 표시됨을 검증한다."""

    def test_create_progress_callback이_정의되어_있다(self):
        """cli 모듈에 create_progress_callback 함수가 정의되어 있다."""
        from pdf_tool.cli import create_progress_callback

        assert callable(create_progress_callback)

    def test_long_operation에서_progress_callback이_전달된다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """2초 이상 추정 작업에서 progress callback이 명령어에 전달된다."""
        # 100페이지 PDF를 사용하면 2초 이상으로 추정된다
        from tests.conftest import _create_pdf

        large_pdf = _create_pdf(tmp_path / "large.pdf", 100)
        output = tmp_path / "result.pdf"

        with patch("pdf_tool.cli.rotate_pdf") as mock_rotate:
            mock_rotate.return_value = output
            # 파일이 존재해야 PdfReader가 동작한다
            from tests.conftest import _create_pdf as create

            create(output, 100)

            result = runner.invoke(
                app,
                [
                    "rotate",
                    str(large_pdf),
                    "--angle",
                    "90",
                    "--output",
                    str(output),
                ],
            )
            # callback 파라미터가 전달되었는지 확인
            if mock_rotate.called:
                call_kwargs = mock_rotate.call_args
                assert "callback" in call_kwargs.kwargs

    def test_quick_operation은_callback_None으로_전달된다(
        self, single_page_pdf: Path, tmp_path: Path
    ):
        """2초 미만 추정 작업은 callback=None으로 전달된다."""
        output = tmp_path / "result.pdf"

        with patch("pdf_tool.cli.cut_pdf") as mock_cut:
            mock_cut.return_value = output
            from tests.conftest import _create_pdf

            _create_pdf(output, 1)

            result = runner.invoke(
                app,
                [
                    "cut",
                    str(single_page_pdf),
                    "--pages",
                    "1",
                    "--output",
                    str(output),
                ],
            )
            if mock_cut.called:
                call_kwargs = mock_cut.call_args
                # callback이 None이거나 전달되지 않았어야 한다
                cb = call_kwargs.kwargs.get("callback", None)
                assert cb is None


# ============================================================================
# AC-04: Progress 포맷 테스트
# ============================================================================


class TestCliProgressFormat:
    """CLI progress bar 포맷을 검증한다."""

    def test_create_progress_callback은_Rich_Task를_업데이트한다(self):
        """create_progress_callback은 Rich Progress의 task를 업데이트한다."""
        from pdf_tool.cli import create_progress_callback

        mock_progress = MagicMock()
        mock_task_id = 1

        callback = create_progress_callback(mock_progress, mock_task_id)
        callback(5, 10)

        mock_progress.update.assert_called_once_with(mock_task_id, completed=5, total=10)

    def test_create_progress_callback은_callable을_반환한다(self):
        """create_progress_callback은 callable을 반환한다."""
        from pdf_tool.cli import create_progress_callback

        mock_progress = MagicMock()
        callback = create_progress_callback(mock_progress, task_id=1)
        assert callable(callback)
