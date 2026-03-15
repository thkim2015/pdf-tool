"""접근성 모듈.

키보드 네비게이션, 접근성 레이블, 포커스 관리,
고대비 모드를 위한 순수 로직을 제공한다.
"""

from __future__ import annotations

import logging
from collections.abc import Callable

from pdf_tool.gui.constants import NAV_BUTTONS

logger = logging.getLogger(__name__)

# ============================================================================
# Task 5.1: 키보드 네비게이션 상수
# ============================================================================

TAB_KEY = "<Tab>"
SHIFT_TAB_KEY = "<Shift-Tab>"
ENTER_KEY = "<Return>"
SPACE_KEY = "<space>"
ESCAPE_KEY = "<Escape>"


# ============================================================================
# Task 5.1: 포커스 순서 관리
# ============================================================================


class FocusManager:
    """위젯의 포커스 순서를 관리한다.

    Tab/Shift-Tab으로 순환하는 포커스 체인을 구현한다.
    """

    def __init__(self) -> None:
        self.focus_order: list[object] = []
        self.current_index: int = -1

    def register(self, widget: object) -> None:
        """위젯을 포커스 순서에 등록한다.

        Args:
            widget: 포커스 가능한 위젯
        """
        self.focus_order.append(widget)

    def clear(self) -> None:
        """포커스 순서를 초기화한다."""
        self.focus_order.clear()
        self.current_index = -1

    def focus_next(self) -> object | None:
        """다음 위젯으로 포커스를 이동한다.

        마지막 요소에서 호출하면 첫 요소로 순환한다.

        Returns:
            다음 포커스 대상 위젯, 빈 리스트이면 None
        """
        if not self.focus_order:
            return None

        self.current_index = (self.current_index + 1) % len(self.focus_order)
        return self.focus_order[self.current_index]

    def focus_prev(self) -> object | None:
        """이전 위젯으로 포커스를 이동한다.

        첫 요소에서 호출하면 마지막 요소로 순환한다.

        Returns:
            이전 포커스 대상 위젯, 빈 리스트이면 None
        """
        if not self.focus_order:
            return None

        self.current_index = (self.current_index - 1) % len(self.focus_order)
        return self.focus_order[self.current_index]


# ============================================================================
# Task 5.1: 플랫폼별 키보드 단축키
# ============================================================================


def get_page_shortcut_keys(platform: str) -> dict[int, str]:
    """플랫폼에 따른 페이지 전환 단축키 매핑을 반환한다.

    Args:
        platform: 플랫폼 문자열 ("darwin", "win32", "linux")

    Returns:
        {1: "<Command-Key-1>", ...} 형태의 딕셔너리
    """
    modifier = "Command" if platform == "darwin" else "Control"
    return {i: f"<{modifier}-Key-{i}>" for i in range(1, 10)}


def get_page_for_shortcut(index: int) -> str | None:
    """단축키 인덱스(1~9)에 해당하는 페이지 이름을 반환한다.

    Args:
        index: 1부터 시작하는 페이지 인덱스

    Returns:
        페이지 이름, 범위 밖이면 None
    """
    if 1 <= index <= len(NAV_BUTTONS):
        return NAV_BUTTONS[index - 1]
    return None


# ============================================================================
# Task 5.2: 접근성 레이블 레지스트리
# ============================================================================


class AccessibilityLabelRegistry:
    """위젯의 접근성 레이블을 관리한다."""

    def __init__(self) -> None:
        self._labels: dict[int, tuple[object, str]] = {}

    def register(self, widget: object, label: str) -> None:
        """위젯에 접근성 레이블을 등록한다.

        Args:
            widget: 레이블을 지정할 위젯
            label: 접근성 레이블 문자열
        """
        self._labels[id(widget)] = (widget, label)

    def get_label(self, widget: object) -> str | None:
        """위젯의 접근성 레이블을 조회한다.

        Args:
            widget: 레이블을 조회할 위젯

        Returns:
            접근성 레이블, 미등록이면 None
        """
        entry = self._labels.get(id(widget))
        if entry is not None:
            return entry[1]
        return None

    def unregister(self, widget: object) -> None:
        """위젯의 접근성 레이블을 해제한다.

        Args:
            widget: 레이블을 해제할 위젯
        """
        self._labels.pop(id(widget), None)

    def get_all(self) -> list[tuple[object, str]]:
        """등록된 모든 위젯-레이블 쌍을 반환한다.

        Returns:
            (위젯, 레이블) 튜플 리스트
        """
        return list(self._labels.values())


# ============================================================================
# Task 5.2: 상태 변경 알림
# ============================================================================


class StatusAnnouncer:
    """상태 변경 알림을 콜백으로 전달한다.

    스크린 리더 등 보조 기술에 상태 변경을 알린다.
    """

    def __init__(self) -> None:
        self.callbacks: list[Callable[[str], None]] = []

    def register_callback(self, callback: Callable[[str], None]) -> None:
        """알림 콜백을 등록한다.

        Args:
            callback: 상태 메시지를 받을 콜백 함수
        """
        self.callbacks.append(callback)

    def unregister_callback(self, callback: Callable[[str], None]) -> None:
        """알림 콜백을 해제한다.

        Args:
            callback: 해제할 콜백 함수
        """
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def announce(self, message: str) -> None:
        """상태 변경을 모든 등록된 콜백에 알린다.

        개별 콜백의 예외는 로깅 후 무시하여
        나머지 콜백의 실행을 보장한다.

        Args:
            message: 상태 변경 메시지
        """
        for callback in self.callbacks:
            try:
                callback(message)
            except Exception:
                logger.warning(
                    "상태 알림 콜백 실행 중 오류 발생", exc_info=True
                )


# ============================================================================
# Task 5.3: 포커스 링 스타일
# ============================================================================

