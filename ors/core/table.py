import shutil
import struct
import fcntl
import termios
import sys


# optional: better column width for CJK etc.
try:
    from wcwidth import wcswidth as _wcswidth
except Exception:
    _wcswidth = None


def _pad_to_width(s: str, width: int) -> str:
    s = "" if s is None else str(s)
    w = _disp_width(s)
    if w >= width:
        return s
    return s + " " * (width - w)


def _disp_width(s: str) -> int:
    if s is None:
        return 0
    if _wcswidth:
        w = _wcswidth(str(s))
        return w if w >= 0 else len(str(s))
    return len(str(s))


def _winsize_from_stdout():
    try:
        s = struct.pack("HHHH", 0, 0, 0, 0)
        rows, cols, _, _ = struct.unpack(
            "HHHH", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s)
        )
        return rows, cols
    except Exception:
        return 24, 80


def ascii_table(
        headers: list[str], rows: list[list[str]],
        max_total_width: int | None = None) -> str:

    cols = len(headers)
    col_widths = [max(_disp_width(h), 1) for h in headers]
    for row in rows:
        for i in range(cols):
            col_widths[i] = max(
                col_widths[i],
                _disp_width(row[i] if i < len(row) else "")
            )

    if max_total_width is None:
        try:
            max_total_width = shutil.get_terminal_size().columns
        except Exception:
            max_total_width = 120

    base_padding = 3 * cols + 1
    total_width = sum(col_widths) + base_padding
    min_widths = [max(2, _disp_width(h)) for h in headers]
    idx_order = list(range(cols - 1, -1, -1))
    while total_width > max_total_width and any(col_widths[i] > min_widths[i] for i in range(cols)):
        for i in idx_order:
            if col_widths[i] > min_widths[i]:
                col_widths[i] -= 1
                total_width = sum(col_widths) + base_padding
                if total_width <= max_total_width:
                    break
        else:
            break

    def hline(ch: str = "-") -> str:
        return "+" + "+".join(ch * (w + 2) for w in col_widths) + "+"

    top, mid = hline("-"), hline("=")
    out = [
        top,
        "| " + " | ".join(_pad_to_width(
            h, col_widths[i]) for i, h in enumerate(headers)) + " |",
        mid
    ]
    for row in rows:
        out.append("| " + " | ".join(
            _pad_to_width(
                row[i] if i < len(row) else "",
                col_widths[i]) for i in range(cols)
        ) + " |")
        out.append(top)
    return "\n".join(out)


def set_winsize(fd):
    rows, cols = _winsize_from_stdout()
    s = struct.pack("HHHH", rows, cols, 0, 0)
    try:
        fcntl.ioctl(fd, termios.TIOCSWINSZ, s)
    except Exception:
        pass
