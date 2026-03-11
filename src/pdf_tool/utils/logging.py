"""Rich 기반 로깅 설정: 터미널 출력 포맷팅을 제공한다."""

from rich.console import Console

# 전역 콘솔 인스턴스
console = Console()
err_console = Console(stderr=True)


def print_success(message: str) -> None:
    """성공 메시지를 출력한다."""
    console.print(f"[green][완료][/green] {message}")


def print_error(message: str) -> None:
    """에러 메시지를 출력한다."""
    err_console.print(f"[red][에러][/red] {message}")


def print_warning(message: str) -> None:
    """경고 메시지를 출력한다."""
    err_console.print(f"[yellow][경고][/yellow] {message}")


def print_info(message: str) -> None:
    """정보 메시지를 출력한다."""
    console.print(f"[blue][정보][/blue] {message}")


def print_summary(title: str, details: dict[str, str]) -> None:
    """작업 결과 요약을 출력한다."""
    console.print(f"\n[bold]{title}[/bold]")
    for key, value in details.items():
        console.print(f"  {key}: {value}")
