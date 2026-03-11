"""PDF 도구 사용자 정의 예외 클래스."""


class PDFToolError(Exception):
    """PDF 도구 기본 예외."""


class FileValidationError(PDFToolError):
    """파일 관련 검증 에러."""


class PageRangeError(PDFToolError):
    """페이지 범위 관련 에러."""


class PDFProcessingError(PDFToolError):
    """PDF 처리 중 발생하는 에러."""
