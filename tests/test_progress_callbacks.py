"""Progress Callback Framework 명세 테스트.

SPEC-PDF-003 Phase 1: 대용량 PDF 처리 지원 및 진행 상황 추적 개선
- R1: ProgressCallback Protocol 설계
- R2: 8개 명령어 콜백 통합
- R5: 하위 호환성
- R6: 콜백 예외 안전성
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pypdf import PdfReader

# ============================================================================
# R1: ProgressCallback 타입 및 safe_callback 테스트
# ============================================================================


class TestProgressCallbackType:
    """ProgressCallback 타입 정의를 검증한다."""

    def test_ProgressCallback_타입이_정의되어_있다(self):
        """ProgressCallback이 core.progress에 정의되어 있다."""
        from pdf_tool.core.progress import ProgressCallback

        assert ProgressCallback is not None

    def test_ProgressCallback은_None을_허용한다(self):
        """ProgressCallback은 Optional이므로 None이 될 수 있다."""
        from pdf_tool.core.progress import ProgressCallback

        callback: ProgressCallback = None
        assert callback is None

    def test_ProgressCallback은_Callable을_받는다(self):
        """ProgressCallback은 (int, int) -> None 형태의 Callable을 받는다."""
        from pdf_tool.core.progress import ProgressCallback

        def my_callback(current: int, total: int) -> None:
            pass

        callback: ProgressCallback = my_callback
        assert callable(callback)


class TestSafeCallback:
    """safe_callback 래퍼의 예외 안전성을 검증한다."""

    def test_safe_callback은_정상_콜백을_실행한다(self):
        """정상적인 콜백은 그대로 실행된다."""
        from pdf_tool.core.progress import safe_callback

        mock = MagicMock()
        safe_callback(mock, 1, 10)
        mock.assert_called_once_with(1, 10)

    def test_safe_callback은_None_콜백을_무시한다(self):
        """콜백이 None이면 아무 동작도 하지 않는다."""
        from pdf_tool.core.progress import safe_callback

        # None 콜백을 호출해도 에러가 발생하지 않는다
        safe_callback(None, 1, 10)

    def test_safe_callback은_예외를_삼킨다(self):
        """콜백이 예외를 발생시켜도 전파되지 않는다."""
        from pdf_tool.core.progress import safe_callback

        def bad_callback(current: int, total: int) -> None:
            raise ValueError("콜백 에러")

        # 예외가 전파되지 않아야 한다
        safe_callback(bad_callback, 1, 10)

    def test_safe_callback은_RuntimeError도_삼킨다(self):
        """RuntimeError도 안전하게 처리한다."""
        from pdf_tool.core.progress import safe_callback

        def bad_callback(current: int, total: int) -> None:
            raise RuntimeError("심각한 에러")

        safe_callback(bad_callback, 5, 10)

    def test_safe_callback은_KeyboardInterrupt를_전파한다(self):
        """KeyboardInterrupt는 예외 안전성에서 제외된다."""
        from pdf_tool.core.progress import safe_callback

        def interrupt_callback(current: int, total: int) -> None:
            raise KeyboardInterrupt()

        with pytest.raises(KeyboardInterrupt):
            safe_callback(interrupt_callback, 1, 10)


# ============================================================================
# R2: pdf_handler 콜백 통합 테스트
# ============================================================================


class TestPdfHandlerCallback:
    """pdf_handler의 load_pdf에 콜백 파라미터가 추가됨을 검증한다."""

    def test_load_pdf는_callback_파라미터를_받는다(self, sample_pdf: Path):
        """load_pdf에 callback 파라미터를 전달할 수 있다."""
        from pdf_tool.core.pdf_handler import load_pdf

        mock = MagicMock()
        reader = load_pdf(sample_pdf, callback=mock)
        assert isinstance(reader, PdfReader)

    def test_load_pdf는_callback_없이도_동작한다(self, sample_pdf: Path):
        """하위 호환성: callback 없이도 정상 동작한다."""
        from pdf_tool.core.pdf_handler import load_pdf

        reader = load_pdf(sample_pdf)
        assert isinstance(reader, PdfReader)
        assert len(reader.pages) == 10


# ============================================================================
# R2: 8개 명령어 콜백 통합 테스트
# ============================================================================


class TestCutPdfCallback:
    """cut_pdf 명령어의 콜백 통합을 검증한다."""

    def test_cut_pdf는_callback을_받는다(self, sample_pdf: Path, tmp_path: Path):
        """cut_pdf에 callback을 전달할 수 있다."""
        from pdf_tool.commands.cut import cut_pdf

        mock = MagicMock()
        output = tmp_path / "cut_result.pdf"
        cut_pdf(sample_pdf, pages="1-3", output=output, callback=mock)
        assert output.exists()
        assert mock.call_count > 0

    def test_cut_pdf는_callback_없이도_동작한다(self, sample_pdf: Path, tmp_path: Path):
        """하위 호환성: callback 없이도 정상 동작한다."""
        from pdf_tool.commands.cut import cut_pdf

        output = tmp_path / "cut_result.pdf"
        result = cut_pdf(sample_pdf, pages="1-3", output=output)
        assert result == output
        assert output.exists()

    def test_cut_pdf_callback은_current_total을_전달한다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """콜백에 (current, total) 인수가 전달된다."""
        from pdf_tool.commands.cut import cut_pdf

        calls = []

        def track(current: int, total: int) -> None:
            calls.append((current, total))

        output = tmp_path / "cut_track.pdf"
        cut_pdf(sample_pdf, pages="1-3", output=output, callback=track)
        assert len(calls) > 0
        # 마지막 호출의 current == total (완료)
        last_current, last_total = calls[-1]
        assert last_current == last_total


class TestMergePdfCallback:
    """merge_pdfs 명령어의 콜백 통합을 검증한다."""

    def test_merge_pdfs는_callback을_받는다(
        self, sample_pdf: Path, small_pdf: Path, tmp_path: Path
    ):
        """merge_pdfs에 callback을 전달할 수 있다."""
        from pdf_tool.commands.merge import merge_pdfs

        mock = MagicMock()
        output = tmp_path / "merge_result.pdf"
        merge_pdfs([sample_pdf, small_pdf], output=output, callback=mock)
        assert output.exists()
        assert mock.call_count > 0

    def test_merge_pdfs는_callback_없이도_동작한다(
        self, sample_pdf: Path, small_pdf: Path, tmp_path: Path
    ):
        """하위 호환성: callback 없이도 정상 동작한다."""
        from pdf_tool.commands.merge import merge_pdfs

        output = tmp_path / "merge_result.pdf"
        result = merge_pdfs([sample_pdf, small_pdf], output=output)
        assert result == output


class TestSplitPdfCallback:
    """split_pdf 명령어의 콜백 통합을 검증한다."""

    def test_split_pdf는_callback을_받는다(self, sample_pdf: Path, tmp_path: Path):
        """split_pdf에 callback을 전달할 수 있다."""
        from pdf_tool.commands.split import split_pdf

        mock = MagicMock()
        split_pdf(sample_pdf, every=2, output_dir=tmp_path, callback=mock)
        assert mock.call_count > 0

    def test_split_pdf는_callback_없이도_동작한다(self, sample_pdf: Path, tmp_path: Path):
        """하위 호환성: callback 없이도 정상 동작한다."""
        from pdf_tool.commands.split import split_pdf

        results = split_pdf(sample_pdf, every=5, output_dir=tmp_path)
        assert len(results) == 2


class TestRotatePdfCallback:
    """rotate_pdf 명령어의 콜백 통합을 검증한다."""

    def test_rotate_pdf는_callback을_받는다(self, sample_pdf: Path, tmp_path: Path):
        """rotate_pdf에 callback을 전달할 수 있다."""
        from pdf_tool.commands.rotate import rotate_pdf

        mock = MagicMock()
        output = tmp_path / "rotate_result.pdf"
        rotate_pdf(sample_pdf, angle=90, output=output, callback=mock)
        assert output.exists()
        assert mock.call_count > 0

    def test_rotate_pdf는_callback_없이도_동작한다(self, sample_pdf: Path, tmp_path: Path):
        """하위 호환성: callback 없이도 정상 동작한다."""
        from pdf_tool.commands.rotate import rotate_pdf

        output = tmp_path / "rotate_result.pdf"
        result = rotate_pdf(sample_pdf, angle=90, output=output)
        assert result == output


class TestResizePdfCallback:
    """resize_pdf 명령어의 콜백 통합을 검증한다."""

    def test_resize_pdf는_callback을_받는다(self, sample_pdf: Path, tmp_path: Path):
        """resize_pdf에 callback을 전달할 수 있다."""
        from pdf_tool.commands.resize import resize_pdf

        mock = MagicMock()
        output = tmp_path / "resize_result.pdf"
        resize_pdf(sample_pdf, output=output, size="A4", callback=mock)
        assert output.exists()
        assert mock.call_count > 0

    def test_resize_pdf는_callback_없이도_동작한다(self, sample_pdf: Path, tmp_path: Path):
        """하위 호환성: callback 없이도 정상 동작한다."""
        from pdf_tool.commands.resize import resize_pdf

        output = tmp_path / "resize_result.pdf"
        result = resize_pdf(sample_pdf, output=output, size="A4")
        assert result == output


class TestCompressPdfCallback:
    """compress_pdf 명령어의 콜백 통합을 검증한다."""

    def test_compress_pdf는_callback을_받는다(self, sample_pdf: Path, tmp_path: Path):
        """compress_pdf에 callback을 전달할 수 있다."""
        from pdf_tool.commands.compress import compress_pdf

        mock = MagicMock()
        output = tmp_path / "compress_result.pdf"
        result = compress_pdf(sample_pdf, output=output, callback=mock)
        assert result["output_path"] == output
        assert mock.call_count > 0

    def test_compress_pdf는_callback_없이도_동작한다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """하위 호환성: callback 없이도 정상 동작한다."""
        from pdf_tool.commands.compress import compress_pdf

        output = tmp_path / "compress_result.pdf"
        result = compress_pdf(sample_pdf, output=output)
        assert result["output_path"] == output


class TestWatermarkPdfCallback:
    """watermark_pdf 명령어의 콜백 통합을 검증한다."""

    def test_watermark_pdf는_callback을_받는다(self, sample_pdf: Path, tmp_path: Path):
        """watermark_pdf에 callback을 전달할 수 있다."""
        from pdf_tool.commands.watermark import watermark_pdf

        mock = MagicMock()
        output = tmp_path / "watermark_result.pdf"
        watermark_pdf(
            sample_pdf, output=output, text="DRAFT", callback=mock
        )
        assert output.exists()
        assert mock.call_count > 0

    def test_watermark_pdf는_callback_없이도_동작한다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """하위 호환성: callback 없이도 정상 동작한다."""
        from pdf_tool.commands.watermark import watermark_pdf

        output = tmp_path / "watermark_result.pdf"
        result = watermark_pdf(sample_pdf, output=output, text="DRAFT")
        assert result == output


class TestInfoCallback:
    """info 명령어의 콜백 통합을 검증한다."""

    def test_get_metadata는_callback을_받는다(self, sample_pdf: Path):
        """get_metadata에 callback을 전달할 수 있다."""
        from pdf_tool.commands.info import get_metadata

        mock = MagicMock()
        result = get_metadata(sample_pdf, callback=mock)
        assert "pages" in result
        assert mock.call_count > 0

    def test_get_metadata는_callback_없이도_동작한다(self, sample_pdf: Path):
        """하위 호환성: callback 없이도 정상 동작한다."""
        from pdf_tool.commands.info import get_metadata

        result = get_metadata(sample_pdf)
        assert result["pages"] == 10

    def test_set_metadata는_callback을_받는다(self, sample_pdf: Path, tmp_path: Path):
        """set_metadata에 callback을 전달할 수 있다."""
        from pdf_tool.commands.info import set_metadata

        mock = MagicMock()
        output = tmp_path / "info_result.pdf"
        set_metadata(
            sample_pdf, output=output, title="Test", callback=mock
        )
        assert output.exists()
        assert mock.call_count > 0

    def test_set_metadata는_callback_없이도_동작한다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """하위 호환성: callback 없이도 정상 동작한다."""
        from pdf_tool.commands.info import set_metadata

        output = tmp_path / "info_result.pdf"
        result = set_metadata(sample_pdf, output=output, title="Test")
        assert result == output


# ============================================================================
# R5: 하위 호환성 통합 테스트
# ============================================================================


class TestBackwardCompatibility:
    """모든 명령어가 callback 없이도 기존과 동일하게 동작함을 검증한다."""

    def test_모든_기존_테스트와의_호환성(self, sample_pdf: Path, tmp_path: Path):
        """기존 API 시그니처가 변경 없이 동작한다."""
        from pdf_tool.commands.cut import cut_pdf
        from pdf_tool.commands.merge import merge_pdfs
        from pdf_tool.commands.rotate import rotate_pdf
        from pdf_tool.core.pdf_handler import load_pdf

        # load_pdf: 기존 호출 방식
        reader = load_pdf(sample_pdf)
        assert len(reader.pages) == 10

        # cut_pdf: 기존 호출 방식
        cut_output = tmp_path / "compat_cut.pdf"
        cut_pdf(sample_pdf, pages="1-3", output=cut_output)
        assert cut_output.exists()

        # merge_pdfs: 기존 호출 방식
        merge_output = tmp_path / "compat_merge.pdf"
        merge_pdfs([sample_pdf], output=merge_output)
        assert merge_output.exists()

        # rotate_pdf: 기존 호출 방식
        rotate_output = tmp_path / "compat_rotate.pdf"
        rotate_pdf(sample_pdf, angle=90, output=rotate_output)
        assert rotate_output.exists()


# ============================================================================
# R6: 콜백 예외 안전성 통합 테스트
# ============================================================================


class TestCallbackExceptionSafety:
    """콜백이 예외를 발생시켜도 명령어가 정상 완료됨을 검증한다."""

    def test_cut_pdf는_콜백_에러에도_정상_완료된다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """콜백이 예외를 발생시켜도 cut_pdf는 정상 완료된다."""
        from pdf_tool.commands.cut import cut_pdf

        def bad_callback(current: int, total: int) -> None:
            raise ValueError("콜백 에러")

        output = tmp_path / "safe_cut.pdf"
        result = cut_pdf(sample_pdf, pages="1-3", output=output, callback=bad_callback)
        assert result == output
        assert output.exists()

    def test_merge_pdfs는_콜백_에러에도_정상_완료된다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """콜백이 예외를 발생시켜도 merge_pdfs는 정상 완료된다."""
        from pdf_tool.commands.merge import merge_pdfs

        def bad_callback(current: int, total: int) -> None:
            raise RuntimeError("콜백 에러")

        output = tmp_path / "safe_merge.pdf"
        result = merge_pdfs(
            [sample_pdf], output=output, callback=bad_callback
        )
        assert result == output
        assert output.exists()

    def test_split_pdf는_콜백_에러에도_정상_완료된다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """콜백이 예외를 발생시켜도 split_pdf는 정상 완료된다."""
        from pdf_tool.commands.split import split_pdf

        def bad_callback(current: int, total: int) -> None:
            raise ValueError("콜백 에러")

        results = split_pdf(
            sample_pdf, every=5, output_dir=tmp_path, callback=bad_callback
        )
        assert len(results) == 2

    def test_rotate_pdf는_콜백_에러에도_정상_완료된다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """콜백이 예외를 발생시켜도 rotate_pdf는 정상 완료된다."""
        from pdf_tool.commands.rotate import rotate_pdf

        def bad_callback(current: int, total: int) -> None:
            raise ValueError("콜백 에러")

        output = tmp_path / "safe_rotate.pdf"
        result = rotate_pdf(
            sample_pdf, angle=90, output=output, callback=bad_callback
        )
        assert result == output
        assert output.exists()

    def test_compress_pdf는_콜백_에러에도_정상_완료된다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """콜백이 예외를 발생시켜도 compress_pdf는 정상 완료된다."""
        from pdf_tool.commands.compress import compress_pdf

        def bad_callback(current: int, total: int) -> None:
            raise ValueError("콜백 에러")

        output = tmp_path / "safe_compress.pdf"
        result = compress_pdf(
            sample_pdf, output=output, callback=bad_callback
        )
        assert result["output_path"] == output


class TestCallbackProgressValues:
    """콜백에 전달되는 진행률 값의 정확성을 검증한다."""

    def test_콜백의_current는_0부터_시작한다(self, sample_pdf: Path, tmp_path: Path):
        """첫 번째 콜백 호출 시 current >= 1이다."""
        from pdf_tool.commands.cut import cut_pdf

        calls = []

        def track(current: int, total: int) -> None:
            calls.append((current, total))

        output = tmp_path / "track_cut.pdf"
        cut_pdf(sample_pdf, pages="1-5", output=output, callback=track)
        assert calls[0][0] >= 1

    def test_콜백의_total은_양수이다(self, sample_pdf: Path, tmp_path: Path):
        """콜백의 total 값은 항상 양수이다."""
        from pdf_tool.commands.rotate import rotate_pdf

        calls = []

        def track(current: int, total: int) -> None:
            calls.append((current, total))

        output = tmp_path / "track_rotate.pdf"
        rotate_pdf(sample_pdf, angle=90, output=output, callback=track)
        for _current, total in calls:
            assert total > 0

    def test_콜백의_current는_total을_초과하지_않는다(
        self, sample_pdf: Path, tmp_path: Path
    ):
        """콜백의 current 값은 total을 초과하지 않는다."""
        from pdf_tool.commands.cut import cut_pdf

        calls = []

        def track(current: int, total: int) -> None:
            calls.append((current, total))

        output = tmp_path / "track_bound.pdf"
        cut_pdf(sample_pdf, pages="1-3", output=output, callback=track)
        for current, total in calls:
            assert current <= total

    def test_콜백의_current는_단조_증가한다(self, sample_pdf: Path, tmp_path: Path):
        """콜백의 current 값은 단조 증가한다."""
        from pdf_tool.commands.rotate import rotate_pdf

        calls = []

        def track(current: int, total: int) -> None:
            calls.append((current, total))

        output = tmp_path / "track_mono.pdf"
        rotate_pdf(sample_pdf, angle=90, output=output, callback=track)
        currents = [c for c, t in calls]
        for i in range(1, len(currents)):
            assert currents[i] >= currents[i - 1]
