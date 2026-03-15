"""PDF 리사이즈 명령어: 페이지 크기 변경 및 DPI 리사이즈를 수행한다."""

from pathlib import Path

from pypdf import PdfWriter, Transformation

from pdf_tool.core.exceptions import PDFProcessingError
from pdf_tool.core.page_sizes import get_paper_size, get_supported_sizes, mm_to_points
from pdf_tool.core.pdf_handler import load_pdf
from pdf_tool.core.progress import ProgressCallback, safe_callback
from pdf_tool.core.validators import validate_output_path
from pdf_tool.utils.file_utils import generate_output_filename


def resize_pdf(
    input_path: Path,
    *,
    output: Path | None = None,
    size: str | None = None,
    width_mm: float | None = None,
    height_mm: float | None = None,
    mode: str = "fit",
    callback: ProgressCallback = None,
) -> Path:
    """PDF 페이지 크기를 변경한다.

    Args:
        input_path: 입력 PDF 파일 경로
        output: 출력 파일 경로 (None이면 자동 생성)
        size: 표준 용지 크기 이름 (예: "A4", "Letter")
        width_mm: 커스텀 너비 (mm)
        height_mm: 커스텀 높이 (mm)
        mode: 리사이즈 모드 ("fit", "stretch", "fill")
        callback: 진행 상황 콜백 (current, total)

    Returns:
        출력 파일 경로

    Raises:
        FileValidationError: 파일이 존재하지 않거나 유효하지 않을 때
        PDFProcessingError: 리사이즈 처리 중 에러
    """
    reader = load_pdf(input_path)

    # 목표 크기 결정
    target_width, target_height = _resolve_target_size(
        size=size, width_mm=width_mm, height_mm=height_mm
    )

    if output is None:
        output = generate_output_filename(input_path, "resize")

    validate_output_path(output)

    total_pages = len(reader.pages)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        _resize_page(writer, page, target_width, target_height, mode)
        safe_callback(callback, i + 1, total_pages)

    # 메타데이터 복사
    if reader.metadata:
        writer.add_metadata(
            {k: v for k, v in reader.metadata.items() if v is not None}
        )

    with open(output, "wb") as f:
        writer.write(f)

    return output


def _resolve_target_size(
    *,
    size: str | None,
    width_mm: float | None,
    height_mm: float | None,
) -> tuple[float, float]:
    """목표 페이지 크기를 포인트 단위로 결정한다."""
    if size is not None:
        paper = get_paper_size(size)
        if paper is None:
            supported = ", ".join(get_supported_sizes())
            raise PDFProcessingError(
                f"지원되지 않는 크기: {size}. 지원 목록: {supported}"
            )
        return paper

    if width_mm is not None and height_mm is not None:
        return mm_to_points(width_mm), mm_to_points(height_mm)

    raise PDFProcessingError(
        "크기를 지정해야 합니다: --size 또는 --width/--height 사용"
    )


def _resize_page(
    writer: PdfWriter,
    page,
    target_width: float,
    target_height: float,
    mode: str,
) -> None:
    """단일 페이지를 목표 크기로 리사이즈한다."""
    current_width = float(page.mediabox.width)
    current_height = float(page.mediabox.height)

    # 스케일 계산
    scale_x = target_width / current_width
    scale_y = target_height / current_height

    if mode == "fit":
        # 비율 유지 - 작은 쪽에 맞춤
        scale = min(scale_x, scale_y)
        sx, sy = scale, scale
    elif mode == "stretch":
        # 비율 무시 - 목표 크기에 강제 맞춤
        sx, sy = scale_x, scale_y
    elif mode == "fill":
        # 비율 유지 - 큰 쪽에 맞춤 (잘릴 수 있음)
        scale = max(scale_x, scale_y)
        sx, sy = scale, scale
    else:
        sx, sy = min(scale_x, scale_y), min(scale_x, scale_y)

    # fit/fill 모드에서 콘텐츠 중앙 정렬을 위한 오프셋
    tx = (target_width - current_width * sx) / 2
    ty = (target_height - current_height * sy) / 2

    # 변환 적용
    page.add_transformation(Transformation().scale(sx, sy).translate(tx / sx, ty / sy))

    # MediaBox를 목표 크기로 설정
    page.mediabox.lower_left = (0, 0)
    page.mediabox.upper_right = (target_width, target_height)

    writer.add_page(page)
