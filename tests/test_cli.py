"""CLI 통합 테스트: Typer 앱의 전체 명령어를 검증한다."""

from pathlib import Path

from pypdf import PdfReader
from typer.testing import CliRunner

from pdf_tool.cli import app

runner = CliRunner()


class TestCliVersion:
    """버전 명령을 검증한다."""

    def test_버전_출력(self):
        """--version 옵션으로 버전을 출력한다."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "pdf-tool v" in result.output


class TestCliCut:
    """cut 명령의 CLI 통합을 검증한다."""

    def test_정상_페이지_추출(self, sample_pdf: Path, tmp_path: Path):
        """CLI로 페이지를 추출한다."""
        output = tmp_path / "result.pdf"
        result = runner.invoke(
            app, ["cut", str(sample_pdf), "--pages", "1-3", "--output", str(output)]
        )
        assert result.exit_code == 0
        assert "완료" in result.output
        assert output.exists()

    def test_verbose_옵션(self, sample_pdf: Path, tmp_path: Path):
        """--verbose 옵션으로 상세 로그를 출력한다."""
        output = tmp_path / "result.pdf"
        result = runner.invoke(
            app,
            [
                "cut",
                str(sample_pdf),
                "--pages",
                "1",
                "--output",
                str(output),
                "--verbose",
            ],
        )
        assert result.exit_code == 0

    def test_존재하지_않는_파일_에러(self, tmp_path: Path):
        """존재하지 않는 파일 입력 시 에러 코드 1을 반환한다."""
        result = runner.invoke(
            app,
            ["cut", str(tmp_path / "no.pdf"), "--pages", "1"],
        )
        assert result.exit_code == 1

    def test_페이지_범위_초과_에러(self, five_page_pdf: Path, tmp_path: Path):
        """페이지 범위 초과 시 에러 코드 1을 반환한다."""
        result = runner.invoke(
            app,
            [
                "cut",
                str(five_page_pdf),
                "--pages",
                "3-10",
                "--output",
                str(tmp_path / "out.pdf"),
            ],
        )
        assert result.exit_code == 1


class TestCliMerge:
    """merge 명령의 CLI 통합을 검증한다."""

    def test_정상_병합(self, create_pdf, tmp_path: Path):
        """CLI로 파일을 병합한다."""
        a = create_pdf("a.pdf", 3)
        b = create_pdf("b.pdf", 2)
        output = tmp_path / "merged.pdf"
        result = runner.invoke(
            app,
            ["merge", str(a), str(b), "--output", str(output)],
        )
        assert result.exit_code == 0
        assert "완료" in result.output
        reader = PdfReader(output)
        assert len(reader.pages) == 5

    def test_존재하지_않는_파일_에러(self, create_pdf, tmp_path: Path):
        """존재하지 않는 파일 포함 시 에러를 반환한다."""
        a = create_pdf("a.pdf", 3)
        result = runner.invoke(
            app,
            ["merge", str(a), str(tmp_path / "missing.pdf")],
        )
        assert result.exit_code == 1


class TestCliSplit:
    """split 명령의 CLI 통합을 검증한다."""

    def test_페이지별_분할(self, five_page_pdf: Path, tmp_path: Path):
        """CLI로 페이지별 분할한다."""
        output_dir = tmp_path / "pages"
        result = runner.invoke(
            app,
            ["split", str(five_page_pdf), "--output-dir", str(output_dir)],
        )
        assert result.exit_code == 0
        assert "완료" in result.output

    def test_단위별_분할(self, twelve_page_pdf: Path, tmp_path: Path):
        """CLI로 단위별 분할한다."""
        output_dir = tmp_path / "parts"
        result = runner.invoke(
            app,
            [
                "split",
                str(twelve_page_pdf),
                "--every",
                "5",
                "--output-dir",
                str(output_dir),
            ],
        )
        assert result.exit_code == 0


class TestCliRotate:
    """rotate 명령의 CLI 통합을 검증한다."""

    def test_전체_회전(self, five_page_pdf: Path, tmp_path: Path):
        """CLI로 전체 페이지를 회전한다."""
        output = tmp_path / "rotated.pdf"
        result = runner.invoke(
            app,
            [
                "rotate",
                str(five_page_pdf),
                "--angle",
                "90",
                "--output",
                str(output),
            ],
        )
        assert result.exit_code == 0
        assert "완료" in result.output

    def test_특정_페이지_회전(self, five_page_pdf: Path, tmp_path: Path):
        """CLI로 특정 페이지만 회전한다."""
        output = tmp_path / "rotated.pdf"
        result = runner.invoke(
            app,
            [
                "rotate",
                str(five_page_pdf),
                "--angle",
                "180",
                "--pages",
                "2,4",
                "--output",
                str(output),
            ],
        )
        assert result.exit_code == 0

    def test_잘못된_각도_에러(self, five_page_pdf: Path, tmp_path: Path):
        """지원하지 않는 각도 입력 시 에러를 반환한다."""
        result = runner.invoke(
            app,
            [
                "rotate",
                str(five_page_pdf),
                "--angle",
                "45",
                "--output",
                str(tmp_path / "out.pdf"),
            ],
        )
        assert result.exit_code == 1
