# Tech Stack: pdf-tool

## Runtime

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | >= 3.13 | Runtime |
| pypdf | >= 6.8.0 | PDF read/write/manipulation |
| typer | >= 0.24.1 | CLI framework (Click-based) |
| rich | >= 13.0.0 | Terminal formatting |
| reportlab | >= 4.4.10 | Watermark overlay generation |
| Pillow | >= 12.1.1 | Image watermark processing |

## Development

| Tool | Version | Purpose |
|------|---------|---------|
| pytest | >= 8.0.0 | Test framework |
| pytest-cov | >= 6.0.0 | Coverage measurement |
| ruff | >= 0.9.0 | Linter & formatter |

## Build & Deploy

| Tool | Purpose |
|------|---------|
| hatchling | PEP 517/518 build backend |
| uv | Package manager (recommended) |
| PyInstaller | Windows EXE packaging |
| GitHub Actions | CI/CD (Windows EXE auto-build) |

## Code Quality

- Ruff rules: E, F, W, I, N, UP, B, A, SIM
- Max line length: 99
- Korean test function names allowed (N802 exemption)

## Design Patterns

- Facade: cli.py orchestrates all commands
- Strategy: resize modes (fit/stretch/fill)
- Factory: conftest.py create_pdf fixture

## Exception Hierarchy

```
PDFToolError
├── FileValidationError
├── PageRangeError
└── PDFProcessingError
```
