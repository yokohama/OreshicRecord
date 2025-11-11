import sys
import os
import signal
import subprocess
import shutil

import ors.core


def _maybe_wrap_stdbuf(cmd_list):
    if os.name != "nt" and shutil.which("stdbuf"):
        return ["stdbuf", "-oL", "-eL", *cmd_list]
    return cmd_list


def run_stream_tee(cmd_list, fp, silent):
    cmd_list = _maybe_wrap_stdbuf(cmd_list)
    proc = subprocess.Popen(
        cmd_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    def forward(sig, frame):
        try:
            proc.send_signal(sig)
        except Exception:
            pass
    old_handler = signal.signal(signal.SIGINT, forward)
    try:
        while True:
            out = proc.stdout.readline()
            if out:
                sys.stdout.write(out)
                sys.stdout.flush()
                if not silent:
                    fp.write(ors.core.clean.clean_term_chunk(out))
                    fp.flush()
            err = proc.stderr.readline()
            if err:
                sys.stderr.write(err)
                sys.stderr.flush()
                if not silent:
                    fp.write(ors.core.clean.clean_term_chunk(err))
                    fp.flush()
            if not out and not err and proc.poll() is not None:
                break
    finally:
        signal.signal(signal.SIGINT, old_handler)
    return proc.returncode
