"""GUI 상수 테스트."""

from pdf_tool.gui.constants import (
    BORDER_RADIUS_DEFAULT,
    BUTTON_HEIGHT_DEFAULT,
    BUTTON_HEIGHT_LG,
    BUTTON_HEIGHT_SM,
    ELEMENT_SPACING,
    FONT_LABEL,
    FONT_LABEL_BOLD,
    FONT_SIZE_BASE,
    FONT_SIZE_H1,
    FONT_SIZE_H2,
    FONT_SIZE_H3,
    FONT_SIZE_LG,
    FONT_SIZE_SM,
    FONT_SIZE_TITLE,
    FONT_SIZE_XS,
    FONT_SMALL,
    FONT_SMALL_BOLD,
    FONT_TITLE,
    INPUT_HEIGHT_DEFAULT,
    INPUT_HEIGHT_LG,
    INPUT_HEIGHT_SM,
    MAIN_PADX,
    MAIN_PADY,
    NAV_BUTTON_COUNT,
    NAV_BUTTONS,
    PADDING_2XL,
    PADDING_LG,
    PADDING_MD,
    PADDING_SM,
    PADDING_UNIT,
    PADDING_XL,
    PADDING_XS,
    SECTION_SPACING,
    SIDEBAR_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_WIDTH,
)


class Test_스페이싱_상수:
    """스페이싱 상수들이 올바르게 정의되어 있는지 검증한다."""

    def test_기본_단위(self):
        """기본 패딩 단위는 8pt이다."""
        assert PADDING_UNIT == 8

    def test_패딩_계산(self):
        """패딩 상수들이 기본 단위의 배수인지 확인한다."""
        assert PADDING_XS == PADDING_UNIT
        assert PADDING_SM == PADDING_UNIT * 2
        assert PADDING_MD == PADDING_UNIT * 3
        assert PADDING_LG == PADDING_UNIT * 4
        assert PADDING_XL == PADDING_UNIT * 5
        assert PADDING_2XL == PADDING_UNIT * 6

    def test_구체적_패딩값(self):
        """구체적 패딩 값들이 올바르다 (8pt 그리드)."""
        assert PADDING_XS == 8
        assert PADDING_SM == 16
        assert PADDING_MD == 24
        assert PADDING_LG == 32
        assert PADDING_XL == 40
        assert PADDING_2XL == 48

    def test_섹션_간격(self):
        """섹션 간격이 정의되어 있다."""
        assert SECTION_SPACING == PADDING_LG

    def test_요소_간격(self):
        """요소 간 간격이 정의되어 있다."""
        assert ELEMENT_SPACING == PADDING_XS


class Test_윈도우_크기:
    """윈도우 크기 상수들이 올바르게 정의되어 있는지 검증한다."""

    def test_기본_윈도우_크기(self):
        """기본 윈도우 크기가 정의되어 있다."""
        assert WINDOW_WIDTH == 1000
        assert WINDOW_HEIGHT == 700

    def test_최소_윈도우_크기(self):
        """최소 윈도우 크기가 정의되어 있다."""
        assert WINDOW_MIN_WIDTH == 800
        assert WINDOW_MIN_HEIGHT == 600

    def test_사이드바_너비(self):
        """사이드바 너비가 정의되어 있다."""
        assert SIDEBAR_WIDTH == 200

    def test_메인_영역_패딩(self):
        """메인 영역 패딩이 8pt 그리드 기반이다."""
        assert MAIN_PADX == PADDING_SM  # 16pt
        assert MAIN_PADY == PADDING_SM  # 16pt


class Test_테두리_반지름:
    """테두리 반지름 상수들이 올바르게 정의되어 있는지 검증한다."""

    def test_기본_테두리_반지름(self):
        """기본 테두리 반지름이 10px (Apple Medium)이다."""
        assert BORDER_RADIUS_DEFAULT == 10


