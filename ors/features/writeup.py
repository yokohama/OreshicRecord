import sys
from pathlib import Path

import ors.core


# 指定階層で子ノードを表形式表示（Name / Count=配下ファイル数）
def _list_writeup_level(indices: list[int]):
    root = _build_writeup_tree()
    node, children = _wu_get_by_indices(root, indices)
    headers = ["ID", "Name", "Count"]
    rows = []
    for i, (name, ch) in enumerate(children, 1):
        rows.append([str(i), name, str(_wu_leaf_count(ch))])
    print(ors.core.table.ascii_table(headers, rows))


class _WUNode:
    __slots__ = ("children", "file_path")

    def __init__(self):
        self.children: dict[str, _WUNode] = {}
        self.file_path: Path | None = None


# writeups ディレクトリ配下の *.md を '_' 区切りで木構造にする
def _build_writeup_tree() -> _WUNode:
    root = _WUNode()
    outdir = ors.core.settings.get_writeups_dir().expanduser()
    if not outdir.exists():
        return root
    for p in sorted(outdir.glob("*.md")):
        stem = p.stem  # 拡張子なし
        parts = stem.split("_") if "_" in stem else [stem]
        node = root
        for token in parts:
            node = node.children.setdefault(token, _WUNode())
        node.file_path = p  # このパスでファイルが存在
    return root


# indices で辿ったノードがファイル（葉）なら md を表示。階層が残っていれば一覧表示。
def _show_writeup_by_indices(indices: list[int]):
    root = _build_writeup_tree()
    node = root
    for idx in indices:
        children = _wu_sorted_children(node)
        if not (1 <= idx <= len(children)):
            print("[ors] ID out of range", file=sys.stderr)
            sys.exit(2)
        _, node = children[idx - 1]

    # 子が存在するなら一覧表示、子が無く file_path があれば中身表示
    if node.children:
        _list_writeup_level(indices)
        return

    if node.file_path:
        try:
            content = node.file_path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        except FileNotFoundError:
            print(f"[ors] not found: {node.file_path}", file=sys.stderr)
            sys.exit(2)

        sys.stdout.write(content)
        return

    # 子もファイルもない（空ノード）
    print("[ors] empty node", file=sys.stderr)
    sys.exit(2)


# 配下に存在するファイル（葉）の総数
def _wu_leaf_count(node: _WUNode) -> int:
    cnt = 1 if node.file_path is not None else 0
    for ch in node.children.values():
        cnt += _wu_leaf_count(ch)
    return cnt


# indices で辿った先のノードと、そのノード直下の (name,node) 一覧を返す
def _wu_get_by_indices(
        root: _WUNode,
        indices: list[int]) -> tuple[_WUNode, list[tuple[str, _WUNode]]]:

    node = root
    for idx in indices:
        children = _wu_sorted_children(node)
        if not (1 <= idx <= len(children)):
            print("[ors] ID out of range", file=sys.stderr)
            sys.exit(2)

        _, node = children[idx - 1]

    return node, _wu_sorted_children(node)


# 子を名前でソートして [(name, node)] を返す
def _wu_sorted_children(node: _WUNode) -> list[tuple[str, _WUNode]]:
    return sorted(node.children.items(), key=lambda kv: kv[0])


# writeup: 任意階層ナビ。--run/--del は非対応。
def run(args):
    if args.run or args.delete:
        print(
            "[ors] writeup does not support --run/--del",
            file=sys.stderr
        )
        sys.exit(2)

    ids = []
    for tok in args.search[1:]:
        if not tok.isdigit():
            print(
                "[ors] numeric ID required at each level (e.g. `ors -s writeup 2 1`)",
                file=sys.stderr
            )
            sys.exit(2)
        ids.append(int(tok))

    if len(ids) == 0:
        _list_writeup_level([])
        return

    # ノードが葉かどうかで出し分け
    root = _build_writeup_tree()
    node, children = _wu_get_by_indices(root, ids)
    if node.children:
        # まだ下に階層がある -> 一覧
        _list_writeup_level(ids)
        return

    # 葉なら中身表示（ファイル必須）
    if node.file_path:
        _show_writeup_by_indices(ids)
        return

    print("[ors] empty node", file=sys.stderr)
