import sys
import subprocess
import shlex
from pathlib import Path

import ors.core.settings
from ors.core.image_display import display_content_with_images


def _get_path_by_mode(mode):
    if mode == "command":
        path = ors.core.settings.get_command_dir()
    else:
        path = ors.core.settings.get_track_dir()

    return path


def _get_entry_name(mode, file_id):
    path = _get_path_by_mode(mode)
    files = list_files_sorted(path)
    return path, ors.features.search.resolve_name_by_id(file_id, files, mode)


def _get_entries(mode, file_id):
    path, name = _get_entry_name(mode, file_id)
    return ors.features.search.load_entries_generic(path, name)


def list_files_sorted(path) -> list[Path]:
    outdir = path.expanduser()
    if not outdir.exists():
        return []
    return sorted(outdir.glob("*.md"))


def list_files_ascii(mode):
    path = _get_path_by_mode(mode)
    headers = ["ID", "Name", "Count"]
    rows = []
    for idx, p in enumerate(list_files_sorted(path), start=1):
        rows.append([str(idx), p.stem, str(ors.core.md.count_md_sections(p))])
    print(ors.core.table.ascii_table(headers, rows))


def search_file_ascii_by_id(mode, file_id: str):
    entries = _get_entries(mode, file_id)
    headers = ["ID", "Title", "Command"]
    rows = [[str(i), e["title"], e["cmd"]] for i, e in enumerate(entries, 1)]
    print(ors.core.table.ascii_table(headers, rows))


def show_entry_detail_by_ids(mode, file_id: str, entry_id: str):
    entries = _get_entries(mode, file_id)
    try:
        eid = int(entry_id)
        e = entries[eid - 1]
    except Exception:
        print("[ors] invalid entry id", file=sys.stderr)
        sys.exit(2)

    # MDファイルのパスを取得（画像表示のため）
    path, name = _get_entry_name(mode, file_id)
    md_path = path / f"{name}.md"

    # 表示内容を構築
    content = f"# {e['title']}\n\n"
    content += "```bash\n"
    if e['cmd']:
        content += e['cmd'] + "\n"
    content += "\n"
    content += (e['out'] or "(no output)") + "\n"
    content += "```\n\n"

    # 画像対応の表示関数を使用
    display_content_with_images(content, md_path)


# エントリ削除。削除後の Count が 0 ならファイルも削除（command）
def delete_entry_by_ids(mode, file_id: str, entry_id: str):
    path, name = _get_entry_name(mode, file_id)
    md_path = path / f"{name}.md"
    if not md_path.exists():
        print(f"[ors] not found: {md_path}", file=sys.stderr)
        sys.exit(2)

    ranges = ors.core.md.index_entry_ranges(md_path)
    try:
        idx = int(entry_id)
        start, end = ranges[idx - 1]
    except Exception:
        print("[ors] invalid entry id", file=sys.stderr)
        sys.exit(2)

    lines = md_path.read_text(
        encoding="utf-8",
        errors="replace"
    ).splitlines(keepends=True)
    new_lines = lines[:start] + lines[end:]
    md_path.write_text("".join(new_lines), encoding="utf-8")

    remaining = ors.core.md.count_md_sections(md_path)
    if remaining == 0:
        try:
            md_path.unlink()
            msg = f"[ors] deleted entry {idx} and removed file: {name}.md " \
                  f"(Count=0)"
            print(msg)
        except Exception as e:
            print(
                f"[ors] deleted entry {idx}, but failed to remove file: {e}",
                file=sys.stderr
            )
    else:
        msg = f"[ors] deleted: {name} entry {idx} " \
              f"(remaining Count={remaining})"
        print(msg)


def run_entry_by_ids(
    mode, file_id: str, entry_id: str,
        message_override: str | None, quiet: bool):

    entries = _get_entries(mode, file_id)
    try:
        eid = int(entry_id)
        e = entries[eid - 1]
    except Exception:
        print("[ors] invalid entry id", file=sys.stderr)
        sys.exit(2)

    if not e["cmd"]:
        print("[ors] selected entry has no command line", file=sys.stderr)
        sys.exit(2)

    cmd_list = shlex.split(e["cmd"])
    print(f"[ors] executing: {' '.join(cmd_list)}")
    try:
        subprocess.run(cmd_list)
    except FileNotFoundError:
        print(f"[ors] command not found: {cmd_list[0]}", file=sys.stderr)
        sys.exit(2)
    except Exception as ex:
        print(f"[ors] execution failed: {ex}", file=sys.stderr)
        sys.exit(2)
