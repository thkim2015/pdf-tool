"""워터마크 생성기: ReportLab을 사용하여 텍스트/이미지 워터마크 오버레이 PDF를 생성한다."""

from pathlib import Path

from reportlab.pdfgen import canvas


def create_text_watermark(
    *,
    text: str,
    output_path: Path,
    page_width: float,
    page_height: float,
    opacity: float = 0.3,
    rotation: float = 45,
    position: str = "center",
) -> None:
    """텍스트 워터마크가 포함된 단일 페이지 PDF를 생성한다.

    Args:
        text: 워터마크 텍스트
        output_path: 출력 PDF 경로
        page_width: 페이지 너비 (포인트)
        page_height: 페이지 높이 (포인트)
        opacity: 투명도 (0.0~1.0, 기본값 0.3)
        rotation: 회전 각도 (기본값 45도)
        position: 위치 ("center", "top", "bottom")
    """
    c = canvas.Canvas(str(output_path), pagesize=(page_width, page_height))

    # 투명도 설정
    c.saveState()
    c.setFillAlpha(opacity)

    # 폰트 크기를 페이지 너비 기반으로 자동 조정
    font_size = min(page_width, page_height) / 6
    c.setFont("Helvetica", font_size)
    c.setFillColorRGB(0.5, 0.5, 0.5)

    # 위치 계산
    x, y = _calculate_text_position(
        position, page_width, page_height, font_size
    )

    # 회전 및 텍스트 그리기
    c.translate(x, y)
    c.rotate(rotation)
    c.drawCentredString(0, 0, text)

    c.restoreState()
    c.save()


def create_image_watermark(
    *,
    image_path: Path,
    output_path: Path,
    page_width: float,
    page_height: float,
    opacity: float = 0.3,
    position: str = "center",
) -> None:
    """이미지 워터마크가 포함된 단일 페이지 PDF를 생성한다.

    Args:
        image_path: 워터마크 이미지 경로
        output_path: 출력 PDF 경로
        page_width: 페이지 너비 (포인트)
        page_height: 페이지 높이 (포인트)
        opacity: 투명도 (0.0~1.0, 기본값 0.3)
        position: 위치 ("center", "top", "bottom")

    Raises:
        FileNotFoundError: 이미지 파일이 존재하지 않을 때
    """
    if not image_path.is_file():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: '{image_path}'")

    from PIL import Image

    img = Image.open(image_path)
    img_width, img_height = img.size

    # 이미지를 페이지 크기의 1/3로 스케일링
    scale = min(page_width / 3 / img_width, page_height / 3 / img_height)
    draw_width = img_width * scale
    draw_height = img_height * scale

    # 위치 계산
    x, y = _calculate_image_position(
        position, page_width, page_height, draw_width, draw_height
    )

    c = canvas.Canvas(str(output_path), pagesize=(page_width, page_height))
    c.saveState()
    c.setFillAlpha(opacity)

    # ReportLab에 이미지 그리기
    c.drawImage(
        str(image_path),
        x,
        y,
        width=draw_width,
        height=draw_height,
        mask="auto",
    )

    c.restoreState()
    c.save()


def _calculate_text_position(
    position: str,
    page_width: float,
    page_height: float,
    font_size: float,
) -> tuple[float, float]:
    """텍스트 워터마크의 위치를 계산한다."""
    x = page_width / 2

    if position == "top":
        y = page_height - font_size * 2
    elif position == "bottom":
        y = font_size * 2
    else:  # center
        y = page_height / 2

    return x, y


def _calculate_image_position(
    position: str,
    page_width: float,
    page_height: float,
    draw_width: float,
    draw_height: float,
) -> tuple[float, float]:
    """이미지 워터마크의 위치를 계산한다."""
    x = (page_width - draw_width) / 2

    if position == "top":
        y = page_height - draw_height - 50
    elif position == "bottom":
        y = 50
    else:  # center
        y = (page_height - draw_height) / 2

    return x, y
