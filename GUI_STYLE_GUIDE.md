# PDF-Tool GUI 스타일 가이드

## 1. 색상 팔레트

### 다크모드 (기본값)
```
Primary:        #3b82f6 (Bright Blue)
Secondary:      #8b5cf6 (Purple)
Accent:         #ec4899 (Pink)

Background:     #0f172a (Navy Black)
Surface:        #1e293b (Dark Slate)
Surface Elevated: #334155 (Slate)

Text Primary:   #f1f5f9 (Light Slate)
Text Secondary: #cbd5e1 (Medium Slate)
Text Tertiary:  #94a3b8 (Dim Slate)

Success:        #10b981 (Emerald)
Warning:        #f59e0b (Amber)
Error:          #ef4444 (Red)
Info:           #06b6d4 (Cyan)
```

### 라이트모드
```
Primary:        #2563eb (Deep Blue)
Secondary:      #7c3aed (Deep Purple)
Accent:         #db2777 (Deep Pink)

Background:     #f8fafc (Very Light Slate)
Surface:        #ffffff (White)
Surface Elevated: #f1f5f9 (Light Slate)

Text Primary:   #0f172a (Navy Black)
Text Secondary: #475569 (Slate)
Text Tertiary:  #94a3b8 (Dim Slate)

Success:        #059669 (Deep Emerald)
Warning:        #d97706 (Deep Amber)
Error:          #dc2626 (Deep Red)
Info:           #0891b2 (Deep Cyan)
```

## 2. 스페이싱 및 패딩

### 기본 단위: 4px

```
XS (4px):     PADDING_XS
SM (8px):     PADDING_SM
MD (12px):    PADDING_MD (기본)
LG (16px):    PADDING_LG
XL (20px):    PADDING_XL
2XL (24px):   PADDING_2XL

일반 패딩:    PADX_DEFAULT (12px), PADY_DEFAULT (8px)
섹션 간격:    SECTION_SPACING (16px)
요소 간격:    ELEMENT_SPACING (8px)
```

### 사용 규칙
- 버튼 간격: `PADDING_MD` (12px)
- 섹션 구분: `SECTION_SPACING` (16px)
- 요소 내부: `PADDING_SM` ~ `PADDING_MD`

## 3. Typography (폰트)

### 제목 (Titles)
```
H1: 28px, Bold
H2: 24px, Bold
H3: 20px, Bold
Title: 18px, Bold (페이지 제목)

사용: FONT_TITLE = (system_font, 20, "bold")
```

### 본문 (Body)
```
Base: 13px, Normal (기본 텍스트)
Small: 12px, Normal
XS: 11px, Normal
Large: 14px, Normal

사용: FONT_LABEL = (system_font, 13, "normal")
```

### 강조 (Emphasis)
```
Label Bold: 13px, Bold
Small Bold: 12px, Bold

사용: FONT_LABEL_BOLD = (system_font, 13, "bold")
```

## 4. 버튼 스타일

### 기본 버튼 (Primary)
```python
ctk.CTkButton(
    master,
    text="버튼 텍스트",
    height=BUTTON_HEIGHT_DEFAULT,       # 36px
    corner_radius=BORDER_RADIUS_DEFAULT, # 8px
    fg_color=palette.primary,            # Blue
    hover_color=palette.button_hover,    # Darker Blue
)
```

### 보조 버튼 (Secondary)
```python
ctk.CTkButton(
    master,
    text="보조 버튼",
    height=BUTTON_HEIGHT_DEFAULT,
    corner_radius=BORDER_RADIUS_DEFAULT,
    fg_color=palette.secondary,          # Purple
    hover_color=palette.button_hover,
)
```

### 위험 버튼 (Danger)
```python
ctk.CTkButton(
    master,
    text="삭제",
    height=BUTTON_HEIGHT_DEFAULT,
    fg_color=palette.error,              # Red
    hover_color=palette.button_hover,
)
```

### 작은 버튼 (Small)
```python
ctk.CTkButton(
    master,
    text="↑",
    width=36,
    height=BUTTON_HEIGHT_SM,             # 28px
    corner_radius=BORDER_RADIUS_DEFAULT,
    fg_color=palette.secondary,
)
```

### 버튼 아이콘 규칙
- 추가: ➕
- 제거: ✕
- 실행: ✨
- 위로/아래: ↑↓
- 병합: ✨
- 파일: 📁
- 테마: 🌙
- 정보: ℹ️
- 성공: ✓
- 에러: ✗

## 5. 입력 필드 스타일

### 기본 입력 필드
```python
ctk.CTkEntry(
    master,
    placeholder_text="입력하세요...",
    height=INPUT_HEIGHT_DEFAULT,         # 36px
    corner_radius=BORDER_RADIUS_DEFAULT, # 8px
    fg_color=palette.surface_elevated,
    text_color=palette.text_primary,
    placeholder_text_color=palette.text_tertiary,
)
```

### 포커스 상태
- 테두리: palette.primary (자동)
- 배경: palette.surface_elevated (유지)

## 6. 컴포넌트 사용 규칙

