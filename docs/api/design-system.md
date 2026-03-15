# Design System API Reference

SPEC-UI-MAC-001: macOS Style UI Redesign — v0.2.0

## Overview

The pdf-tool design system is built on Apple Human Interface Guidelines (HIG).
All visual tokens, animations, and accessibility utilities are defined in standalone modules
that can be imported independently of the GUI framework.

---

## design_tokens.py

Module: `pdf_tool.gui.design_tokens`

Defines Apple HIG-compliant design tokens: colors, typography, spacing, corner radii, and animation timing.

### SystemColors

```
class SystemColors(frozen dataclass)
```

Stores system background colors for dark or light mode.

| Attribute | Type | Description |
|-----------|------|-------------|
| `system_background` | `str` | Primary background (hex) |
| `secondary_system_background` | `str` | Secondary background (hex) |
| `tertiary_system_background` | `str` | Tertiary background (hex) |

**Constants:**

- `DARK_COLORS` — Dark mode system colors (`#1C1C1E` base)
- `LIGHT_COLORS` — Light mode system colors (`#F2F2F7` base)

### AccentColors

```
class AccentColors
```

Apple system accent colors as class-level string constants.

| Constant | Value | Usage |
|----------|-------|-------|
| `BLUE` | `#007AFF` | Primary actions |
| `GREEN` | `#34C759` | Success states |
| `RED` | `#FF3B30` | Destructive actions |
| `ORANGE` | `#FF9500` | Warnings |
| `YELLOW` | `#FFCC00` | Highlights |
| `PURPLE` | `#AF52DE` | Special states |
| `GRAY` | `#8E8E93` | Disabled / secondary |

### Typography

```
class Typography
```

San Francisco typography scale (Apple HIG 2024).

| Constant | Size (pt) | Weight | Usage |
|----------|-----------|--------|-------|
| `LARGE_TITLE` | 34 | Regular | Hero headings |
| `TITLE_1` | 28 | Regular | Page titles |
| `TITLE_2` | 22 | Regular | Section headings |
| `TITLE_3` | 20 | Regular | Sub-section headings |
| `HEADLINE` | 17 | Bold | Emphasized labels |
| `BODY` | 17 | Regular | Body text |
| `CALLOUT` | 16 | Regular | Callout text |
| `SUBHEADLINE` | 15 | Regular | Secondary labels |
| `FOOTNOTE` | 13 | Regular | Footnotes |
| `CAPTION` | 12 | Regular | Captions |

**Font family fallback chain:**

1. macOS: `SF Pro Text` / `SF Pro Display` / `SF Mono`
2. Windows: `Segoe UI`
3. Linux: `Inter` or `Cantarell`

### Spacing

```
class Spacing
```

8-point grid spacing system.

| Constant | Value (pt) | Usage |
|----------|-----------|-------|
| `XXS` | 2 | Micro gaps |
| `XS` | 4 | Icon padding |
| `SM` | 8 | Base unit |
| `MD` | 16 | Component padding |
| `LG` | 24 | Section spacing |
| `XL` | 32 | Page margins |
| `XXL` | 48 | Major sections |

### CornerRadius

```
class CornerRadius
```

Apple HIG corner radius tokens.

| Constant | Value (pt) | Usage |
|----------|-----------|-------|
| `SMALL` | 4 | Tags, badges |
| `MEDIUM` | 8 | Cards, inputs |
| `LARGE` | 12 | Panels |
| `EXTRA_LARGE` | 16 | Sheets |
| `FULL` | 9999 | Pills, buttons |

### AnimationTiming

```
class AnimationTiming
```

Animation duration constants (seconds).

| Constant | Value (s) | Usage |
|----------|----------|-------|
| `INSTANT` | 0.0 | No animation |
| `FAST` | 0.15 | Hover states |
| `NORMAL` | 0.25 | Page transitions |
| `SLOW` | 0.35 | Modal appear |
| `VERY_SLOW` | 0.5 | Complex transitions |

---

## animation.py

Module: `pdf_tool.gui.animation`

Pure Python animation engine. No CustomTkinter dependency. Integrates with tkinter's `after()` loop.

### Easing

```
class Easing
```

Static easing functions. All accept `t: float` in range `[0.0, 1.0]` and return a clamped interpolation value.

| Method | Formula | Usage |
|--------|---------|-------|
| `linear(t)` | `f(t) = t` | Constant speed |
| `ease_in(t)` | `f(t) = t²` | Accelerating |
| `ease_out(t)` | `f(t) = 1 - (1-t)²` | Decelerating |
| `ease_in_out(t)` | `f(t) = 3t² - 2t³` | Smooth start and end |

### Animation

```
class Animation
```

Single animation instance: interpolates from `start_value` to `end_value` over `duration` seconds.

**Constructor:**

```python
Animation(
    start_value: float,
    end_value: float,
    duration: float,
    easing_func: Callable[[float], float] = Easing.ease_in_out,
    on_update: Callable[[float], None] | None = None,
    on_complete: Callable[[], None] | None = None,
)
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `animation_id` | `str` | UUID for tracking |
| `is_complete` | `bool` | True when finished |

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `update(elapsed: float)` | `float` | Advance animation; returns current value |

### Animator

```
class Animator
```

Manages multiple concurrent animations. Drives them via tkinter's `after()` loop.

**Constructor:**

```python
Animator(root: tk.Tk | tk.Widget, frame_rate: int = 60)
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `add(animation: Animation)` | `str` | Register animation; returns `animation_id` |
| `cancel(animation_id: str)` | `None` | Cancel a running animation |
| `cancel_all()` | `None` | Cancel all animations |
| `start()` | `None` | Begin animation loop |
| `stop()` | `None` | Stop animation loop |

