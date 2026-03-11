"""파일 경로 유틸리티: 출력 파일명 자동 생성 등의 기능을 제공한다."""

from pathlib import Path

# 명령어별 출력 파일명 접미사 매핑
_SUFFIX_MAP = {
    "cut": "_cut",
    "merge": "_merged",
    "split": "_{num:03d}",
    "rotate": "_rotated",
    "resize": "_resized",
    "compress": "_compressed",
    "watermark": "_watermarked",
    "info": "_updated",
}


def generate_output_filename(input_path: Path, command: str) -> Path:
    """입력 파일명과 명령어에 기반하여 출력 파일명을 자동 생성한다.

    Args:
        input_path: 입력 PDF 파일 경로
        command: 실행 명령어 (cut, merge, split, rotate)

    Returns:
        자동 생성된 출력 파일 경로
    """
    stem = input_path.stem
    suffix = input_path.suffix  # .pdf
    parent = input_path.parent

    name_suffix = _SUFFIX_MAP.get(command, f"_{command}")
    return parent / f"{stem}{name_suffix}{suffix}"