class Test_버튼_크기:
    """버튼 크기 상수들이 올바르게 정의되어 있는지 검증한다."""

    def test_버튼_높이(self):
        """각 버튼 높이 상수들이 정의되어 있다."""
        assert BUTTON_HEIGHT_SM == 28
        assert BUTTON_HEIGHT_DEFAULT == 36
        assert BUTTON_HEIGHT_LG == 44

    def test_기본_버튼_높이(self):
        """기본 버튼 높이는 36px이다."""
        assert BUTTON_HEIGHT_DEFAULT == 36


class Test_입력_필드_크기:
    """입력 필드 크기 상수들이 올바르게 정의되어 있는지 검증한다."""

    def test_입력_필드_높이(self):
        """각 입력 필드 높이 상수들이 정의되어 있다."""
        assert INPUT_HEIGHT_SM == 28
        assert INPUT_HEIGHT_DEFAULT == 36
        assert INPUT_HEIGHT_LG == 44

    def test_기본_입력_필드_높이(self):
        """기본 입력 필드 높이는 36px이다."""
        assert INPUT_HEIGHT_DEFAULT == 36


class Test_폰트_크기:
    """폰트 크기 상수들이 올바르게 정의되어 있는지 검증한다."""

    def test_제목_폰트_크기(self):
        """제목 폰트 크기가 Apple Dynamic Type 스케일이다."""
        assert FONT_SIZE_H1 == 34   # Large Title
        assert FONT_SIZE_H2 == 28   # Title 1
        assert FONT_SIZE_H3 == 22   # Title 2
        assert FONT_SIZE_TITLE == 20  # Title 3

    def test_본문_폰트_크기(self):
        """본문 폰트 크기가 Apple Dynamic Type 스케일이다."""
        assert FONT_SIZE_BASE == 17  # Body
        assert FONT_SIZE_SM == 15    # Subheadline
        assert FONT_SIZE_XS == 13    # Footnote
        assert FONT_SIZE_LG == 16    # Callout

    def test_폰트_조합_구조(self):
        """폰트 조합이 (name, size, weight) 튜플이다."""
        assert isinstance(FONT_TITLE, tuple)
        assert len(FONT_TITLE) == 3
        assert FONT_TITLE[1] == FONT_SIZE_H3

    def test_폰트_조합들(self):
        """주요 폰트 조합들이 정의되어 있다."""
        assert FONT_TITLE[1] == 22   # Title 2
        assert FONT_LABEL[1] == 17   # Body
        assert FONT_LABEL_BOLD[1] == 17
        assert FONT_SMALL[1] == 15   # Subheadline
        assert FONT_SMALL_BOLD[1] == 15


class Test_네비게이션:
    """네비게이션 상수들이 올바르게 정의되어 있는지 검증한다."""

    def test_네비게이션_버튼_목록(self):
        """네비게이션 버튼 목록이 9개이다."""
        expected = [
            "Cut", "Merge", "Split", "Rotate", "Resize",
            "Compress", "Watermark", "Images to PDF", "Info",
        ]
        assert expected == NAV_BUTTONS

    def test_네비게이션_버튼_개수(self):
        """네비게이션 버튼 개수 상수와 실제 개수가 일치한다."""
        assert len(NAV_BUTTONS) == NAV_BUTTON_COUNT
        assert NAV_BUTTON_COUNT == 9

    def test_네비게이션_버튼_고유성(self):
        """네비게이션 버튼 이름들이 고유하다."""
        assert len(NAV_BUTTONS) == len(set(NAV_BUTTONS))


class Test_상수_일관성:
    """상수들 간의 일관성을 검증한다."""

    def test_버튼과_입력_필드_높이_일치(self):
        """버튼과 입력 필드의 기본 높이가 동일하다."""
        assert BUTTON_HEIGHT_DEFAULT == INPUT_HEIGHT_DEFAULT

    def test_메인_패딩이_표준_패딩(self):
        """메인 영역의 패딩이 표준 패딩을 사용한다."""
        assert MAIN_PADX in (PADDING_XS, PADDING_SM, PADDING_MD, PADDING_LG)
        assert MAIN_PADY in (PADDING_XS, PADDING_SM, PADDING_MD, PADDING_LG)
