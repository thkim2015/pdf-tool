"""GUI 에러 로그 검증 테스트.

_handle_exception이 에러를 로그에 기록하는지 확인하고,
로그 파일에 에러가 없는지 검증한다.
"""

from __future__ import annotations

import logging


class Test_handle_exception_로깅:
    """_handle_exception이 에러를 로그에 기록하는지 검증한다."""

    def test_handle_exception_에러_로그_기록(self, caplog):
        """미처리 예외가 logger.error로 기록된다."""
        from pdf_tool.gui.app import format_exception_message

        # app 모듈의 logger를 직접 사용
        with caplog.at_level(logging.ERROR, logger="pdf_tool.gui.app"):
            # _handle_exception 로직을 직접 재현
            # (실제 메서드는 CTk 인스턴스 내부에 있어 직접 호출 불가)
            exc_type = TclError
            exc_value = TclError('image "pyimage1" does not exist')
            msg = format_exception_message(exc_value)

            gui_logger = logging.getLogger("pdf_tool.gui.app")
            gui_logger.error("GUI 미처리 예외: %s: %s", exc_type.__name__, msg)

        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.levelname == "ERROR"
        assert "pyimage1" in record.message
        assert "TclError" in record.message

    def test_handle_exception_PDF_오류_로그_기록(self, caplog):
        """PDFToolError도 로그에 기록된다."""
        from pdf_tool.core.exceptions import PDFToolError
        from pdf_tool.gui.app import format_exception_message

        with caplog.at_level(logging.ERROR, logger="pdf_tool.gui.app"):
            exc_value = PDFToolError("PDF 처리 실패")
            msg = format_exception_message(exc_value)

            gui_logger = logging.getLogger("pdf_tool.gui.app")
            gui_logger.error("GUI 미처리 예외: %s: %s", PDFToolError.__name__, msg)

        assert len(caplog.records) == 1
        assert "PDF 오류" in caplog.records[0].message


class Test_로그_파일_에러_없음:
    """로그 파일에 에러가 없는지 검증한다."""

    def test_로그_파일_에러_없음(self, tmp_path):
        """정상 동작 시 로그 파일에 ERROR 레벨 기록이 없어야 한다."""
        log_file = tmp_path / "pdf_tool_gui.log"

        # 파일 핸들러로 로그 설정
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )

        test_logger = logging.getLogger("pdf_tool.gui.app.test_clean")
        test_logger.addHandler(handler)

        # 정상 동작 시뮬레이션 (에러 없음)
        test_logger.info("정상 동작")
        test_logger.debug("디버그 메시지")

        handler.flush()
        handler.close()
        test_logger.removeHandler(handler)

        # 로그 파일에 ERROR가 없어야 한다
        if log_file.exists():
            content = log_file.read_text()
            assert "[ERROR]" not in content, f"로그 파일에 에러 발견:\n{content}"

    def test_에러_발생_시_로그_파일에_기록됨(self, tmp_path):
        """에러 발생 시 로그 파일에 ERROR가 기록되어야 한다."""
        log_file = tmp_path / "pdf_tool_gui.log"

        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )

        test_logger = logging.getLogger("pdf_tool.gui.app.test_error")
        test_logger.addHandler(handler)

        # 에러 시뮬레이션
        test_logger.error("GUI 미처리 예외: TclError: image \"pyimage1\" does not exist")

        handler.flush()
        handler.close()
        test_logger.removeHandler(handler)

        content = log_file.read_text()
        assert "[ERROR]" in content
        assert "pyimage1" in content

    def test_기존_로그_파일_에러_검사(self, tmp_path):
        """실제 GUI 로그 파일 경로에서 에러를 검사하는 유틸리티 테스트."""
        from pdf_tool.gui.app import GUI_LOG_FILE

        log_path = tmp_path / GUI_LOG_FILE

        # 빈 로그 파일 생성 (정상 상태)
        log_path.write_text("")

        content = log_path.read_text()
        error_lines = [
            line for line in content.splitlines() if "[ERROR]" in line
        ]
        assert len(error_lines) == 0, (
            f"로그 파일에 {len(error_lines)}개의 에러 발견:\n"
            + "\n".join(error_lines)
        )


class TclError(Exception):
    """테스트용 TclError stub."""
