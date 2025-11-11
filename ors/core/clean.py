import re


# ==========================================================
# ANSI/TTY クリーンアップ
# ==========================================================
_ANSI_CSI = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
_OSC = re.compile(r'\x1B\][^\x07]*(\x07|\x1B\\)')

# ステートフル・クリーナ
try:
    _CLEAN_STATE
except NameError:
    _CLEAN_STATE = {"buf": [], "pos": 0}


def term_flush() -> str:
    """未改行で残っている最終行をフラッシュして返す（改行付き）。"""
    buf = _CLEAN_STATE.get("buf", [])
    pos = _CLEAN_STATE.get("pos", 0)
    if pos > 0:
        s = "".join(buf[:pos]) + "\n"
    else:
        s = ""
    _CLEAN_STATE["buf"] = []
    _CLEAN_STATE["pos"] = 0
    return s


def term_chunk(s: str) -> str:
    """ステートフル版：CR上書きで残りを切り捨てる実装"""
    if not s:
        return s

    s = _OSC.sub("", s)
    s = _ANSI_CSI.sub("", s)
    s = s.replace("\r\n", "\n")

    out_parts: list[str] = []
    buf = _CLEAN_STATE["buf"]
    pos = _CLEAN_STATE["pos"]

    def flush_line():
        nonlocal buf, pos
        if pos > 0:
            out_parts.append("".join(buf[:pos]))
        else:
            out_parts.append("")
        out_parts.append("\n")
        buf = []
        pos = 0

    for ch in s:
        if ch == "\n":
            flush_line()
        elif ch == "\r":
            pos = 0
        elif ch == "\b" or ch == "\x7f":
            if pos > 0:
                del buf[pos - 1]
                pos -= 1
        else:
            if pos < len(buf):
                buf[pos] = ch
            else:
                buf.append(ch)
            pos += 1

    _CLEAN_STATE["buf"] = buf
    _CLEAN_STATE["pos"] = pos
    return "".join(out_parts)
