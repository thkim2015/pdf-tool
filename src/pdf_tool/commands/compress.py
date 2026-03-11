"""PDF 압축 명령어: 콘텐츠 스트림 압축 및 동일 객체 병합으로 파일 크기를 줄인다."""

from pathlib import Path

from pypdf import PdfWriter

from pdf_tool.core.pdf_handler import load_pdf
from pdf_tool.core.validators import validate_output_path
from pdf_tool.utils.file_utils import generate_output_filename


def compress_pdf(
    input_path: Path,
    *,
    output: Path | None = None,
) -> dict:
    """PDF 파일을 압축하여 파일 크기를 줄인다.

    Args:
        input_path: 입력 PDF 파일 경로
        output: 출력 파일 경로 (None이면 자동 생성)

    Returns:
        압축 결과 딕셔너리:
            - output_path: 출력 파일 경로
            - original_size: 원본 파일 크기 (바이트)
            - compressed_size: 압축 파일 크기 (바이트)
            - reduction_percent: 절감률 (%)

    Raises:
        FileValidationError: 파일이 존재하지 않거나 유효하지 않을 때
    """
    reader = load_pdf(input_path)
    original_size = input_path.stat().st_size

    if output is None:
        output = generate_output_filename(input_path, "compress")

    validate_output_path(output)

    writer = PdfWriter()

    # 모든 페이지 복사
    for page in reader.pages:
        writer.add_page(page)

    # 메타데이터 복사
    if reader.metadata:
        writer.add_metadata(
            {k: v for k, v in reader.metadata.items() if v is not None}
        )

    # 콘텐츠 스트림 압축
    for page in writer.pages:
        page.compress_content_streams()

    # 동일 객체 병합
    writer.compress_identical_objects()

    with open(output, "wb") as f:
        writer.write(f)

    compressed_size = output.stat().st_size

    # 절감률 계산
    if original_size > 0:
        reduction_percent = round(
            (1 - compressed_size / original_size) * 100, 1
        )
    else:
        reduction_percent = 0.0

    return {
        "output_path": output,
        "original_size": original_size,
        "compressed_size": compressed_size,
        "reduction_percent": max(0, reduction_percent),
    }
