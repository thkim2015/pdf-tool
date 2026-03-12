# Project Structure: pdf-tool

## Directory Layout

```
pdf_tool/
├── src/pdf_tool/              # Main package
│   ├── __init__.py            # Version (0.1.0)
│   ├── cli.py                 # Typer CLI entry point (440 lines)
│   ├── commands/              # 8 command implementations
│   │   ├── cut.py             # Page extraction
│   │   ├── merge.py           # PDF merging
│   │   ├── split.py           # PDF splitting
│   │   ├── rotate.py          # Page rotation
│   │   ├── resize.py          # Page resizing
│   │   ├── compress.py        # File compression
│   │   ├── watermark.py       # Watermark application
│   │   └── info.py            # Metadata management
│   ├── core/                  # Core services
│   │   ├── exceptions.py      # 4 exception classes
│   │   ├── validators.py      # Input validation
│   │   ├── page_range.py      # Page range parser ("1,3,5-10")
│   │   ├── page_sizes.py      # Paper size definitions
│   │   ├── pdf_handler.py     # PDF I/O utilities
│   │   └── watermark_generator.py  # ReportLab overlay generation
│   └── utils/
│       ├── file_utils.py      # Output filename generation
│       └── logging.py         # Rich-based terminal output
│   └── gui/                   # GUI module (SPEC-UI-001)
│       ├── app.py             # CTk main application + sidebar
│       ├── theme.py           # Dark/light theme settings
│       ├── pages/             # 8 operation pages + base
│       │   ├── base_page.py   # Common page logic
│       │   ├── *_page.py      # Pure logic per operation
│       │   └── *_page_widget.py # CTk widget per operation
│       └── widgets/           # Reusable widgets
│           ├── file_picker.py # File selection + drag-and-drop
│           ├── progress_bar.py # Indeterminate progress
│           ├── page_range_input.py # Page range input
│           ├── file_list.py   # Multi-file list (merge)
│           ├── result_display.py # Success/error display
│           ├── pdf_preview.py   # PDF first-page rendering logic
│           └── pdf_preview_widget.py # Preview thumbnail widget
├── tests/                     # 22 test files (~3,200 lines)
│   ├── conftest.py            # pytest fixtures
│   └── test_*.py              # Per-module tests
├── .github/workflows/
│   └── build-exe.yml          # Windows EXE CI/CD
├── pyproject.toml             # Project config
├── build_exe.py               # PyInstaller build script
└── pdf_tool_entry.py          # PyInstaller entry point
```

## Architecture

```
CLI Layer (cli.py)          GUI Layer (gui/app.py)
    ↓                           ↓
Command Layer (commands/*.py) ←──┘
    ↓
Core Services (core/*.py)
    ↓
Utilities (utils/*.py)
    ↓
External: pypdf, reportlab, Pillow, rich, customtkinter, pypdfium2
```

## Code Metrics

- Source: ~4,750 lines (54 files)
- Tests: ~3,200 lines (22 files)
- Total: ~7,950 lines
