import shutil
import struct
import fcntl
import termios
import sys
from unicodedata import east_asian_width


# optional: better column width for CJK etc.
try:
    from wcwidth import wcswidth as _wcswidth
except Exception:
    _wcswidth = None


def _pad_to_width(s: str, width: int) -> str:
    s = "" if s is None else str(s)
    w = _disp_width(s)
    if w >= width:
        return s[:width] if len(s) > width else s
    return s + " " * (width - w)


def _disp_width(s: str) -> int:
    if s is None:
        return 0
    return sum(1 + (east_asian_width(c) in "WF") for c in s)


def _winsize_from_stdout():
    try:
        s = struct.pack("HHHH", 0, 0, 0, 0)
        rows, cols, _, _ = struct.unpack(
            "HHHH", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s)
        )
        return rows, cols
    except Exception:
        return 30, 120


def _wrap_cell_content(text: str, width: int) -> list[str]:
    """セル内容を指定幅で改行し、行のリストを返す"""
    if not text:
        return [""]

    # 日本語対応の改行処理
    lines = []
    current_line = ""
    current_width = 0

    for char in text:
        char_width = _disp_width(char)
        if current_width + char_width > width and current_line:
            lines.append(current_line)
            current_line = char
            current_width = char_width
        else:
            current_line += char
            current_width += char_width

    if current_line:
        lines.append(current_line)

    return lines if lines else [""]


def _calculate_column_widths(headers, rows, cols, max_total_width):
    """列幅を計算する"""
    col_widths = [max(_disp_width(h), 1) for h in headers]
    for row in rows:
        for i in range(cols):
            col_widths[i] = max(
                col_widths[i],
                _disp_width(row[i] if i < len(row) else "")
            )

    base_padding = 3 * cols + 1
    total_width = sum(col_widths) + base_padding
    min_widths = [max(3, _disp_width(h)) for h in headers]

    # より積極的な幅縮小アルゴリズム
    if total_width > max_total_width:
        # 利用可能な幅を列数で分配
        available_width = max_total_width - base_padding
        if available_width > sum(min_widths):
            # 最小幅を確保した上で残りを比例配分
            extra_width = available_width - sum(min_widths)
            total_original_extra = sum(max(0, w - min_widths[i])
                                       for i, w in enumerate(col_widths))

            for i in range(cols):
                if total_original_extra > 0:
                    extra_col_width = max(0, col_widths[i] - min_widths[i])
                    extra_for_col = int(
                        extra_width * extra_col_width // total_original_extra
                    )
                    col_widths[i] = min_widths[i] + extra_for_col
                else:
                    col_widths[i] = min_widths[i]
        else:
            # 最小幅でも収まらない場合は均等分割
            col_widths = [
                max(2, available_width // cols) for _ in range(cols)]

    return col_widths


def ascii_table(
        headers: list[str], rows: list[list[str]],
        max_total_width: int | None = None) -> str:

    cols = len(headers)

    if max_total_width is None:
        try:
            max_total_width = shutil.get_terminal_size().columns
        except Exception:
            max_total_width = 120

    col_widths = _calculate_column_widths(headers, rows, cols, max_total_width)

    def hline(ch: str = "-") -> str:
        return "+" + "+".join(ch * (w + 2) for w in col_widths) + "+"

    top, mid = hline("-"), hline("=")
    out = [
        top,
        "| " + " | ".join(_pad_to_width(
            h, col_widths[i]) for i, h in enumerate(headers)) + " |",
        mid
    ]

    # 各行を処理（セル内改行対応）
    for row in rows:
        # 各セルの内容を改行処理
        cell_lines = []
        max_lines = 1

        for i in range(cols):
            cell_content = row[i] if i < len(row) else ""
            wrapped_lines = _wrap_cell_content(cell_content, col_widths[i])
            cell_lines.append(wrapped_lines)
            max_lines = max(max_lines, len(wrapped_lines))

        # 複数行のセルに対応した行を生成
        for line_idx in range(max_lines):
            line_parts = []
            for i in range(cols):
                if line_idx < len(cell_lines[i]):
                    content = cell_lines[i][line_idx]
                else:
                    content = ""
                line_parts.append(_pad_to_width(content, col_widths[i]))

            out.append("| " + " | ".join(line_parts) + " |")

        out.append(top)

    return "\n".join(out)


def set_winsize(fd):
    rows, cols = _winsize_from_stdout()
    s = struct.pack("HHHH", rows, cols, 0, 0)
    try:
        fcntl.ioctl(fd, termios.TIOCSWINSZ, s)
    except Exception:
        pass
