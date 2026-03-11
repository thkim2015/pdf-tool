"""validators 모듈의 명세 테스트."""

from pathlib import Path

import pytest

from pdf_tool.core.exceptions import FileValidationError
from pdf_tool.core.validators import validate_output_path, validate_pdf_file


class TestValidatePdfFile:
    """PDF 파일 유효성 검증을 테스트한다."""

    def test_유효한_PDF_파일을_통과시킨다(self, sample_pdf: Path):
        """유효한 PDF 파일은 에러 없이 통과한다."""
        # 예외 없이 정상 종료되어야 한다
        validate_pdf_file(sample_pdf)

    def test_존재하지_않는_파일에_에러를_발생시킨다(self, tmp_path: Path):
        """존재하지 않는 파일은 FileValidationError를 발생시킨다."""
        nonexistent = tmp_path / "nonexistent.pdf"
        with pytest.raises(FileValidationError, match="파일을 찾을 수 없습니다"):
            validate_pdf_file(nonexistent)

    def test_유효하지_않은_PDF에_에러를_발생시킨다(self, invalid_pdf: Path):
        """유효하지 않은 PDF 파일은 FileValidationError를 발생시킨다."""
        with pytest.raises(FileValidationError, match="유효한 PDF 파일이 아닙니다"):
            validate_pdf_file(invalid_pdf)

    def test_디렉토리_경로에_에러를_발생시킨다(self, tmp_path: Path):
        """디렉토리 경로는 파일이 아니므로 에러를 발생시킨다."""
        with pytest.raises(FileValidationError, match="파일을 찾을 수 없습니다"):
            validate_pdf_file(tmp_path)


class TestValidateOutputPath:
    """출력 경로 검증을 테스트한다."""

    def test_유효한_출력_경로를_통과시킨다(self, tmp_path: Path):
        """존재하는 디렉토리에 대한 출력 경로는 통과한다."""
        output = tmp_path / "output.pdf"
        validate_output_path(output)

    def test_존재하지_않는_디렉토리에_에러를_발생시킨다(self, tmp_path: Path):
        """부모 디렉토리가 존재하지 않으면 에러를 발생시킨다."""
        output = tmp_path / "nonexistent_dir" / "output.pdf"
        with pytest.raises(FileValidationError, match="출력 디렉토리"):
            validate_output_path(output)
