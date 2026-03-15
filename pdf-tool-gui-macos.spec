# -*- mode: python ; coding: utf-8 -*-
# macOS 전용 PyInstaller Spec 파일
# pdf-tool GUI를 macOS .app 번들로 빌드

from PyInstaller.utils.hooks import collect_all
import os

# 프로젝트 경로
project_root = '/Users/taehyunkim/pdf_tool'

# customtkinter 및 모든 관련 리소스 수집
datas = []
binaries = []
hiddenimports = [
    'pypdf',
    'customtkinter',
    'reportlab',
    'reportlab.pdfgen',
    'reportlab.pdfgen.canvas',
    'reportlab.lib.pagesizes',
    'reportlab.lib.units',
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'typer',
    'typer.core',
    'rich',
    'rich.console',
    'darkdetect',
]

# customtkinter 데이터 수집
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# PIL 데이터 수집
tmp_ret = collect_all('PIL')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

a = Analysis(
    [os.path.join(project_root, 'pdf_tool_gui_entry.py')],
    pathex=[os.path.join(project_root, 'src')],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'scipy', 'pandas', 'test', 'unittest', 'pytest'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pdf-tool-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,  # macOS arg emulation
    target_arch=None,
    codesign_identity=None,  # 선택사항: "your-team-id" 로 설정하여 코드 서명
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pdf-tool-gui',
)

app = BUNDLE(
    coll,
    name='pdf-tool-gui.app',
    icon=None,  # 선택사항: icon='path/to/icon.icns'로 설정하여 아이콘 추가
    bundle_identifier='com.taehyunkim.pdf-tool-gui',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'NSRequiresIPhoneOS': False,
        'LSMinimumSystemVersion': '10.13.0',  # macOS 10.13+
        'CFBundleShortVersionString': '0.2.0',
        'CFBundleVersion': '0.2.0',
    },
)
