"""Typer CLI 진입점: 모든 PDF 조작 명령어를 등록하고 공통 옵션을 관리한다."""

import json
from pathlib import Path
from typing import Annotated

import typer
from pypdf import PdfReader

from pdf_tool import __version__
from pdf_tool.commands.compress import compress_pdf
from pdf_tool.commands.cut import cut_pdf
from pdf_tool.commands.info import get_metadata, set_metadata
from pdf_tool.commands.merge import merge_pdfs
from pdf_tool.commands.resize import resize_pdf
from pdf_tool.commands.rotate import rotate_pdf
from pdf_tool.commands.split import split_pdf
from pdf_tool.commands.watermark import watermark_pdf
from pdf_tool.core.exceptions import PDFToolError
from pdf_tool.utils.logging import (
    print_error,
    print_info,
    print_success,
    print_summary,
    print_warning,
)

app = typer.Typer(
    name="pdf-tool",
    help="PDF 조작 도구 (Cut, Merge, Split, Rotate, Resize, Compress, Watermark, Info)",
    add_completion=False,
)


def _version_callback(value: bool) -> None:
    """버전 정보를 출력하고 종료한다."""
    if value:
        typer.echo(f"pdf-tool v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            help="버전 정보를 표시합니다.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """PDF 핵심 조작 도구."""


@app.command()
def cut(
    input_file: Annotated[Path, typer.Argument(help="입력 PDF 파일 경로")],
    pages: Annotated[
        str,
        typer.Option("--pages", "-p", help="추출할 페이지 범위 (예: 1,3,5-10)"),
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="출력 파일 경로"),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="상세 로그 출력")
    ] = False,
) -> None:
    """PDF에서 지정된 페이지를 추출합니다."""
    try:
        if verbose:
            print_info(f"입력 파일: {input_file}")
            print_info(f"페이지 범위: {pages}")

        result = cut_pdf(input_file, pages=pages, output=output)

        reader = PdfReader(result)
        print_success("페이지 추출 완료")
        print_summary(
            "결과 요약",
            {
                "출력 파일": str(result),
                "추출된 페이지 수": str(len(reader.pages)),
            },
        )
    except PDFToolError as e:
        print_error(str(e))
        raise typer.Exit(code=1) from None


@app.command()
def merge(
    input_files: Annotated[
        list[Path], typer.Argument(help="병합할 PDF 파일 경로 목록")
    ],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="출력 파일 경로"),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="상세 로그 출력")
    ] = False,
    use_glob: Annotated[bool, typer.Option("--glob", help="glob 패턴 사용")] = False,
) -> None:
    """여러 PDF 파일을 하나로 병합합니다."""
    try:
        if verbose:
            print_info(f"입력 파일: {len(input_files)}개")

        result = merge_pdfs(input_files, output=output, use_glob=use_glob)

        reader = PdfReader(result)
        print_success("PDF 병합 완료")
        print_summary(
            "결과 요약",
            {
                "출력 파일": str(result),
                "총 페이지 수": str(len(reader.pages)),
            },
        )
    except PDFToolError as e:
        print_error(str(e))
        raise typer.Exit(code=1) from None


@app.command()
def split(
    input_file: Annotated[Path, typer.Argument(help="입력 PDF 파일 경로")],
    every: Annotated[
        int, typer.Option("--every", "-e", help="분할 단위 (페이지 수)")
    ] = 1,
    output_dir: Annotated[
        Path | None,
        typer.Option("--output-dir", "-d", help="출력 디렉토리 경로"),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="상세 로그 출력")
    ] = False,
) -> None:
    """PDF를 페이지별 또는 단위별로 분할합니다."""
    try:
        if verbose:
            print_info(f"입력 파일: {input_file}")
            print_info(f"분할 단위: {every}페이지")

        result_files = split_pdf(input_file, every=every, output_dir=output_dir)

        print_success("PDF 분할 완료")
        print_summary(
            "결과 요약",
            {
                "출력 디렉토리": str(result_files[0].parent) if result_files else "N/A",
                "생성된 파일 수": str(len(result_files)),
            },
        )
    except PDFToolError as e:
        print_error(str(e))
        raise typer.Exit(code=1) from None


@app.command()
def rotate(
    input_file: Annotated[Path, typer.Argument(help="입력 PDF 파일 경로")],
    angle: Annotated[
        int, typer.Option("--angle", "-a", help="회전 각도 (90, 180, 270)")
    ],
    pages: Annotated[
        str | None,
        typer.Option("--pages", "-p", help="회전할 페이지 범위"),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="출력 파일 경로"),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="상세 로그 출력")
    ] = False,
) -> None:
    """PDF 페이지를 시계 방향으로 회전합니다."""
    try:
        if verbose:
            print_info(f"입력 파일: {input_file}")
            print_info(f"회전 각도: {angle}도")

        result = rotate_pdf(input_file, angle=angle, pages=pages, output=output)

        reader = PdfReader(result)
        print_success("페이지 회전 완료")
        print_summary(
            "결과 요약",
            {
                "출력 파일": str(result),
                "총 페이지 수": str(len(reader.pages)),
                "회전 각도": f"{angle}도",
            },
        )
    except PDFToolError as e:
        print_error(str(e))
        raise typer.Exit(code=1) from None


