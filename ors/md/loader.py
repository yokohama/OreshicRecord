from pathlib import Path
import re


_FENCE_RE = re.compile(r'^\s*```')


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