# # @MX:NOTE: Apple HIG 포커스 링 스펙
FOCUS_RING_COLOR = "#007AFF"  # Apple Blue
FOCUS_RING_THICKNESS = 3      # 3pt solid
FOCUS_RING_OFFSET = 3         # 3px offset


def get_focus_ring_style() -> dict:
    """포커스 링 스타일 딕셔너리를 반환한다.

    Returns:
        color, thickness, offset 키를 포함하는 딕셔너리
    """
    return {
        "color": FOCUS_RING_COLOR,
        "thickness": FOCUS_RING_THICKNESS,
        "offset": FOCUS_RING_OFFSET,
    }


# ============================================================================
# Task 5.3: 초기 포커스
# ============================================================================

# 포커스 가능 위젯 우선순위 (입력 필드 > 버튼)
FOCUSABLE_WIDGET_PRIORITY = ["entry", "combobox", "optionmenu", "button"]


def get_initial_focus_page() -> str:
    """앱 시작 시 초기 포커스를 받을 페이지 이름을 반환한다.

    Returns:
        첫 번째 페이지 이름
    """
    return NAV_BUTTONS[0]


# ============================================================================
# Task 5.3: 포커스 트래핑 (모달 대화상자용)
# ============================================================================


class FocusTrap:
    """모달 대화상자의 포커스 트래핑을 구현한다.

    활성화 시 지정된 위젯 내에서만 Tab이 순환한다.
    """

    def __init__(self) -> None:
        self.is_active: bool = False
        self._trapped_widgets: list[object] = []
        self.current_index: int = -1

    def activate(self, widgets: list[object]) -> None:
        """포커스 트랩을 활성화한다.

        Args:
            widgets: 트랩할 위젯 리스트 (빈 리스트이면 비활성 유지)
        """
        if not widgets:
            return
        self._trapped_widgets = widgets
        self.is_active = True
        self.current_index = 0

    def deactivate(self) -> None:
        """포커스 트랩을 비활성화한다."""
        self.is_active = False
        self._trapped_widgets.clear()
        self.current_index = -1

    def next(self) -> object | None:
        """트랩 내 다음 위젯으로 이동한다.

        Returns:
            다음 위젯, 비활성 시 None
        """
        if not self.is_active or not self._trapped_widgets:
            return None
        self.current_index = (self.current_index + 1) % len(
            self._trapped_widgets
        )
        return self._trapped_widgets[self.current_index]


# ============================================================================
# Task 5.4: 고대비 모드
# ============================================================================

# WCAG AAA 대비 기준
WCAG_AAA_CONTRAST_RATIO = 7.0

# 모듈 수준 고대비 상태
_high_contrast_enabled: bool = False


def is_high_contrast_enabled() -> bool:
    """고대비 모드가 활성화되어 있는지 반환한다.

    Returns:
        고대비 모드 활성화 여부
    """
    return _high_contrast_enabled


def set_high_contrast(enabled: bool) -> None:
    """고대비 모드를 설정한다.

    Args:
        enabled: 활성화 여부
    """
    global _high_contrast_enabled
    _high_contrast_enabled = enabled


def toggle_high_contrast() -> bool:
    """고대비 모드를 토글한다.

    Returns:
        토글 후 고대비 모드 상태
    """
    global _high_contrast_enabled
    _high_contrast_enabled = not _high_contrast_enabled
    return _high_contrast_enabled


def get_high_contrast_colors(mode: str) -> dict[str, str]:
    """고대비 모드의 색상 딕셔너리를 반환한다.

    WCAG AAA 대비 기준(7:1)을 충족하도록 강화된 색상을 제공한다.

    Args:
        mode: "dark" 또는 "light"

    Returns:
        background, text_primary, border 등 키를 포함하는 딕셔너리
    """
    if mode == "dark":
        return {
            "background": "#000000",
            "text_primary": "#FFFFFF",
            "text_secondary": "#E0E0E0",
            "border": "#FFFFFF",
            "surface": "#1A1A1A",
        }
    return {
        "background": "#FFFFFF",
        "text_primary": "#000000",
        "text_secondary": "#333333",
        "border": "#000000",
        "surface": "#F5F5F5",
    }


def get_border_width(high_contrast: bool) -> int:
    """대비 모드에 따른 보더 두께를 반환한다.

    Args:
        high_contrast: 고대비 모드 활성화 여부

    Returns:
        보더 두께 (일반: 1pt, 고대비: 2pt)
    """
    return 2 if high_contrast else 1


def calculate_contrast_ratio(color1: str, color2: str) -> float:
    """두 HEX 색상의 WCAG 대비 비율을 계산한다.

    WCAG 2.0 상대 휘도 공식을 사용한다.

    Args:
        color1: 전경색 (HEX, 예: "#FFFFFF")
        color2: 배경색 (HEX, 예: "#000000")

    Returns:
        대비 비율 (1.0 ~ 21.0)
    """
    lum1 = _relative_luminance(color1)
    lum2 = _relative_luminance(color2)

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)


def _relative_luminance(hex_color: str) -> float:
    """HEX 색상의 상대 휘도를 계산한다.

    WCAG 2.0 공식: L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    각 채널은 sRGB 감마 보정을 적용한다.

    Args:
        hex_color: HEX 색상 문자열 ("#RRGGBB")

    Returns:
        상대 휘도 (0.0 ~ 1.0)
    """
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    # sRGB 감마 보정
    r = _linearize(r)
    g = _linearize(g)
    b = _linearize(b)

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _linearize(channel: float) -> float:
    """sRGB 채널 값을 선형화한다.

    Args:
        channel: 0.0 ~ 1.0 범위의 sRGB 채널 값

    Returns:
        선형화된 채널 값
    """
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4