**Example:**

```python
from pdf_tool.gui.animation import Animation, Animator, Easing

animator = Animator(root)
anim = Animation(
    start_value=0.0,
    end_value=1.0,
    duration=0.25,
    easing_func=Easing.ease_out,
    on_update=lambda v: widget.configure(fg_color=interpolate_color(v)),
)
animator.add(anim)
animator.start()
```

---

## accessibility.py

Module: `pdf_tool.gui.accessibility`

Keyboard navigation, accessibility labels, focus management, and high-contrast mode. Pure logic; no widget dependencies.

### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `TAB_KEY` | `<Tab>` | Forward focus |
| `SHIFT_TAB_KEY` | `<Shift-Tab>` | Backward focus |
| `ENTER_KEY` | `<Return>` | Activate |
| `SPACE_KEY` | `<space>` | Activate (alternative) |
| `ESCAPE_KEY` | `<Escape>` | Close / dismiss |

### FocusManager

```
class FocusManager
```

Manages Tab/Shift-Tab focus cycling across registered widgets.

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `register(widget)` | `None` | Add widget to focus chain |
| `clear()` | `None` | Reset focus chain |
| `focus_next()` | `object \| None` | Move to next widget; cycles |
| `focus_previous()` | `object \| None` | Move to previous widget; cycles |

### AccessibilityLabel

```
class AccessibilityLabel
```

Associates accessibility metadata with a widget identifier.

**Constructor:**

```python
AccessibilityLabel(
    widget_id: str,
    label: str,
    hint: str = "",
    role: str = "button",
)
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `widget_id` | `str` | Widget identifier |
| `label` | `str` | Screen reader label |
| `hint` | `str` | Additional description |
| `role` | `str` | ARIA-equivalent role |

### AccessibilityManager

```
class AccessibilityManager
```

Central registry for all accessibility labels in the application.

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `register(label: AccessibilityLabel)` | `None` | Register a label |
| `get_label(widget_id: str)` | `AccessibilityLabel \| None` | Retrieve by widget ID |
| `get_description(widget_id: str)` | `str` | Formatted label + hint string |

### HighContrastMode

```
class HighContrastMode
```

Detects and provides high-contrast color overrides.

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `is_enabled()` | `bool` | Check if high contrast is active |
| `get_background()` | `str` | High-contrast background hex |
| `get_foreground()` | `str` | High-contrast foreground hex |
| `get_accent()` | `str` | High-contrast accent hex |

### KeyboardNavigationMixin

```
class KeyboardNavigationMixin
```

Mixin providing macOS keyboard shortcut registration (Cmd+1~9 for page navigation).

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `setup_keyboard_navigation(root, page_callbacks)` | `None` | Bind Cmd+1~9 shortcuts |
| `teardown_keyboard_navigation(root)` | `None` | Remove bindings |

---

## widgets/

### macos_button.py

Module: `pdf_tool.gui.widgets.macos_button`

macOS-style button with Primary, Secondary, and Destructive variants.

#### MacOSButtonStyle

```
class MacOSButtonStyle
```

Computes button colors and dimensions from style + size tokens.

**Constructor:**

```python
MacOSButtonStyle(
    style: str = "primary",   # "primary" | "secondary" | "destructive"
    size: str = "regular",    # "mini" | "regular" | "large"
)
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `bg_color` | `str` | Normal background color |
| `text_color` | `str` | Text color |
| `hover_color` | `str` | Hover state background |
| `height` | `int` | Button height in pt |
| `corner_radius` | `int` | Corner radius in pt |

**Constants:**

| Constant | Value | Description |
|----------|-------|-------------|
| `HOVER_ANIMATION_DURATION` | `0.15` | Hover fade duration (s) |
| `CLICK_SCALE` | `0.98` | Press scale factor |
| `CLICK_ANIMATION_DURATION` | `0.1` | Click animation duration (s) |

---

### segmented_control.py

Module: `pdf_tool.gui.widgets.segmented_control`

Capsule-shaped segmented control — pure state management logic.

#### SegmentedControlState

```
class SegmentedControlState
```

**Constructor:**

```python
SegmentedControlState(
    values: list[str],
    on_change: Callable[[str], None] | None = None,
)
```

Raises `ValueError` if `values` is empty.

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `get_value()` | `str` | Currently selected segment |
| `set_value(value: str)` | `None` | Select a segment; fires `on_change` if changed |

---

### sidebar_item.py

Module: `pdf_tool.gui.widgets.sidebar_item`

Sidebar navigation item with active state, tint color, and vibrancy styling.

Refer to module docstring for full attribute and method listing.

---

## Cross-Platform Compatibility

| Feature | macOS | Windows | Linux |
|---------|-------|---------|-------|
| Font | SF Pro / SF Mono | Segoe UI | Inter / Cantarell |
| Theme detection | `darkdetect` | `darkdetect` | `darkdetect` |
| Animations | Full | Full | Full |
| Keyboard shortcuts | Cmd+1~9 | Ctrl+1~9 (fallback) | Ctrl+1~9 (fallback) |
| High contrast | System detect | System detect | Manual |

---

*Generated for SPEC-UI-MAC-001 v0.2.0 — 2026-03-15*
