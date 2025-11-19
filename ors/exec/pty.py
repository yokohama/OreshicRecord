import re
import sys
import os
import pty
import tty
import termios
import signal
import fcntl
import select

import ors.core


# optional: better column width for CJK etc.
try:
    from wcwidth import wcswidth as _wcswidth
except Exception:
    _wcswidth = None

# ---- input/output trace state (for PTY interactive) ----
_KBD_BUF: list[str] = []
_IN_SECRET = False
_LAST_OUT_TAIL = ""
_PASS_PROMPT_RE = re.compile(r"(?i)(password|passphrase).{0,40}:\s*$")


def run(cmd_list, fp, silent):
    global _KBD_BUF, _IN_SECRET, _LAST_OUT_TAIL

    master_fd, slave_fd = pty.openpty()
    ors.core.table.set_winsize(master_fd)

    stdin_fd = sys.stdin.fileno()
    try:
        old_tty = termios.tcgetattr(stdin_fd)
        tty.setraw(stdin_fd)
    except Exception:
        old_tty = None

    def _on_winch(signum, frame):
        ors.core.table.set_winsize(master_fd)

    old_winch = signal.getsignal(signal.SIGWINCH)
    signal.signal(signal.SIGWINCH, _on_winch)

    try:
        pid = os.fork()
        if pid == 0:  # child
            try:
                os.setsid()
                fcntl.ioctl(slave_fd, termios.TIOCSCTTY, 0)
                os.dup2(slave_fd, 0)
                os.dup2(slave_fd, 1)
                os.dup2(slave_fd, 2)
                os.close(master_fd)
                os.close(slave_fd)
                os.execvp(cmd_list[0], cmd_list)
            except Exception as e:
                print(f"[ors: child error] {e}", file=sys.stderr)
                os._exit(1)

        # parent
        os.close(slave_fd)
        proc_pid = pid
        _KBD_BUF = []
        _IN_SECRET = False
        _LAST_OUT_TAIL = ""

        def _flush_kbd_line():
            """Enter 押下時に、入力行を md に書く（パスワード中は書かない）"""
            global _KBD_BUF, _IN_SECRET
            if not silent and not _IN_SECRET:
                line = "".join(_KBD_BUF)
                if line.strip():
                    fp.write(line + "\n")
                    fp.flush()
            _KBD_BUF = []
            if _IN_SECRET:
                _IN_SECRET = False

        def _push_out_and_scan(decoded: str):
            """出力を端末/ファイルへ流しつつ、末尾に password プロンプトがないか検知"""
            global _LAST_OUT_TAIL, _IN_SECRET
            # 端末へ
            os.write(sys.stdout.fileno(), decoded.encode(errors="replace"))
            # ファイルへ
            if not silent:
                fp.write(ors.core.clean.term_chunk(decoded))
                fp.flush()
            # 末尾更新（直近 200 文字だけ保持）
            _LAST_OUT_TAIL = (_LAST_OUT_TAIL + decoded)[-200:]
            if _PASS_PROMPT_RE.search(_LAST_OUT_TAIL):
                _IN_SECRET = True  # 次の改行までの入力は記録しない

        while True:
            rlist, _, _ = select.select([master_fd, stdin_fd], [], [], 0.05)

            if master_fd in rlist:
                try:
                    data = os.read(master_fd, 4096)
                except OSError:
                    data = b""
                if not data:
                    break
                decoded = data.decode(errors="replace")
                _push_out_and_scan(decoded)

            if stdin_fd in rlist:
                try:
                    kbd_bytes = os.read(stdin_fd, 4096)
                except OSError:
                    kbd_bytes = b""
                if not kbd_bytes:
                    break

                # そのまま子PTYへ
                os.write(master_fd, kbd_bytes)

                # 入力の可視化（md 記録用・パスワードは抑止）
                try:
                    kbd_text = kbd_bytes.decode("utf-8", errors="ignore")
                except Exception:
                    kbd_text = ""

                for ch in kbd_text:
                    if ch in ("\r", "\n"):
                        _flush_kbd_line()
                    elif ch in ("\b", "\x7f"):  # Backspace / DEL
                        if _KBD_BUF:
                            _KBD_BUF.pop()
                    elif ch == "\x03":  # ^C
                        try:
                            os.killpg(proc_pid, signal.SIGINT)
                        except ProcessLookupError:
                            pass
                    elif ch == "\x1a":  # ^Z
                        try:
                            os.killpg(proc_pid, signal.SIGTSTP)
                        except ProcessLookupError:
                            pass
                    elif ch == "\x1c":  # ^\
                        try:
                            os.killpg(proc_pid, signal.SIGQUIT)
                        except ProcessLookupError:
                            pass
                    else:
                        # 目で見える文字だけ（ESC始まり等は除外）
                        if 0x20 <= ord(ch) <= 0x7E or (_wcswidth and _wcswidth(ch) > 0):
                            _KBD_BUF.append(ch)
                        # それ以外（カーソルキー等のエスケープ列）は記録しない

            # child exit?
            try:
                pid_done, _ = os.waitpid(proc_pid, os.WNOHANG)
                if pid_done != 0:
                    break
            except ChildProcessError:
                break

        # drain the rest
        while True:
            try:
                data = os.read(master_fd, 4096)
                if not data:
                    break
                decoded = data.decode(errors="replace")
                _push_out_and_scan(decoded)
            except OSError:
                break

        _KBD_BUF = []

    finally:
        try:
            if old_tty:
                termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_tty)
        except Exception:
            pass
        try:
            signal.signal(signal.SIGWINCH, old_winch)
        except Exception:
            pass
        try:
            os.close(master_fd)
        except Exception:
            pass
