"""Windows EXE 빌드 스크립트: PyInstaller를 사용하여 단일 실행 파일을 생성한다."""

import argparse
import subprocess
import sys
from pathlib import Path


def _build_cli_cmd(root: Path) -> list[str]:
    """CLI 모드 빌드 명령어를 생성한다."""
    return [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name", "pdf-tool",
        "--paths", str(root / "src"),
        # 불필요한 모듈 제외
        "--exclude-module", "tkinter",
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "scipy",
        "--exclude-module", "pandas",
        "--exclude-module", "test",
        "--exclude-module", "unittest",
        "--exclude-module", "pytest",
        # 숨겨진 임포트 추가
        "--hidden-import", "pypdf",
        "--hidden-import", "typer",
        "--hidden-import", "typer.core",
        "--hidden-import", "typer.main",
        "--hidden-import", "click",
        "--hidden-import", "rich",
        "--hidden-import", "rich.console",
        "--hidden-import", "rich.table",
        "--hidden-import", "reportlab",
        "--hidden-import", "reportlab.pdfgen",
        "--hidden-import", "reportlab.pdfgen.canvas",
        "--hidden-import", "reportlab.lib.pagesizes",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.Image",
        str(root / "pdf_tool_entry.py"),
    ]


def _build_gui_cmd(root: Path) -> list[str]:
    """GUI 모드 빌드 명령어를 생성한다."""
    return [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "pdf-tool-gui",
        "--paths", str(root / "src"),
        # customtkinter 리소스 수집
        "--collect-all", "customtkinter",
        # 불필요한 모듈 제외
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "scipy",
        "--exclude-module", "pandas",
        "--exclude-module", "test",
        "--exclude-module", "unittest",
        "--exclude-module", "pytest",
        # 숨겨진 임포트 추가
        "--hidden-import", "pypdf",
        "--hidden-import", "customtkinter",
        "--hidden-import", "reportlab",
        "--hidden-import", "reportlab.pdfgen",
        "--hidden-import", "reportlab.pdfgen.canvas",
        "--hidden-import", "reportlab.lib.pagesizes",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "pypdfium2",
        "--hidden-import", "darkdetect",
        "--hidden-import", "tkinterdnd2",
        str(root / "pdf_tool_gui_entry.py"),
    ]


def build(mode: str = "cli"):
    """pdf-tool EXE를 빌드한다.

    Args:
        mode: 빌드 모드 ("cli" 또는 "gui")
    """
    root = Path(__file__).parent

    if mode == "gui":
        # GUI 엔트리 포인트 파일 생성 (존재하지 않을 경우)
        gui_entry = root / "pdf_tool_gui_entry.py"
        if not gui_entry.exists():
            gui_entry.write_text(
                "from pdf_tool.gui.app import main\n\nmain()\n",
                encoding="utf-8",
            )
        cmd = _build_gui_cmd(root)
        build_name = "pdf-tool-gui"
    else:
        cmd = _build_cli_cmd(root)
        build_name = "pdf-tool"

    print(f"Build starting ({mode} mode)...")
    print(f"Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(root))

    if result.returncode == 0:
        exe_ext = ".exe" if sys.platform == "win32" else ""
        exe_path = root / "dist" / f"{build_name}{exe_ext}"
        print(f"\nBuild complete: {exe_path}")
        if exe_path.exists():
            print(f"File size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
    else:
        print("\nBuild failed!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Tool 빌드 스크립트")
    parser.add_argument(
        "--mode",
        choices=["cli", "gui"],
        default="cli",
        help="빌드 모드: cli (기본값) 또는 gui",
    )
    args = parser.parse_args()
    build(mode=args.mode)
