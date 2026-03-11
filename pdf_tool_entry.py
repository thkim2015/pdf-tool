"""PyInstaller 진입점: EXE 빌드 시 이 파일을 엔트리포인트로 사용한다."""

from pdf_tool.cli import app

if __name__ == "__main__":
    app()
