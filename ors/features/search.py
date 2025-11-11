import sys
from pathlib import Path


def _extract_cmd_from_prompt_line(cmdline: str) -> str:
    line = (cmdline or "").strip()
    if "$ " in line:
        return line.split("$ ", 1)[1].strip()
    if " > " in line:
        return line.split(" > ", 1)[1].strip()
    if "> " in line and line.count("> ") == 1:
        return line.split("> ", 1)[1].strip()
    return line


def load_entries_generic(base_dir: Path, name: str):
    p = base_dir / f"{name}.md"

    if not p.exists():
        print(f"[ors] not found: {p}", file=sys.stderr)
        sys.exit(2)

    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    entries, i, n = [], 0, len(lines)

    while i < n:
        if lines[i].startswith("##"):
            title = lines[i][2:].strip()
            i += 1
            while i < n and lines[i].strip() == "":
                i += 1
            cmdline = ""
            if i < n and lines[i].strip().startswith("```"):
                i += 1
                block = []
                while i < n and not lines[i].strip().startswith("```"):
                    block.append(lines[i])
                    i += 1
                if i < n:
                    i += 1
                cmdline = "\n".join(block).strip()
            cmd = _extract_cmd_from_prompt_line(cmdline)
            out_text = ""
            while i < n and lines[i].strip() == "":
                i += 1
            if i < n and lines[i].strip().startswith("```"):
                i += 1
                out_lines = []
                while i < n and not lines[i].strip().startswith("```"):
                    out_lines.append(lines[i])
                    i += 1
                if i < n:
                    i += 1
                out_text = "\n".join(out_lines)
            entries.append({"title": title, "cmd": cmd, "out": out_text})
        i += 1
    return entries


def resolve_name_by_id(id_str: str, files: list[Path], kind: str) -> str:
    if not id_str.isdigit():
        print(
            f"[ors] numeric ID required. Example: `ors -s {kind} 1`",
            file=sys.stderr
        )
        sys.exit(2)

    idx = int(id_str)

    if 1 <= idx <= len(files):
        return files[idx - 1].stem

    print(f"[ors] ID out of range (1..{len(files)})", file=sys.stderr)
    sys.exit(2)
