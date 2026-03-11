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
├── tests/                     # 17 test files (~2,600 lines)
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
CLI Layer (cli.py)
    ↓
Command Layer (commands/*.py)
    ↓
Core Services (core/*.py)
    ↓
Utilities (utils/*.py)
    ↓
External: pypdf, reportlab, Pillow, rich
```

## Code Metrics

- Source: ~3,140 lines (21 files)
- Tests: ~2,600 lines (17 files)
- Total: ~5,740 lines
