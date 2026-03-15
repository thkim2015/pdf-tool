"""메타데이터 조회/수정 명령어: PDF 파일의 메타데이터를 조회하거나 수정한다."""

from pathlib import Path

from pypdf import PdfWriter

from pdf_tool.core.pdf_handler import load_pdf
from pdf_tool.core.progress import ProgressCallback, safe_callback
from pdf_tool.core.validators import validate_output_path


def get_metadata(
    input_path: Path,
    *,
    callback: ProgressCallback = None,
) -> dict:
    """PDF 파일의 메타데이터를 딕셔너리로 반환한다.

    Args:
        input_path: PDF 파일 경로
        callback: 진행 상황 콜백 (current, total)

    Returns:
        메타데이터 딕셔너리 (title, author, creator, creation_date, pages, file_size)

    Raises:
        FileValidationError: 파일이 존재하지 않거나 유효하지 않을 때
    """
    reader = load_pdf(input_path)
    meta = reader.metadata

    safe_callback(callback, 1, 2)

    file_size = input_path.stat().st_size

    result = {
        "title": (meta.title if meta and meta.title else "") or "",
        "author": (meta.author if meta and meta.author else "") or "",
        "creator": (meta.creator if meta and meta.creator else "") or "",
        "creation_date": str(meta.creation_date) if meta and meta.creation_date else "",
        "pages": len(reader.pages),
        "file_size": file_size,
    }

    safe_callback(callback, 2, 2)
    return result


def set_metadata(
    input_path: Path,
    *,
    output: Path,
    title: str | None = None,
    author: str | None = None,
    callback: ProgressCallback = None,
) -> Path:
    """PDF 파일의 메타데이터를 수정한다.

    Args:
        input_path: 입력 PDF 파일 경로
        output: 출력 파일 경로
        title: 새 제목 (None이면 변경하지 않음)
        author: 새 저자 (None이면 변경하지 않음)
        callback: 진행 상황 콜백 (current, total)

    Returns:
        출력 파일 경로

    Raises:
        FileValidationError: 파일이 존재하지 않거나 유효하지 않을 때
    """
    reader = load_pdf(input_path)
    validate_output_path(output)

    total_pages = len(reader.pages)
    writer = PdfWriter()

    # 모든 페이지 복사
    for i, page in enumerate(reader.pages):
        writer.add_page(page)
        safe_callback(callback, i + 1, total_pages)

    # 기존 메타데이터 복사
    if reader.metadata:
        writer.add_metadata(
            {
                key: value
                for key, value in reader.metadata.items()
                if value is not None
            }
        )

    # 새 메타데이터 설정
    new_meta: dict[str, str] = {}
    if title is not None:
        new_meta["/Title"] = title
    if author is not None:
        new_meta["/Author"] = author

    if new_meta:
        writer.add_metadata(new_meta)

    with open(output, "wb") as f:
        writer.write(f)

    return output
