import re
import os
from pathlib import Path
from shlex import quote

import ors.core


_FENCE_RE = re.compile(r'^\s*```')


# trackがセットされているかの確認
def _get_active_track() -> str | None:
    path = Path(ors.core.settings.get_track_name_file())
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            name = f.read()
            return name.strip()
    else:
        return None


# .mdの中のエントリー数をカウントする
def count_md_sections(md_path: Path) -> int:
    try:
        in_fence = False
        count = 0
        with md_path.open("r", encoding="utf-8", errors="replace") as fp:
            for raw in fp:
                line = raw.rstrip("\n")
                if _FENCE_RE.match(line):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                if line.lstrip().startswith("## "):  # スペース必須で誤検知低減
                    count += 1
        return count
    except Exception:
        return 0


# 各エントリ（フェンス外の '## ' 行を起点）の [start, end) 行インデックス
def index_entry_ranges(md_path: Path) -> list[tuple[int, int]]:
    lines = md_path.read_text(
        encoding="utf-8",
        errors="replace"
    ).splitlines(keepends=False)
    in_fence = False
    starts: list[int] = []
    for i, line in enumerate(lines):
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.lstrip().startswith("## "):
            starts.append(i)
    ranges: list[tuple[int, int]] = []
    for j, s in enumerate(starts):
        e = starts[j + 1] if j + 1 < len(starts) else len(lines)
        ranges.append((s, e))
    return ranges


def prepare_file(cmd):
    active_track_name = _get_active_track()

    if active_track_name:
        outdir = ors.core.settings.get_track_dir().expanduser()
        outdir.mkdir(parents=True, exist_ok=True)
        return outdir / f"{active_track_name}.md"

    base_name = Path(cmd).name.replace("/", "_")
    outdir = ors.core.settings.get_command_dir().expanduser()
    outdir.mkdir(parents=True, exist_ok=True)

    return outdir / f"{base_name}.md"


def write_header(fp, message, prompt, cmd_list):
    fp.write(f"## {message or '(no message)'}\n\n")
    fp.write("```bash\n")
    fp.write(f"{prompt}{' '.join(quote(c) for c in cmd_list)}\n")
    fp.write("```\n\n")
    fp.write("```\n")


# 末尾未改行の残バッファを flush
def close_output(fp):
    pending = ors.core.clean.term_flush()
    if pending:
        fp.write(pending)
    fp.write("```\n\n")
