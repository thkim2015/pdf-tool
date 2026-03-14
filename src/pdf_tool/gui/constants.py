"""GUI 상수 정의 모듈.

윈도우 크기, 패딩, 폰트 등 UI 관련 상수를 중앙에서 관리한다.
"""

from __future__ import annotations

# ============================================================================
# 윈도우 크기 및 레이아웃
# ============================================================================

# 윈도우 기본 크기
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# 사이드바
SIDEBAR_WIDTH = 200
SIDEBAR_VISIBLE = True

# 메인 컨텐츠 영역 패딩
MAIN_PADX = 12
MAIN_PADY = 12


# ============================================================================
# 스페이싱 및 패딩 (4px 단위)
# ============================================================================

PADDING_UNIT = 4

# 기본 패딩 (단위: px)
PADDING_XS = PADDING_UNIT      # 4px
PADDING_SM = PADDING_UNIT * 2  # 8px
PADDING_MD = PADDING_UNIT * 3  # 12px
PADDING_LG = PADDING_UNIT * 4  # 16px
PADDING_XL = PADDING_UNIT * 5  # 20px
PADDING_2XL = PADDING_UNIT * 6 # 24px

# 일반적인 간격
PADX_DEFAULT = PADDING_MD      # 12px
PADY_DEFAULT = PADDING_SM      # 8px

# 섹션 간격
SECTION_SPACING = PADDING_LG   # 16px

# 요소 간 간격
ELEMENT_SPACING = PADDING_SM   # 8px


# ============================================================================
# 테두리 반지름 (모서리 둥글기)
# ============================================================================

BORDER_RADIUS_NONE = 0
BORDER_RADIUS_SM = 4
BORDER_RADIUS_MD = 8     # 기본값
BORDER_RADIUS_LG = 12
BORDER_RADIUS_FULL = 20

# 기본 테두리 반지름
BORDER_RADIUS_DEFAULT = BORDER_RADIUS_MD


# ============================================================================
# 버튼 크기 및 스타일
# ============================================================================

# 버튼 높이
BUTTON_HEIGHT_SM = 28
BUTTON_HEIGHT_MD = 36  # 기본값
BUTTON_HEIGHT_LG = 44

# 버튼 기본 높이
BUTTON_HEIGHT_DEFAULT = BUTTON_HEIGHT_MD

# 버튼 가로 패딩
BUTTON_PADX = PADDING_MD

# 버튼 세로 패딩
BUTTON_PADY = PADDING_SM


# ============================================================================
# 입력 필드 크기
# ============================================================================

# 입력 필드 높이
INPUT_HEIGHT_SM = 28
INPUT_HEIGHT_MD = 36  # 기본값
INPUT_HEIGHT_LG = 44

INPUT_HEIGHT_DEFAULT = INPUT_HEIGHT_MD

# 입력 필드 테두리
INPUT_BORDER_WIDTH = 1

# 옵션 메뉴 및 기타 컨트롤 높이
OPTIONMENU_HEIGHT_DEFAULT = BUTTON_HEIGHT_DEFAULT
RADIOBUTTON_PADX = PADDING_MD
RADIOBUTTON_PADY = PADDING_SM

# 섹션 및 그룹 스타일
SECTION_PADDING = PADDING_LG
SECTION_LABEL_PADDING = (PADDING_MD, 0)
SUBSECTION_PADDING = PADDING_MD
ITEM_SPACING = PADDING_SM


# ============================================================================
# Typography (폰트)
# ============================================================================

# 기본 폰트 이름 (시스템 기본값 또는 지정)
FONT_FAMILY_DEFAULT = "System"
FONT_FAMILY_MONO = "Menlo"  # macOS 또는 "Courier New" (Windows)

# 제목 폰트 크기
FONT_SIZE_H1 = 28
FONT_SIZE_H2 = 24
FONT_SIZE_H3 = 20
FONT_SIZE_TITLE = 18   # 페이지 제목

# 본문 폰트 크기
FONT_SIZE_BASE = 13    # 기본 텍스트
FONT_SIZE_SM = 12
FONT_SIZE_XS = 11
FONT_SIZE_LG = 14

# 폰트 가중치
FONT_WEIGHT_NORMAL = "normal"
FONT_WEIGHT_BOLD = "bold"

# 일반적인 폰트 조합
FONT_TITLE = (FONT_FAMILY_DEFAULT, FONT_SIZE_H3, FONT_WEIGHT_BOLD)
FONT_LABEL = (FONT_FAMILY_DEFAULT, FONT_SIZE_BASE, FONT_WEIGHT_NORMAL)
FONT_LABEL_BOLD = (FONT_FAMILY_DEFAULT, FONT_SIZE_BASE, FONT_WEIGHT_BOLD)
FONT_SMALL = (FONT_FAMILY_DEFAULT, FONT_SIZE_SM, FONT_WEIGHT_NORMAL)
FONT_SMALL_BOLD = (FONT_FAMILY_DEFAULT, FONT_SIZE_SM, FONT_WEIGHT_BOLD)


# ============================================================================
# 컴포넌트 크기
# ============================================================================

# 파일 피커 영역 높이
FILE_PICKER_HEIGHT = BUTTON_HEIGHT_DEFAULT + PADDING_LG

# 결과 표시 영역 최소 높이
RESULT_DISPLAY_MIN_HEIGHT = 120

# 진행률 바 높이
PROGRESS_BAR_HEIGHT = BUTTON_HEIGHT_SM

# 프리뷰 이미지 최대 너비/높이
PREVIEW_MAX_WIDTH = 400
PREVIEW_MAX_HEIGHT = 300


# ============================================================================
# 애니메이션 및 타이밍
# ============================================================================

# 전환 애니메이션 시간 (ms)
ANIMATION_DURATION_MS = 200

# 호버 효과 반응 시간 (ms)
HOVER_DURATION_MS = 150

# 토스트 알림 표시 시간 (ms)
TOAST_DURATION_MS = 3000

# 진행률 바 애니메이션 주기 (ms)
PROGRESS_ANIMATION_MS = 50


# ============================================================================
# 네비게이션
# ============================================================================

# 네비게이션 버튼 이름
NAV_BUTTONS = ["Cut", "Merge", "Split", "Rotate", "Resize", "Compress", "Watermark", "Images to PDF", "Info"]

# 네비게이션 버튼 개수
NAV_BUTTON_COUNT = len(NAV_BUTTONS)


# ============================================================================
# 기타 상수
# ============================================================================

# 최대 파일 크기 (바이트)
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

# 로깅 레벨
LOG_LEVEL = "INFO"

# 더블클릭 시간 간격 (ms)
DOUBLE_CLICK_INTERVAL_MS = 300

# 포커스 링 너비 (px)
FOCUS_RING_WIDTH = 2

# 포커스 링 오프셋 (px)
FOCUS_RING_OFFSET = 1


# ============================================================================
# 반응형 브레이크포인트 (Optional future use)
# ============================================================================

BREAKPOINT_MOBILE = 600
BREAKPOINT_TABLET = 900
BREAKPOINT_DESKTOP = 1200
