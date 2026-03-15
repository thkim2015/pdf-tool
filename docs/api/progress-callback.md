# Progress Callback API

## 개요

ProgressCallback 시스템은 장시간 PDF 작업에 대한 실시간 진행 상황 추적을 지원합니다.
2초 이상 소요되는 작업에서 CLI 및 GUI 모두 자동으로 진행 표시가 활성화됩니다.

## 사용법

### CLI 예시

```python
from pdf_tool.commands import cut_pdf
from pdf_tool.core.progress import ProgressCallback

def my_callback(current: int, total: int) -> None:
    percent = (current / total * 100) if total > 0 else 0
    print(f"진행률: {percent:.1f}%")

result = cut_pdf(
    input_file="large.pdf",
    pages="1,3,5",
    callback=my_callback
)
```

### GUI 통합

GUI 페이지 위젯에서는 `_make_gui_callback()`으로 자동 GUI 업데이트를 생성합니다:

```python
result = operation_function(
    input_file=file_path,
    output=output_path,
    callback=self._make_gui_callback()  # 자동 GUI 업데이트
)
```

## API 레퍼런스

### ProgressCallback

```python
ProgressCallback = Callable[[int, int], None]
```

- `current`: 현재 처리된 페이지 번호 (0-indexed)
- `total`: 전체 페이지 수

### safe_callback

```python
def safe_callback(callback: Optional[ProgressCallback]) -> Callable:
    """callback을 exception-safe하게 래핑합니다."""
```

실행 중 예외가 발생해도 작업이 중단되지 않도록 콜백을 안전하게 래핑합니다.

## ETA 계산

`core/eta.py` 모듈이 ETA를 계산합니다:

- 작업 유형 (cut, merge, split, rotate, resize, compress, watermark, info)
- 파일 크기 및 페이지 수
- 현재 진행 속도

CLI에서는 "ETA 2m 30s" 형식으로, GUI에서는 진행 표시줄과 함께 표시됩니다.

## 지원 명령어

| 명령어 | 콜백 지원 | 비고 |
|--------|-----------|------|
| `cut` | O | 추출 페이지 기준 |
| `merge` | O | 입력 파일 수 기준 |
| `split` | O | 분할 청크 기준 |
| `rotate` | O | 처리 페이지 기준 |
| `resize` | O | 처리 페이지 기준 |
| `compress` | O | 처리 페이지 기준 |
| `watermark` | O | 처리 페이지 기준 |
| `info` | O | 단계 기준 |

## 하위 호환성

모든 명령어는 `callback` 파라미터 없이도 정상 동작합니다:

```python
# callback 없이 사용 (기존 방식, 계속 지원)
result = cut_pdf(input_file="input.pdf", pages="1-5")

# callback 있이 사용 (신규 방식)
result = cut_pdf(input_file="input.pdf", pages="1-5", callback=my_callback)
```
