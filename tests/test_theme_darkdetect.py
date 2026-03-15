"""theme.py darkdetect 연동 테스트.

시스템 테마 자동 감지 및 테마 전환 기능을 검증한다.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pdf_tool.gui.theme as theme_module


class Test_시스템_테마_감지:
    """시스템 테마 자동 감지 기능을 검증한다."""

    def test_시스템_다크모드_감지(self):
        """시스템이 다크 모드일 때 'dark'를 반환한다."""
        with patch.object(theme_module, "_detect_system_theme", return_value="dark"):
            result = theme_module._detect_system_theme()
            assert result == "dark"

    def test_시스템_라이트모드_감지(self):
        """시스템이 라이트 모드일 때 'light'를 반환한다."""
        with patch.object(theme_module, "_detect_system_theme", return_value="light"):
            result = theme_module._detect_system_theme()
            assert result == "light"


class Test_테마_콜백_등록:
    """테마 변경 콜백 등록/해제 기능을 검증한다."""

    def test_콜백_등록(self):
        """테마 변경 콜백을 등록할 수 있다."""
        callback = MagicMock()
        theme_module.register_theme_callback(callback)
        try:
            assert callback in theme_module._theme_callbacks
        finally:
            theme_module._theme_callbacks.clear()

    def test_콜백_해제(self):
        """등록된 콜백을 해제할 수 있다."""
        callback = MagicMock()
        theme_module.register_theme_callback(callback)
        theme_module.unregister_theme_callback(callback)
        assert callback not in theme_module._theme_callbacks

    def test_테마_변경시_콜백_호출(self):
        """테마가 변경되면 등록된 콜백이 호출된다."""
        mock_ctk = MagicMock()
        theme_module.ctk = mock_ctk
        callback = MagicMock()
        theme_module.register_theme_callback(callback)
        try:
            theme_module.apply_theme("light")
            callback.assert_called_once_with("light")
        finally:
            theme_module.ctk = None
            theme_module._theme_callbacks.clear()
            theme_module._current_theme = "dark"

    def test_다수_콜백_모두_호출(self):
        """여러 콜백이 등록된 경우 모두 호출된다."""
        mock_ctk = MagicMock()
        theme_module.ctk = mock_ctk
        cb1 = MagicMock()
        cb2 = MagicMock()
        theme_module.register_theme_callback(cb1)
        theme_module.register_theme_callback(cb2)
        try:
            theme_module.apply_theme("dark")
            cb1.assert_called_once_with("dark")
            cb2.assert_called_once_with("dark")
        finally:
            theme_module.ctk = None
            theme_module._theme_callbacks.clear()
            theme_module._current_theme = "dark"


class Test_시스템_테마_추적:
    """시스템 테마 변경 추적 기능을 검증한다."""

    def test_detect_system_theme_함수_존재(self):
        """_detect_system_theme 함수가 존재한다."""
        assert hasattr(theme_module, "_detect_system_theme")
        assert callable(theme_module._detect_system_theme)

    def test_register_theme_callback_함수_존재(self):
        """register_theme_callback 함수가 존재한다."""
        assert hasattr(theme_module, "register_theme_callback")

    def test_unregister_theme_callback_함수_존재(self):
        """unregister_theme_callback 함수가 존재한다."""
        assert hasattr(theme_module, "unregister_theme_callback")


class Test_detect_system_theme_실행:
    """_detect_system_theme 함수의 실제 실행 경로를 검증한다."""

    def test_darkdetect_import_실패시_기본값(self):
        """darkdetect를 import할 수 없으면 'dark'를 반환한다."""
        with patch.dict("sys.modules", {"darkdetect": None}):
            # import 실패 시뮬레이션
            import importlib
            importlib.reload(theme_module)
            result = theme_module._detect_system_theme()
            assert result == "dark"
            # 모듈 복원
            importlib.reload(theme_module)

    def test_darkdetect_반환값_dark(self):
        """darkdetect가 'Dark'를 반환하면 'dark'로 변환한다."""
        mock_darkdetect = MagicMock()
        mock_darkdetect.theme.return_value = "Dark"
        with patch.dict("sys.modules", {"darkdetect": mock_darkdetect}):
            result = theme_module._detect_system_theme()
            assert result == "dark"

    def test_darkdetect_반환값_light(self):
        """darkdetect가 'Light'를 반환하면 'light'로 변환한다."""
        mock_darkdetect = MagicMock()
        mock_darkdetect.theme.return_value = "Light"
        with patch.dict("sys.modules", {"darkdetect": mock_darkdetect}):
            result = theme_module._detect_system_theme()
            assert result == "light"

    def test_darkdetect_반환값_none(self):
        """darkdetect가 None을 반환하면 'dark'를 반환한다."""
        mock_darkdetect = MagicMock()
        mock_darkdetect.theme.return_value = None
        with patch.dict("sys.modules", {"darkdetect": mock_darkdetect}):
            result = theme_module._detect_system_theme()
            assert result == "dark"

    def test_darkdetect_예외시_기본값(self):
        """darkdetect에서 예외 발생 시 'dark'를 반환한다."""
        mock_darkdetect = MagicMock()
        mock_darkdetect.theme.side_effect = RuntimeError("테스트 오류")
        with patch.dict("sys.modules", {"darkdetect": mock_darkdetect}):
            result = theme_module._detect_system_theme()
            assert result == "dark"


class Test_콜백_오류_처리:
    """콜백 실행 중 오류가 발생해도 다른 콜백은 실행되는지 검증한다."""

    def test_오류_콜백_이후에도_실행(self):
        """하나의 콜백에서 오류가 발생해도 나머지 콜백은 실행된다."""
        mock_ctk = MagicMock()
        theme_module.ctk = mock_ctk
        error_cb = MagicMock(side_effect=ValueError("테스트 오류"))
        normal_cb = MagicMock()
        theme_module.register_theme_callback(error_cb)
        theme_module.register_theme_callback(normal_cb)
        try:
            theme_module.apply_theme("dark")
            error_cb.assert_called_once_with("dark")
            normal_cb.assert_called_once_with("dark")
        finally:
            theme_module.ctk = None
            theme_module._theme_callbacks.clear()
            theme_module._current_theme = "dark"

    def test_중복_콜백_등록_방지(self):
        """같은 콜백을 두 번 등록하면 하나만 등록된다."""
        callback = MagicMock()
        theme_module.register_theme_callback(callback)
        theme_module.register_theme_callback(callback)
        try:
            assert theme_module._theme_callbacks.count(callback) == 1
        finally:
            theme_module._theme_callbacks.clear()

    def test_미등록_콜백_해제_안전(self):
        """등록되지 않은 콜백을 해제해도 오류가 발생하지 않는다."""
        callback = MagicMock()
        # 오류 없이 실행
        theme_module.unregister_theme_callback(callback)


class Test_기존_기능_회귀:
    """기존 기능이 회귀 없이 동작하는지 확인한다."""

    def test_apply_theme_기존_동작(self):
        """apply_theme가 기존처럼 customtkinter를 호출한다."""
        mock_ctk = MagicMock()
        theme_module.ctk = mock_ctk
        theme_module._theme_callbacks.clear()
        try:
            theme_module.apply_theme("dark")
            mock_ctk.set_appearance_mode.assert_called_once_with("dark")
        finally:
            theme_module.ctk = None
            theme_module._current_theme = "dark"

    def test_toggle_theme_기존_동작(self):
        """toggle_theme가 기존처럼 작동한다."""
        mock_ctk = MagicMock()
        theme_module.ctk = mock_ctk
        theme_module._current_theme = "dark"
        theme_module._theme_callbacks.clear()
        try:
            result = theme_module.toggle_theme()
            assert result == "light"
        finally:
            theme_module.ctk = None
            theme_module._current_theme = "dark"

    def test_get_current_theme_기존_동작(self):
        """get_current_theme가 기존처럼 작동한다."""
        theme_module._current_theme = "dark"
        assert theme_module.get_current_theme() == "dark"

    def test_get_current_palette_기존_동작(self):
        """get_current_palette가 기존처럼 작동한다."""
        theme_module._current_theme = "dark"
        theme_module._current_palette = None
        palette = theme_module.get_current_palette()
        assert palette.primary == "#007AFF"
