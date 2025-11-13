import sys

import ors.core
import ors.features

def run(args):
    if len(args.search) < 2:
        print(
            "[ors] usage: -s query <search_word> [id] [--run|--del]",
            file=sys.stderr
        )
        sys.exit(2)

    search_word = args.search[1]

    # コマンド記録とトラック記録のディレクトリを取得
    command_dir = ors.core.settings.get_command_dir()
    track_dir = ors.core.settings.get_track_dir()

    # 両方のディレクトリ内のすべてのファイルを走査
    # ファイル内のすべてのエントリに対し、検索ワードが含まれているかチェック
    # マッチしたエントリの情報を集計
    matched_entries = []
    for dir_path in [command_dir, track_dir]:
        for md_path in dir_path.glob("*.md"):
            entries = ors.features.search.load_entries_generic(
                dir_path, md_path.stem
            )
            for entry in entries:
                if (search_word in entry["cmd"] or
                        search_word in entry["out"] or
                        search_word in entry["title"] or
                        search_word in md_path.stem):
                    entry["file_path"] = md_path
                    matched_entries.append(entry)

    # 引数の数に応じて処理を分岐
    if len(args.search) == 2:
        # 検索結果をテーブル形式で出力
        headers = ["ID", "Title", "Command"]
        rows = []
        for idx, entry in enumerate(matched_entries, 1):
            title = entry["title"]
            command = entry["cmd"]
            rows.append([str(idx), title, command])

        print(ors.core.table.ascii_table(headers, rows))
        return

    if len(args.search) == 3:
        # 特定のIDの詳細を表示または実行/削除
        try:
            entry_idx = int(args.search[2])
            if not (1 <= entry_idx <= len(matched_entries)):
                print("[ors] ID out of range", file=sys.stderr)
                sys.exit(2)
            selected_entry = matched_entries[entry_idx - 1]
        except ValueError:
            print("[ors] invalid entry ID", file=sys.stderr)
            sys.exit(2)

        # file_idとentry_idを特定する
        file_path = selected_entry["file_path"]
        mode = "command" if file_path.parent == command_dir else "track"

        # ファイルリストからfile_idを取得
        files = ors.features.common.list_files_sorted(file_path.parent)
        file_id = None
        for idx, f in enumerate(files, 1):
            if f == file_path:
                file_id = str(idx)
                break

        if file_id is None:
            print("[ors] file not found", file=sys.stderr)
            sys.exit(2)

        # そのファイル内でのentry_idを取得
        entries_in_file = ors.features.search.load_entries_generic(
            file_path.parent, file_path.stem
        )
        entry_id = None
        for idx, entry in enumerate(entries_in_file, 1):
            if (entry["title"] == selected_entry["title"] and
                    entry["cmd"] == selected_entry["cmd"] and
                    entry["out"] == selected_entry["out"]):
                entry_id = str(idx)
                break
        
        if entry_id is None:
            print("[ors] entry not found", file=sys.stderr)
            sys.exit(2)

        if args.run and args.delete:
            print("[ors] cannot use --run and --del together", file=sys.stderr)
            sys.exit(2)

        if args.run:
            ors.features.common.run_entry_by_ids(
                mode,
                file_id,
                entry_id,
                args.message,
                args.quiet
            )
            return

        if args.delete:
            ors.features.common.delete_entry_by_ids(
                mode,
                file_id,
                entry_id
            )
            return

        # 詳細表示
        ors.features.common.show_entry_detail_by_ids(
            mode,
            file_id,
            entry_id
        )
        return

    print(
        "[ors] usage: -s query <search_word> [id] [--run|--del]",
        file=sys.stderr
    )
    sys.exit(2)
