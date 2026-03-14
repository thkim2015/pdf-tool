"""GUI 테마 설정 테스트."""

from unittest.mock import MagicMock

import pdf_tool.gui.theme as theme_module
from pdf_tool.gui.colors import DARK_PALETTE, LIGHT_PALETTE, get_palette
from pdf_tool.gui.theme import (
    DARK_MODE,
    LIGHT_MODE,
    get_current_palette,
    get_current_theme,
)


class Test_테마_상수:
    """테마 모드 상수가 올바르게 정의되어 있는지 검증한다."""

    def test_다크모드_상수(self):
        assert DARK_MODE == "dark"

    def test_라이트모드_상수(self):
        assert LIGHT_MODE == "light"


class Test_테마_적용:
    """apply_theme 함수가 customtkinter 설정을 올바르게 호출하는지 검증한다."""

    def test_다크_테마_적용(self):
        mock_ctk = MagicMock()
        theme_module.ctk = mock_ctk
        try:
            theme_module.apply_theme(DARK_MODE)
            mock_ctk.set_appearance_mode.assert_called_once_with("dark")
        finally:
            theme_module.ctk = None

    def test_라이트_테마_적용(self):
        mock_ctk = MagicMock()
        theme_module.ctk = mock_ctk
        try:
            theme_module.apply_theme(LIGHT_MODE)
            mock_ctk.set_appearance_mode.assert_called_once_with("light")
        finally:
            theme_module.ctk = None


class Test_테마_토글:
    """toggle_theme 함수가 현재 테마를 반대로 전환하는지 검증한다."""

    def test_다크에서_라이트로_토글(self):
        mock_ctk = MagicMock()
        theme_module.ctk = mock_ctk
        theme_module._current_theme = DARK_MODE
        try:
            result = theme_module.toggle_theme()
            assert result == LIGHT_MODE
            mock_ctk.set_appearance_mode.assert_called_once_with("light")
        finally:
            theme_module.ctk = None
            theme_module._current_theme = DARK_MODE

    def test_라이트에서_다크로_토글(self):
        mock_ctk = MagicMock()
        theme_module.ctk = mock_ctk
        theme_module._current_theme = LIGHT_MODE
        try:
            result = theme_module.toggle_theme()
            assert result == DARK_MODE
            mock_ctk.set_appearance_mode.assert_called_once_with("dark")
        finally:
            theme_module.ctk = None
            theme_module._current_theme = DARK_MODE


class Test_현재_테마_조회:
    """get_current_theme 함수가 현재 테마를 올바르게 반환하는지 검증한다."""

    def test_현재_테마_다크(self):
        theme_module._current_theme = DARK_MODE
        try:
            assert get_current_theme() == DARK_MODE
        finally:
            theme_module._current_theme = DARK_MODE

    def test_현재_테마_라이트(self):
        theme_module._current_theme = LIGHT_MODE
        try:
            assert get_current_theme() == LIGHT_MODE
        finally:
            theme_module._current_theme = DARK_MODE


class Test_색상_팔레트:
    """색상 팔레트가 올바르게 정의되어 있는지 검증한다."""

    def test_다크_팔레트_기본_색상(self):
        """다크 팔레트가 기본 색상들을 정의하고 있다."""
        assert DARK_PALETTE.primary == "#3b82f6"
        assert DARK_PALETTE.secondary == "#8b5cf6"
        assert DARK_PALETTE.accent == "#ec4899"

    def test_다크_팔레트_배경색(self):
        """다크 팔레트가 배경색을 정의하고 있다."""
        assert DARK_PALETTE.background == "#0f172a"
        assert DARK_PALETTE.surface == "#1e293b"
        assert DARK_PALETTE.surface_elevated == "#334155"

    def test_다크_팔레트_텍스트색(self):
        """다크 팔레트가 텍스트 색상을 정의하고 있다."""
        assert DARK_PALETTE.text_primary == "#f1f5f9"
        assert DARK_PALETTE.text_secondary == "#cbd5e1"
        assert DARK_PALETTE.text_tertiary == "#94a3b8"

    def test_다크_팔레트_상태색(self):
        """다크 팔레트가 상태 색상들을 정의하고 있다."""
        assert DARK_PALETTE.success == "#10b981"
        assert DARK_PALETTE.error == "#ef4444"
        assert DARK_PALETTE.warning == "#f59e0b"
        assert DARK_PALETTE.info == "#06b6d4"

    def test_라이트_팔레트_기본_색상(self):
        """라이트 팔레트가 기본 색상들을 정의하고 있다."""
        assert LIGHT_PALETTE.primary == "#2563eb"
        assert LIGHT_PALETTE.secondary == "#7c3aed"
        assert LIGHT_PALETTE.accent == "#db2777"

    def test_라이트_팔레트_배경색(self):
        """라이트 팔레트가 배경색을 정의하고 있다."""
        assert LIGHT_PALETTE.background == "#f8fafc"
        assert LIGHT_PALETTE.surface == "#ffffff"
        assert LIGHT_PALETTE.surface_elevated == "#f1f5f9"

    def test_팔레트_불변(self):
        """팔레트는 불변이다 (frozen dataclass)."""
        from dataclasses import FrozenInstanceError
        import pytest

        with pytest.raises(FrozenInstanceError):
            DARK_PALETTE.primary = "#000000"

    def test_get_palette_다크(self):
        """get_palette 함수가 다크 모드용 팔레트를 반환한다."""
        palette = get_palette("dark")
        assert palette.primary == "#3b82f6"

    def test_get_palette_라이트(self):
        """get_palette 함수가 라이트 모드용 팔레트를 반환한다."""
        palette = get_palette("light")
        assert palette.primary == "#2563eb"

    def test_get_palette_기본값(self):
        """get_palette 함수는 잘못된 모드는 다크 모드로 기본값 처리한다."""
        palette = get_palette("invalid")
        assert palette.primary == "#3b82f6"  # 다크 팔레트


class Test_현재_팔레트_조회:
    """get_current_palette 함수가 현재 테마에 맞는 팔레트를 반환하는지 검증한다."""

    def test_다크_모드_팔레트(self):
        theme_module._current_theme = DARK_MODE
        theme_module._current_palette = None
        try:
            palette = get_current_palette()
            assert palette.primary == "#3b82f6"
        finally:
            theme_module._current_theme = DARK_MODE
            theme_module._current_palette = None

    def test_라이트_모드_팔레트(self):
        theme_module._current_theme = LIGHT_MODE
        theme_module._current_palette = None
        try:
            palette = get_current_palette()
            assert palette.primary == "#2563eb"
        finally:
            theme_module._current_theme = DARK_MODE
            theme_module._current_palette = None
