# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/taehyunkim/pdf_tool/pdf_tool_entry.py'],
    pathex=['/Users/taehyunkim/pdf_tool/src'],
    binaries=[],
    datas=[],
    hiddenimports=['pypdf', 'typer', 'typer.core', 'typer.main', 'click', 'rich', 'rich.console', 'rich.table', 'reportlab', 'reportlab.pdfgen', 'reportlab.pdfgen.canvas', 'reportlab.lib.pagesizes', 'PIL', 'PIL.Image'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy', 'pandas', 'test', 'unittest', 'pytest'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pdf-tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