### FilePickerWidget
```python
FilePickerWidget(
    parent,
    on_file_selected=callback,
)
# 자동으로 palette 기반 색상 적용
```

### BasePageWidget
```python
# Automatic layout:
# 1. 파일 선택 영역 (FilePickerWidget)
# 2. 파라미터 영역 (custom)
# 3. 실행 버튼
# 4. 프로그레스 바
# 5. 결과 표시 영역

# 모든 padding은 PADDING_MD 사용
```

### 결과 표시 위젯
```python
# Success (초록)
result_display.show_success("완료!", output_path)

# Error (빨강)
result_display.show_error("오류 메시지")

# Info (파랑)
result_display.show_info({"key": "value"})
```

## 7. 레이아웃 규칙

### 반응형 레이아웃
```
최소 너비: WINDOW_MIN_WIDTH (800px)
최소 높이: WINDOW_MIN_HEIGHT (600px)
기본 크기: WINDOW_WIDTH (1000px) x WINDOW_HEIGHT (700px)
```

### 윈도우 구조
```
┌─────────────────────────────────────┐
│  Sidebar (200px)  │  Main Area      │
│  ───────────────  │  ──────────────│
│  PDF Tool (Title) │                 │
│  ───────────────  │  Page Content   │
│  [Cut]            │                 │
│  [Merge]          │                 │
│  [Split]          │  padding: 12px  │
│  ...              │                 │
│  [Theme Toggle]   │                 │
└─────────────────────────────────────┘
```

### 페이지 레이아웃
```
┌─────────────────────────────────────────┐
│  File Picker  (padding: 12px)           │
├─────────────────────────────────────────┤
│  Parameters   (padding: 12px)           │
├─────────────────────────────────────────┤
│  [Execute Button] (height: 36px)        │
├─────────────────────────────────────────┤
│  Progress Bar (conditional)             │
├─────────────────────────────────────────┤
│  Result Display (flex: 1)               │
│  padding: 12px                          │
└─────────────────────────────────────────┘
```

## 8. 상태 표시

### 성공 상태
```
Icon:  ✓ (체크마크)
Color: palette.success (#10b981)
Text:  "✓ 완료!"
```

### 에러 상태
```
Icon:  ✗ (엑스)
Color: palette.error (#ef4444)
Text:  "✗ 오류 메시지"
```

### 정보 상태
```
Icon:  ℹ️ (정보)
Color: palette.info (#06b6d4)
Text:  "ℹ️ 정보 메시지"
```

### 로딩 상태
```
Progress Bar:
- Background: palette.surface_elevated
- Progress: palette.primary
- Animation: Indeterminate
- Status Text: "처리 중..."
```

## 9. 접근성

### 대비도
- Text Primary ↔ Background: WCAG AA 이상
- Button Text ↔ Button BG: WCAG AA 이상

### 포커스 인디케이터
- 포커스링: 자동으로 적용됨
- 색상: 테마에 따라 자동 조정

### 키보드 네비게이션
- Tab: 다음 요소로 이동
- Shift+Tab: 이전 요소로 이동
- Enter: 버튼 클릭
- Escape: 다이얼로그 닫기

## 10. 테마 전환

### Dark ↔ Light 전환
```python
from pdf_tool.gui.theme import toggle_theme, get_current_palette

# 테마 전환
new_theme = toggle_theme()

# 현재 팔레트 획득
palette = get_current_palette()
```

### 동적 업데이트
- 모든 위젯이 자동으로 새 팔레트 색상을 사용
- 새 스레드에서 렌더링 중일 때도 안전

## 11. 아이콘 및 이모지

### 사용 가능한 이모지
```
UI Controls:
  ↑ ↓ ↔ ← → 
  ✓ ✗ ✕ ✨ 
  ➕ ➖ ⚙️ 
  📁 📂 📄 
  🌙 ☀️ 
  ℹ️ ⚠️ ❌ 
```

### 사용 규칙
- 한글 텍스트 전에 이모지 배치
- 이모지 뒤에 공백 추가
- 예: `"✨ 병합 실행"`

## 12. 색상 적용 체크리스트

### 새 위젯 추가 시
- [ ] `from pdf_tool.gui.theme import get_current_palette` 임포트
- [ ] `palette = get_current_palette()` 호출
- [ ] 텍스트 색상: `palette.text_primary` 또는 `text_secondary`
- [ ] 배경색: `palette.surface` 또는 `surface_elevated`
- [ ] 버튼 색상: `palette.primary` 또는 `secondary`
- [ ] 에러: `palette.error`
- [ ] 성공: `palette.success`

### 새 상수 추가 시
- [ ] `gui/constants.py`에 추가
- [ ] 모든 관련 파일에서 사용
- [ ] 매직 넘버 제거

---

## 변경 이력

### Phase 2: Core UI Refactor (2026-03-14)
- ✓ 색상 팔레트 정의 (Dark/Light)
- ✓ UI 상수 중앙화
- ✓ 버튼 스타일 표준화
- ✓ 모든 위젯 스타일 적용

### 계획 중
- Phase 3: 고급 기능 (접근성, 애니메이션)
- Phase 4: 테스트 및 문서화
