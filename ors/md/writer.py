import os
from pathlib import Path
from shlex import quote

import ors.core


# 末尾未改行の残バッファを flush
def md_close_output(fp):
    pending = ors.core.clean.clean_term_flush()
    if pending:
        fp.write(pending)
    fp.write("```\n\n")


def _get_active_track() -> str | None:
    name = os.getenv("ORESHIC_TRACK")

    if name:
        name = name.strip()
        return name or None

    return None


def prepare_md_file(cmd):
    active_track_name = _get_active_track()

    if active_track_name:
        outdir = ors.core.get_track_dir().expanduser()
        outdir.mkdir(parents=True, exist_ok=True)
        return outdir / f"{active_track_name}.md"

    base_name = Path(cmd).name.replace("/", "_")
    outdir = ors.core.settings.get_command_dir().expanduser()
    outdir.mkdir(parents=True, exist_ok=True)

    return outdir / f"{base_name}.md"


def md_header(fp, message, prompt, cmd_list):
    fp.write(f"## {message or '(no message)'}\n\n")
    fp.write("```bash\n")
    fp.write(f"{prompt}{' '.join(quote(c) for c in cmd_list)}\n")
    fp.write("```\n\n")
    fp.write("```\n")
