"""아이콘 매핑 테스트.

9개 기능별 유니코드 아이콘 매핑을 검증한다.
"""

from __future__ import annotations

# ============================================================================
# 아이콘 매핑 테스트
# ============================================================================


class Test_아이콘_매핑:
    """9개 기능별 아이콘 매핑이 존재하는지 검증한다."""

    def test_9개_기능_아이콘_존재(self):
        from pdf_tool.gui.icons import ICON_MAP

        expected_keys = {
            "Cut", "Merge", "Split", "Rotate", "Resize",
            "Compress", "Watermark", "Images to PDF", "Info",
        }
        assert set(ICON_MAP.keys()) == expected_keys

    def test_아이콘_개수(self):
        from pdf_tool.gui.icons import ICON_MAP

        assert len(ICON_MAP) == 9

    def test_각_아이콘이_유니코드(self):
        """각 아이콘 값은 유니코드 문자열이다."""
        from pdf_tool.gui.icons import ICON_MAP

        for name, icon in ICON_MAP.items():
            assert isinstance(icon, str), f"{name}의 아이콘이 문자열이 아닙니다"
            assert len(icon) >= 1, f"{name}의 아이콘이 비어 있습니다"

    def test_cut_아이콘(self):
        from pdf_tool.gui.icons import ICON_MAP

        assert ICON_MAP["Cut"] is not None

    def test_merge_아이콘(self):
        from pdf_tool.gui.icons import ICON_MAP

        assert ICON_MAP["Merge"] is not None

    def test_split_아이콘(self):
        from pdf_tool.gui.icons import ICON_MAP

        assert ICON_MAP["Split"] is not None

    def test_rotate_아이콘(self):
        from pdf_tool.gui.icons import ICON_MAP

        assert ICON_MAP["Rotate"] is not None

    def test_resize_아이콘(self):
        from pdf_tool.gui.icons import ICON_MAP

        assert ICON_MAP["Resize"] is not None

    def test_compress_아이콘(self):
        from pdf_tool.gui.icons import ICON_MAP

        assert ICON_MAP["Compress"] is not None

    def test_watermark_아이콘(self):
        from pdf_tool.gui.icons import ICON_MAP

        assert ICON_MAP["Watermark"] is not None

    def test_images_to_pdf_아이콘(self):
        from pdf_tool.gui.icons import ICON_MAP

        assert ICON_MAP["Images to PDF"] is not None

    def test_info_아이콘(self):
        from pdf_tool.gui.icons import ICON_MAP

        assert ICON_MAP["Info"] is not None


# ============================================================================
# get_icon 함수 테스트
# ============================================================================


class Test_get_icon_함수:
    """get_icon 함수를 검증한다."""

    def test_존재하는_아이콘_반환(self):
        from pdf_tool.gui.icons import get_icon

        icon = get_icon("Cut")
        assert isinstance(icon, str)
        assert len(icon) >= 1

    def test_존재하지_않는_아이콘_기본값(self):
        from pdf_tool.gui.icons import get_icon

        icon = get_icon("NonExistent")
        assert icon == ""

    def test_존재하지_않는_아이콘_커스텀_기본값(self):
        from pdf_tool.gui.icons import get_icon

        icon = get_icon("NonExistent", default="?")
        assert icon == "?"

    def test_모든_기능_아이콘_조회(self):
        from pdf_tool.gui.icons import get_icon

        features = [
            "Cut", "Merge", "Split", "Rotate", "Resize",
            "Compress", "Watermark", "Images to PDF", "Info",
        ]
        for feature in features:
            icon = get_icon(feature)
            assert icon != "", f"{feature}의 아이콘을 찾을 수 없습니다"


# ============================================================================
# 다크/라이트 모드 색상 테스트
# ============================================================================


class Test_아이콘_색상:
    """다크/라이트 모드별 아이콘 색상이 정의되어 있는지 검증한다."""

    def test_다크모드_색상_존재(self):
        from pdf_tool.gui.icons import ICON_COLORS

        assert "dark" in ICON_COLORS

    def test_라이트모드_색상_존재(self):
        from pdf_tool.gui.icons import ICON_COLORS

        assert "light" in ICON_COLORS

    def test_다크_라이트_색상_차이(self):
        from pdf_tool.gui.icons import ICON_COLORS

        assert ICON_COLORS["dark"] != ICON_COLORS["light"]
