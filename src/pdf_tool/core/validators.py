"""입력 검증 함수: PDF 파일 및 출력 경로의 유효성을 검사한다."""

from pathlib import Path

from pypdf import PdfReader

from pdf_tool.core.exceptions import FileValidationError


def validate_pdf_file(path: Path) -> None:
    """PDF 파일이 존재하고 유효한지 검증한다.

    Args:
        path: 검증할 PDF 파일 경로

    Raises:
        FileValidationError: 파일이 존재하지 않거나 유효하지 않을 때
    """
    if not path.is_file():
        raise FileValidationError(f"'{path}' 파일을 찾을 수 없습니다")

    try:
        PdfReader(path)
    except Exception as exc:
        raise FileValidationError(f"'{path}'는 유효한 PDF 파일이 아닙니다") from exc


def validate_output_path(path: Path) -> None:
    """출력 경로의 부모 디렉토리가 존재하는지 검증한다.

    Args:
        path: 검증할 출력 파일 경로

    Raises:
        FileValidationError: 부모 디렉토리가 존재하지 않을 때
    """
    parent = path.parent
    if not parent.exists():
        raise FileValidationError(f"출력 디렉토리가 존재하지 않습니다: '{parent}'")
