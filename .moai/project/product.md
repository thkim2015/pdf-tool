# Product: pdf-tool

## Overview

PDF 파일을 조작할 수 있는 Python CLI + GUI 도구. 페이지 추출, 병합, 분할, 회전, 크기 변경, 압축, 워터마크 적용, 메타데이터 관리 기능을 CLI와 CustomTkinter 기반 GUI로 제공한다.

## Target Users

- PDF 파일을 자주 다루는 사무직 종사자
- 커맨드라인에 익숙한 개발자 및 파워 유저
- PDF 일괄 처리가 필요한 업무 환경
- CLI에 익숙하지 않은 일반 사용자 (GUI)

## Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| Cut | 지정 페이지 추출 | Done |
| Merge | 여러 PDF 병합 | Done |
| Split | 페이지 단위 분할 | Done |
| Rotate | 페이지 회전 (90/180/270) | Done |
| Resize | 용지 크기 변경 (A3/A4/A5/Letter/Legal) | Done |
| Compress | 콘텐츠 스트림 압축 | Done |
| Watermark | 텍스트/이미지 워터마크 | Done |
| Info | 메타데이터 조회/수정 | Done |
| GUI | CustomTkinter 기반 Windows GUI (다크/라이트 테마) | Done |
| PDF Preview | 작업 완료 후 결과 PDF 첫 페이지 썸네일 미리보기 | Done |

## Distribution

- PyPI 패키지 (pip/uv install)
- Windows EXE CLI (PyInstaller, GitHub Actions 자동 빌드)
- Windows EXE GUI (PyInstaller, `--mode gui` 빌드)
- macOS/Linux CLI

## Version

- Current: 0.1.0
- Python: >= 3.13
