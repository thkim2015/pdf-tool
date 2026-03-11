"""Windows EXE 빌드 스크립트: PyInstaller를 사용하여 단일 실행 파일을 생성한다."""

import subprocess
import sys
from pathlib import Path


def build():
    """pdf-tool EXE를 빌드한다."""
    root = Path(__file__).parent

    cmd = [
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

    print("빌드 시작...")
    print(f"명령어: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(root))

    if result.returncode == 0:
        exe_ext = ".exe" if sys.platform == "win32" else ""
        exe_path = root / "dist" / f"pdf-tool{exe_ext}"
        print(f"\n빌드 완료: {exe_path}")
        print(f"파일 크기: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
    else:
        print("\n빌드 실패!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    build()
