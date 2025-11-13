import sys
from pathlib import Path

import ors.core
from ors.core.image_display import display_content_with_images


# ==========================================================
# ノード構造定義
# ==========================================================
class _WUNode:
    __slots__ = ("children", "file_path", "rel_path")

    def __init__(self, rel_path: Path | None = None):
        self.children: dict[str, "_WUNode"] = {}
        self.file_path: Path | None = None
        self.rel_path: Path | None = rel_path


# ==========================================================
# writeups ディレクトリ配下の実ディレクトリ階層を木構造にする
# ==========================================================
def _build_writeup_tree() -> _WUNode:
    root = _WUNode(rel_path=Path(""))
    basedir = ors.core.settings.get_writeups_dir().expanduser()
    if not basedir.exists():
        return root

    # すべてのディレクトリをノード化（空フォルダも表示対象）
    for d in basedir.rglob("*"):
        if d.is_dir():
            rel = d.relative_to(basedir)
            if not rel.parts:
                continue
            node = root
            acc = Path("")
            for token in rel.parts:
                acc = acc / token
                node = node.children.setdefault(token, _WUNode(rel_path=acc))

    # Markdown「ファイル」だけをノード化（*.md ディレクトリは除外）
    for p in sorted(basedir.rglob("*.md")):
        if not p.is_file():
            continue
        rel = p.relative_to(basedir)
        node = root
        acc = Path("")
        for i, token in enumerate(rel.parts):
            acc = acc / token
            node = node.children.setdefault(token, _WUNode(rel_path=acc))
            if i == len(rel.parts) - 1:
                node.file_path = p
    return root


# ==========================================================
# パンくず生成（indices → ["htb", "room1"] → "htb > room1"）
# ==========================================================
def _breadcrumb(indices: list[int]) -> str:
    if not indices:
        return ""
    names: list[str] = []
    root = _build_writeup_tree()
    node = root
    for idx in indices:
        children = _wu_sorted_children(node)
        if not (1 <= idx <= len(children)):
            return ""
        name, node = children[idx - 1]
        names.append(name)
    return " > ".join(names)


# ==========================================================
# 指定階層で子ノードを表形式表示（Name / Count）
# ==========================================================
def _list_writeup_level(indices: list[int]):
    root = _build_writeup_tree()
    node, children = _wu_get_by_indices(root, indices)
    headers = ["ID", "Name", "Count"]
    rows = []

    for i, (name, ch) in enumerate(children, 1):
        is_file_leaf = _is_md_file_leaf(ch)
        count = "" if is_file_leaf else str(_wu_leaf_count(ch))
        rows.append([str(i), name, count])

    crumb = _breadcrumb(indices)
    if crumb:
        print()
        print(crumb)
        print()

    print(ors.core.table.ascii_table(headers, rows))


# ==========================================================
# md ファイル葉の判定（構造＋拡張子で厳密化）
# ==========================================================
def _is_md_file_leaf(node: _WUNode) -> bool:
    if (node.file_path is not None and node.file_path.is_file() and not node.children):
        return True
    if (node.rel_path is not None and node.rel_path.suffix.lower() == ".md" and not node.children):
        return True
    return False


# ==========================================================
# 指定ノード（indices指定）の内容を表示
# ==========================================================
def _show_writeup_by_indices(indices: list[int]):
    basedir = ors.core.settings.get_writeups_dir().expanduser()
    root = _build_writeup_tree()
    node = root
    for idx in indices:
        children = _wu_sorted_children(node)
        if not (1 <= idx <= len(children)):
            print("[ors] ID out of range", file=sys.stderr)
            sys.exit(2)
        _, node = children[idx - 1]

    if _is_md_file_leaf(node):
        fp: Path | None = node.file_path
        if fp is None and node.rel_path is not None:
            fp = basedir / node.rel_path
        if fp is None:
            print("[ors] empty node", file=sys.stderr)
            sys.exit(2)
        try:
            content = fp.read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError:
            print(f"[ors] not found: {fp}", file=sys.stderr)
            sys.exit(2)
        display_content_with_images(content, fp)
        return

    _list_writeup_level(indices)


# ==========================================================
# 配下に存在する Markdown ファイル（葉）の総数をカウント
# ==========================================================
def _wu_leaf_count(node: _WUNode) -> int:
    cnt = 1 if _is_md_file_leaf(node) else 0
    for ch in node.children.values():
        cnt += _wu_leaf_count(ch)
    return cnt


# ==========================================================
# indices で辿った先のノードと、そのノード直下の (name,node) 一覧を返す
# ==========================================================
def _wu_get_by_indices(
    root: _WUNode, indices: list[int]
) -> tuple[_WUNode, list[tuple[str, _WUNode]]]:
    node = root
    for idx in indices:
        children = _wu_sorted_children(node)
        if not (1 <= idx <= len(children)):
            print("[ors] ID out of range", file=sys.stderr)
            sys.exit(2)
        _, node = children[idx - 1]
    return node, _wu_sorted_children(node)


# ==========================================================
# 子を (ディレクトリ優先, 名前順) でソートして返す
# ==========================================================
def _wu_sorted_children(node: _WUNode) -> list[tuple[str, _WUNode]]:
    items = list(node.children.items())

    def _sort_key(kv: tuple[str, _WUNode]):
        name, nd = kv
        is_dir = bool(nd.children)
        is_file_only = _is_md_file_leaf(nd)
        kind_rank = 0 if is_dir else 1 if is_file_only else 0
        return (kind_rank, name)

    return sorted(items, key=_sort_key)


# ==========================================================
# メインエントリーポイント
# ==========================================================
def run(args):
    if args.run or args.delete:
        print("[ors] writeup does not support --run/--del", file=sys.stderr)
        sys.exit(2)

    ids = []
    for tok in args.search[1:]:
        if not tok.isdigit():
            print(
                "[ors] numeric ID required at each level (e.g. `ors -s writeup 2 1`)",
                file=sys.stderr,
            )
            sys.exit(2)
        ids.append(int(tok))

    if len(ids) == 0:
        _list_writeup_level([])
        return

    root = _build_writeup_tree()
    node, _ = _wu_get_by_indices(root, ids)

    if _is_md_file_leaf(node):
        _show_writeup_by_indices(ids)
        return

    _list_writeup_level(ids)