@app.command()
def resize(
    input_file: Annotated[Path, typer.Argument(help="입력 PDF 파일 경로")],
    size: Annotated[
        str | None,
        typer.Option("--size", "-s", help="목표 용지 크기 (A3, A4, A5, Letter, Legal)"),
    ] = None,
    width: Annotated[
        float | None,
        typer.Option("--width", help="커스텀 너비 (mm)"),
    ] = None,
    height: Annotated[
        float | None,
        typer.Option("--height", help="커스텀 높이 (mm)"),
    ] = None,
    mode: Annotated[
        str,
        typer.Option("--mode", "-m", help="리사이즈 모드 (fit, stretch, fill)"),
    ] = "fit",
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="출력 파일 경로"),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="상세 로그 출력")
    ] = False,
) -> None:
    """PDF 페이지 크기를 변경합니다."""
    try:
        if verbose:
            print_info(f"입력 파일: {input_file}")

        result = resize_pdf(
            input_file,
            output=output,
            size=size,
            width_mm=width,
            height_mm=height,
            mode=mode,
        )

        reader = PdfReader(result)
        print_success("페이지 리사이즈 완료")
        print_summary(
            "결과 요약",
            {
                "출력 파일": str(result),
                "총 페이지 수": str(len(reader.pages)),
                "리사이즈 모드": mode,
            },
        )
    except PDFToolError as e:
        print_error(str(e))
        raise typer.Exit(code=1) from None


@app.command()
def compress(
    input_file: Annotated[Path, typer.Argument(help="입력 PDF 파일 경로")],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="출력 파일 경로"),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="상세 로그 출력")
    ] = False,
) -> None:
    """PDF 파일을 압축합니다."""
    try:
        if verbose:
            print_info(f"입력 파일: {input_file}")

        result = compress_pdf(input_file, output=output)

        original_mb = result["original_size"] / (1024 * 1024)
        compressed_mb = result["compressed_size"] / (1024 * 1024)

        if result["reduction_percent"] == 0:
            print_warning("추가 압축 효과가 없습니다")

        print_success("PDF 압축 완료")
        print_summary(
            "결과 요약",
            {
                "출력 파일": str(result["output_path"]),
                "원본 크기": f"{original_mb:.1f}MB",
                "압축 크기": f"{compressed_mb:.1f}MB",
                "절감률": f"{result['reduction_percent']}%",
            },
        )
    except PDFToolError as e:
        print_error(str(e))
        raise typer.Exit(code=1) from None


@app.command()
def watermark(
    input_file: Annotated[Path, typer.Argument(help="입력 PDF 파일 경로")],
    text: Annotated[
        str | None,
        typer.Option("--text", "-t", help="워터마크 텍스트"),
    ] = None,
    image: Annotated[
        Path | None,
        typer.Option("--image", "-i", help="워터마크 이미지 경로"),
    ] = None,
    opacity: Annotated[
        float,
        typer.Option("--opacity", help="투명도 (0.0~1.0)"),
    ] = 0.3,
    rotation: Annotated[
        float,
        typer.Option("--rotation", help="회전 각도 (텍스트 전용)"),
    ] = 45,
    position: Annotated[
        str,
        typer.Option("--position", help="위치 (center, top, bottom)"),
    ] = "center",
    pages: Annotated[
        str | None,
        typer.Option("--pages", "-p", help="적용할 페이지 범위 (예: 1,3,5-10)"),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="출력 파일 경로"),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="상세 로그 출력")
    ] = False,
) -> None:
    """PDF에 워터마크를 적용합니다."""
    try:
        if verbose:
            print_info(f"입력 파일: {input_file}")

        result = watermark_pdf(
            input_file,
            output=output,
            text=text,
            image=image,
            opacity=opacity,
            rotation=rotation,
            position=position,
            pages=pages,
        )

        reader = PdfReader(result)
        wm_type = "텍스트" if text else "이미지"
        print_success("워터마크 적용 완료")
        print_summary(
            "결과 요약",
            {
                "출력 파일": str(result),
                "총 페이지 수": str(len(reader.pages)),
                "워터마크 유형": wm_type,
            },
        )
    except (PDFToolError, FileNotFoundError) as e:
        print_error(str(e))
        raise typer.Exit(code=1) from None


@app.command()
def info(
    input_file: Annotated[Path, typer.Argument(help="입력 PDF 파일 경로")],
    set_title: Annotated[
        str | None,
        typer.Option("--set-title", help="제목 설정"),
    ] = None,
    set_author: Annotated[
        str | None,
        typer.Option("--set-author", help="저자 설정"),
    ] = None,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="JSON 형식으로 출력"),
    ] = False,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="출력 파일 경로 (메타데이터 수정 시)"),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="상세 로그 출력")
    ] = False,
) -> None:
    """PDF 메타데이터를 조회하거나 수정합니다."""
    try:
        if verbose:
            print_info(f"입력 파일: {input_file}")

        # 메타데이터 수정 모드
        if set_title is not None or set_author is not None:
            if output is None:
                from pdf_tool.utils.file_utils import generate_output_filename

                output = generate_output_filename(input_file, "info")

            set_metadata(
                input_file,
                output=output,
                title=set_title,
                author=set_author,
            )
            print_success("메타데이터 수정 완료")
            print_summary(
                "결과 요약",
                {
                    "출력 파일": str(output),
                    **({"제목": set_title} if set_title else {}),
                    **({"저자": set_author} if set_author else {}),
                },
            )
            return

        # 메타데이터 조회 모드
        metadata = get_metadata(input_file)

        if json_output:
            typer.echo(json.dumps(metadata, ensure_ascii=False, indent=2))
        else:
            file_size_kb = metadata["file_size"] / 1024
            print_summary(
                "PDF 메타데이터",
                {
                    "제목": metadata["title"] or "(없음)",
                    "저자": metadata["author"] or "(없음)",
                    "생성 프로그램": metadata["creator"] or "(없음)",
                    "생성일": metadata["creation_date"] or "(없음)",
                    "페이지 수": str(metadata["pages"]),
                    "파일 크기": f"{file_size_kb:.1f}KB",
                },
            )
    except PDFToolError as e:
        print_error(str(e))
        raise typer.Exit(code=1) from None
