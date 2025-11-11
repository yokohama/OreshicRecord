import sys
import os
import shlex
from pathlib import Path

import ors.features
import ors.core
import ors.exec
import ors.md

# ==========================================================
# Command機能
# ==========================================================


def _list_command_files_sorted() -> list[Path]:
    outdir = ors.core.settings.get_command_dir().expanduser()
    if not outdir.exists():
        return []
    return sorted(outdir.glob("*.md"))


def _search_command_file_ascii_by_id(id_str: str):
    files = _list_command_files_sorted()
    name = ors.features.search.resolve_name_by_id(id_str, files, "command")
    entries = ors.features.search.load_entries_generic(
        ors.core.settings.get_command_dir(),
        name
    )
    headers = ["ID", "Title", "Command"]
    rows = [[str(i), e["title"], e["cmd"]] for i, e in enumerate(entries, 1)]
    print(ors.core.table.ascii_table(headers, rows))


def _list_command_files_ascii():
    headers = ["ID", "Name", "Count"]
    rows = []
    for idx, p in enumerate(_list_command_files_sorted(), start=1):
        rows.append([
            str(idx),
            p.stem,
            str(ors.md.loader.count_md_sections(p))
        ])
    print(ors.core.table.ascii_table(headers, rows))


def _get_active_track() -> str | None:
    name = os.getenv("ORESHIC_TRACK")
    if name:
        name = name.strip()
        return name or None
    return None


def _run_entry_by_ids(
    file_id: str, entry_id: str,
        message_override: str | None, quiet: bool):

    files = _list_command_files_sorted()
    name = ors.features.search.resolve_name_by_id(file_id, files, "command")
    entries = ors.features.search.load_entries_generic(
        ors.core.settings.get_command_dir(),
        name
    )

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
    md_file = ors.md.writer.prepare_md_file(cmd_list[0])
    prompt = ors.core.prompt.build_prompt()
    cmd0 = Path(cmd_list[0]).name.lower()
    use_pty = cmd0 in ors.core.settings.get_auto_interactive()

    with open(md_file, "a", encoding="utf-8") as fp:
        ors.md.writer.md_header(
            fp,
            message_override or e["title"] or "(re-run)",
            prompt, cmd_list
        )
        try:
            if use_pty:
                ors.exec.pty_runner.run_via_pty(cmd_list, fp, quiet)
            else:
                ors.exec.stream_runner.run_stream_tee(cmd_list, fp, quiet)
        finally:
            ors.md.writer.md_close_output(fp)


# エントリ削除。削除後の Count が 0 ならファイルも削除（command）
def _delete_entry_by_ids(file_id: str, entry_id: str):
    files = _list_command_files_sorted()
    name = ors.features.search.resolve_name_by_id(file_id, files, "command")
    md_path = ors.core.settings.get_command_dir() / f"{name}.md"
    if not md_path.exists():
        print(f"[ors] not found: {md_path}", file=sys.stderr)
        sys.exit(2)

    ranges = ors.md.loader.index_entry_ranges(md_path)
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

    remaining = ors.md.loader.count_md_sections(md_path)
    if remaining == 0:
        try:
            md_path.unlink()
            print(f"[ors] deleted entry {idx} and removed file: {name}.md (Count=0)")
        except Exception as e:
            print(
                f"[ors] deleted entry {idx}, but failed to remove file: {e}",
                file=sys.stderr
            )
    else:
        print(f"[ors] deleted: {name} entry {idx} (remaining Count={remaining})")


def _show_entry_detail_by_ids(file_id: str, entry_id: str):
    files = _list_command_files_sorted()
    name = ors.features.search.resolve_name_by_id(file_id, files, "command")
    entries = ors.features.search.load_entries_generic(
        ors.core.settings.get_command_dir(),
        name
    )
    try:
        eid = int(entry_id)
        e = entries[eid - 1]
    except Exception:
        print("[ors] invalid entry id", file=sys.stderr)
        sys.exit(2)

    print(f"# {e['title']}\n")
    print("```bash")
    if e['cmd']:
        print(e['cmd'])
    print()
    print(e['out'] or "(no output)")
    print("```\n")


def hoge(args):
    if len(args.search) == 1:
        _list_command_files_ascii()
        return
    if len(args.search) == 2:
        _search_command_file_ascii_by_id(args.search[1])
        return
    if len(args.search) == 3:
        file_id, entry_id = args.search[1], args.search[2]
        if args.run and args.delete:
            print("[ors] cannot use --run and --del together", file=sys.stderr)
            sys.exit(2)
        if args.run:
            _run_entry_by_ids(file_id, entry_id, args.message, args.quiet)
            return
        if args.delete:
            _delete_entry_by_ids(file_id, entry_id)
            return
        _show_entry_detail_by_ids(file_id, entry_id)
        return
    print(
        "[ors] usage: -s command [file_id [entry_id]] [--run|--del]",
        file=sys.stderr
    )
