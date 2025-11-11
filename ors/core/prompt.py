import os


def build():
    user = os.getenv("USER", "<unknown>")
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    cwd_display = "~" + cwd[len(home):] if cwd.startswith(home) else cwd
    host = os.uname().nodename
    return f"{user}@{cwd_display} {host}$ "
