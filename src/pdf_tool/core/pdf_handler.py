"""PDF I/O 유틸리티: PDF 파일 읽기 및 쓰기 공통 기능을 제공한다."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_tool.core.progress import ProgressCallback
from pdf_tool.core.validators import validate_output_path, validate_pdf_file


def load_pdf(
    path: Path,
    *,
    callback: ProgressCallback = None,
) -> PdfReader:
    """PDF 파일을 읽어 PdfReader 객체를 반환한다.

    Args:
        path: PDF 파일 경로
        callback: 진행 상황 콜백 (current, total)

    Returns:
        PdfReader 인스턴스

    Raises:
        FileValidationError: 파일이 존재하지 않거나 유효하지 않을 때
    """
    validate_pdf_file(path)
    return PdfReader(path)


def save_pdf(writer: PdfWriter, path: Path) -> None:
    """PdfWriter의 내용을 파일로 저장한다.

    Args:
        writer: 저장할 PdfWriter 인스턴스
        path: 출력 파일 경로

    Raises:
        FileValidationError: 출력 경로가 유효하지 않을 때
    """
    validate_output_path(path)
    with open(path, "wb") as f:
        writer.write(f)
