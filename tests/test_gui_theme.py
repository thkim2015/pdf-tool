"""GUI 테마 설정 테스트."""

from unittest.mock import MagicMock, patch

import pdf_tool.gui.theme as theme_module
from pdf_tool.gui.theme import (
    DARK_MODE,
    LIGHT_MODE,
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
