# AGENTS – OreshicRecord 開発者向け引き継ぎメモ

このドキュメントは、OreshicRecord の開発・保守を行うエンジニア向けの引き継ぎメモです。旧 `AGENT.md` に書かれていた概要を土台に、実際のコード構成を踏まえて再整理したものです。

---

## 1. プロジェクト概要

OreshicRecord は、シェルで実行したコマンドとその出力、および簡単なメモを Markdown で蓄積し、あとから検索・再実行できるようにするツールです。主な目的は以下のとおりです。

- 日々の調査・作業コマンドを「再実行可能なログ」として残す
- 作業トラック（現在取り組んでいるタスク）単位でログを紐づける
- コマンド・トラック・自由形式の writeup を全文検索・一覧表示できるようにする
- 将来的にはチーム全体でナレッジを共有できる wiki リポジトリへ移行する（`tasks/1_wiki.md` 参照）

CLI エントリポイントは `ors` で、`pyproject.toml` の `[project.scripts]` で定義されています。

```toml
[project.scripts]
ors = "ors.__main__:main"
```

---

## 2. 技術スタック・ランタイム

- 言語: Python 3.8+
- パッケージ管理: `pyproject.toml` + setuptools
- 設定ファイル: `config.toml`（TOML 形式）
- 端末制御: `pty`, `termios`, `fcntl`, `select` など POSIX 系 API
- 表示まわり: CJK 幅対応のテーブルレンダリング（`unicodedata.east_asian_width` / 任意で `wcwidth`）

**実行環境の前提**

- 実質的に Linux / macOS 等の POSIX 環境を前提にしています。
  - `ors.exec.pty`, `ors.core.table.set_winsize` などで `termios` 系 API を使用
- Windows 対応は現状ほぼ考慮されていません（`os.name != "nt"` 条件付きの箇所はありますが、PTY 周りは非対応）。

---

## 3. ディレクトリ構成とデータ配置

### 3.1 リポジトリ構成（コード）

```text
OreshicRecord/
  ├─ ors/                # アプリ本体
  │   ├─ __main__.py     # エントリーポイント
  │   ├─ cli/            # CLI パーサ
  │   │   └─ parser.py
  │   ├─ core/           # 共通基盤
  │   │   ├─ settings.py
  │   │   ├─ md.py
  │   │   ├─ prompt.py
  │   │   ├─ clean.py
  │   │   ├─ table.py
  │   │   └─ image_display.py
  │   ├─ exec/           # コマンド実行ラッパ
  │   │   ├─ stream.py
  │   │   └─ pty.py
  │   └─ features/       # 機能別エントリ
  │       ├─ recording.py
  │       ├─ command.py
  │       ├─ track.py
  │       ├─ writeup.py
  │       ├─ query.py
  │       └─ common.py / search.py
  ├─ config.toml         # auto_interactive 設定など（任意）
  ├─ README.md
  ├─ AGENTS.md           # 本ドキュメント
  ├─ AGENT.md            # 旧メモ（参考）
  └─ tasks/
      └─ 1_wiki.md       # 将来の wiki 化構想ドキュメント
```

### 3.2 ランタイムディレクトリ構成（記録データ）

`records/` 以下はユーザー環境側に作成される領域で、Git 管理外を想定しています。ベースディレクトリは環境変数 `ORESHIC_RECORD_DIR` で指定します。

- `ORESHIC_RECORD_DIR`:
  - `ors.core.settings.get_base_dir()` が参照
  - 通常はこのリポジトリのルートパスを設定

```bash
# プロジェクトルートで設定例
echo "export ORESHIC_RECORD_DIR=$(pwd)" >> ~/.zshrc
source ~/.zshrc
```

- ディレクトリ構造（現行仕様 AsIs）

```text
$ORESHIC_RECORD_DIR/
  └─ records/
      ├─ commands/   # 非トラック実行の記録
      ├─ tracks/     # トラック名ごとの記録
      └─ writeups/   # 自由形式のメモツリー
```

- 補助ファイル
  - 現在アクティブなトラック名: `/tmp/oreshic_records_track_name`
    - `ors.core.settings.get_track_name_file()` が返す固定パス

### 3.3 将来構成（wiki 化構想; `tasks/1_wiki.md`）

`tasks/1_wiki.md` では、将来的に `records/` を専用 wiki リポジトリ（`OreshicRecord.wiki`）に置き換え、ユーザーごとディレクトリへ分離する構想が示されています。

```text
OreshicRecord/
  ├─ ors/
  ├─ .gitignore           # records を除外
  └─ records/ (git clone OreshicRecord.wiki)
      └─ <user_name>/
          ├─ commands/
          ├─ tracks/
          └─ writeups/
```

- 現状のコードは `settings.get_records_dir()` を通じて `records` パスを参照しているため、
  - `ORESHIC_RECORD_DIR/records` を wiki リポジトリにしても、**自ユーザー配下だけを使う形**であれば大きな変更なく動かせます。
- CLI の `--user/-u` オプションなど、多人数検索の仕様はまだ実装されていません（`1_wiki.md` は将来仕様メモ）。

---

## 4. 全体アーキテクチャとフロー

### 4.1 実行フロー概要

1. エントリポイント: `ors.__main__.py:main()`
   - `sys.argv` を見て、引数なしならヘルプを表示して終了
   - それ以外は `ors.cli.parser.parse_args()` へ委譲
2. 引数解釈（`ors/cli/parser.py`）
   - `-s/--search` による検索モード（`command|track|writeup|query`）
   - `--run` / `--del` によるエントリ再実行・削除
   - `-m/--message` で任意メモ
   - `-q/--quiet` でファイルへの保存抑止
   - `-t/--track` で一時的トラック名のセット
   - `-u/--unset` でトラック名の解除
   - `command`（残り全引数）で実際に実行するコマンド
3. トラック名のセット/解除
   - `-t` 指定時: `/tmp/oreshic_records_track_name` にトラック名を書き込む
   - `-u` 指定時: 上記ファイルを削除
4. 検索モード (`-s`) のディスパッチ（`ors.__main__`）
   - `command`, `track`, `writeup`, `query` のいずれかに応じて
     `ors.features.<mode>.run(args)` を呼び出し
5. 実行モード（`-s` 未指定）
   - `command` 引数が必須
   - `ors.features.recording.run(args)` が呼ばれ、記録付きでコマンドを実行

### 4.2 レイヤ構成

- CLI レイヤ: `ors.cli`
- コアレイヤ: `ors.core`（パス解決・MD フォーマット・端末制御など）
- 実行レイヤ: `ors.exec`（PTY / 非 PTY 実行）
- 機能レイヤ: `ors.features`（recording / command / track / writeup / query など）

依存方向はおおむね以下のようになっています。

```text
ors.__main__
  └─ ors.cli.parser
  └─ ors.features.*
       ├─ ors.core.*
       └─ ors.exec.*
ors.exec.*
  └─ ors.core.clean, table
```

---

## 5. 主要モジュール別メモ

### 5.1 `ors.cli.parser`

- `build_parser()` で `argparse.ArgumentParser` を構築
- `parse_args(argv)` でパース + エラー時に独自メッセージを出して終了コード 2
- 引数の意味はヘルプメッセージにかなり詳細に記載されています。

### 5.2 `ors.core.settings`

- `get_base_dir()`
  - `ORESHIC_RECORD_DIR` を必須前提で環境変数から取得し、`Path` で返却
- `get_records_dir()`, `get_command_dir()`, `get_track_dir()`, `get_writeups_dir()`
  - それぞれ `base/records/...` パスを返却
- `get_track_name_file()`
  - 現在は固定で `/tmp/oreshic_records_track_name`
- `get_auto_interactive()`
  - `config.toml` の `auto_interactive = [ ... ]` を読み込み
  - ここに含まれるコマンド名は PTY 経由（インタラクティブ扱い）で記録されます

### 5.3 `ors.core.md` – Markdown フォーマットの要

**このファイルの仕様が、`command`/`track`/`query` 検索の前提になっています。変更する場合は慎重に。**

- `_get_active_track()`
  - `/tmp/oreshic_records_track_name` があれば読み取り、トラック名を返却
- `prepare_file(cmd)`
  - アクティブトラックがあれば `tracks/<track_name>.md` に記録
  - なければ `commands/<base_cmd_name>.md` に記録
- `write_header(fp, message, prompt, cmd_list)`
  - 1 エントリの先頭を以下のような形式で書き込みます:

    ```md
    ## <message or "(no message)">

    ```bash
    user@cwd host$ actual command args...
    ```

    ```
    # ここからコマンド出力が入り、close_output で ``` が閉じられる
    ```

- `close_output(fp)`
  - `ors.core.clean.term_flush()` の残りバッファを書き出し、出力用の ``` を閉じる
- `count_md_sections(md_path)` / `index_entry_ranges(md_path)`
  - フェンス（```）の内外を意識しつつ、`## ` から始まる行を「エントリ見出し」としてカウント/範囲算出
  - `features.common.delete_entry_by_ids()` がこの範囲情報を使ってエントリを削除

> **重要**: MD フォーマットを変える場合は、`features.search.load_entries_generic()` と `features.common.*` 群との整合性が崩れないようにテストが必要です。

### 5.4 `ors.core.clean`

- ANSI エスケープ（CSI / OSC）を除去しつつ、カーソル移動やバックスペース、`\r` 上書きなどを考慮して「見た目上の最終行」を文字列として構築するステートフルなクリーンアップロジックです。
- `term_chunk(s: str) -> str`
  - ストリーム中の部分文字列を受け取り、**確定した行のみ**を返します。
  - 末尾の途中行は `_CLEAN_STATE` に保持され、次のチャンクに跨るときに再計算されます。
- `term_flush() -> str`
  - 途中行を最終行として確定させて返します（改行付き）。
- `ors.exec.stream`, `ors.exec.pty` の両方から呼ばれており、出力の整形品質に直結します。

### 5.5 `ors.core.table`

- CJK 幅考慮の ASCII テーブル生成ユーティリティ。
- 主な公開関数:
  - `ascii_table(headers, rows, max_total_width=None) -> str`
  - `set_winsize(fd)` – PTY のウィンドウサイズを stdout に合わせる
- `features.command`, `features.track`, `features.query`, `features.writeup` などで一覧表示に利用。

### 5.6 `ors.core.prompt`

- `build()`
  - `USER`, `cwd`, `~` 置換、`os.uname().nodename` を組み合わせて `user@path host$ ` の形式を返却
  - `md.write_header()` の prompt 部分に埋め込まれます。

### 5.7 `ors.core.image_display`

- writeup 表示時の画像パス変換ユーティリティ。
- `convert_image_paths(content, md_file_path)`
  - Markdown の `![alt](./md_images/xxx.png)` 形式を、
    - MD ファイルの位置を基準とする絶対パスに変換した上で、
    - 実行カレントディレクトリからの相対パスに書き換えます。
- `display_content_with_images(content, md_file_path)`
  - 上記変換後に `stdout` に出力。

### 5.8 `ors.exec.stream` / `ors.exec.pty`

- `ors.exec.stream.run(cmd_list, fp, silent)`
  - 通常の非インタラクティブコマンドの実行。
  - `stdbuf` があれば `stdbuf -oL -eL` で行バッファリングを強制してから実行。
  - stdout/stderr をそれぞれリアルタイム転送しつつ、`silent` でなければ `clean.term_chunk` を通して MD に追記します。
- `ors.exec.pty.run(cmd_list, fp, silent)`
  - `pty.openpty()` を使ったインタラクティブセッション実行。
  - 端末サイズは `ors.core.table.set_winsize()` で同期。
  - パスワードプロンプトらしき出力（`password|passphrase` を含む末尾）を検知している間は、ユーザー入力を MD に記録しないよう制御。
  - Ctrl-C / Ctrl-Z / Ctrl-\ をシグナルとして子プロセスのプロセスグループへ送出。

### 5.9 `ors.features.recording`

- 実コマンドの記録実行を行うメイン機能。
- フロー:
  1. `md.prepare_file(args.command[0])` で出力先 MD を決定
  2. `prompt.build()` でプロンプト文字列生成
  3. 先頭コマンド名で `settings.get_auto_interactive()` を見て `use_pty` を決定
  4. ヘッダを書き込んだ後、`exec.pty` または `exec.stream` を呼び出し
  5. finally 節で `md.close_output(fp)` を呼んでフェンスを閉じる

### 5.10 `ors.features.common` / `ors.features.search`

- `features.search.load_entries_generic(base_dir, name)`
  - `md.py` のフォーマットに依存して、1 MD ファイルの中からエントリをパースし、
    `{ "title": str, "cmd": str, "out": str }` のリストを返します。
- `features.search.resolve_name_by_id(id_str, files, kind)`
  - 一覧表示時の ID 番号から MD ファイル名（拡張子抜き）を求めます。
- `features.common.*` は command / track 双方から共通利用される操作群です。
  - `list_files_sorted(path)` – `*.md` のソート済みリスト
  - `list_files_ascii(mode)` – ID/Name/Count のテーブル表示
  - `search_file_ascii_by_id(mode, file_id)` – あるファイル内のエントリ一覧
  - `show_entry_detail_by_ids(mode, file_id, entry_id)` – 単一エントリの詳細表示
  - `delete_entry_by_ids(mode, file_id, entry_id)` – エントリ削除（Count=0 ならファイル削除）
  - `run_entry_by_ids(mode, file_id, entry_id, message_override, quiet)` – エントリのコマンド部分を再実行

### 5.11 `ors.features.command` / `track`

- 共通のパターンで `args.search` の長さに応じて挙動を切り替えます。
  - `-s command` / `-s track`
    - ファイル一覧
  - `-s command <file_id>`
    - ファイル内エントリ一覧
  - `-s command <file_id> <entry_id> [--run|--del]`
    - エントリ詳細表示 / 再実行 / 削除
- `--run` と `--del` の同時指定はエラー。

### 5.12 `ors.features.writeup`

- `writeups/` 以下のディレクトリ・ファイル構造をツリーとして扱う機能です。
- 特徴:
  - ディレクトリはそのままノード化（空フォルダも表示対象）
  - `*.md` ファイルは葉ノードとして扱い、`ID` により階層的に選択
  - `./md_images/` フォルダはディレクトリツリー上は隠し扱い
- 主な挙動:
  - `ors -s writeup`
    - ルート直下の子ノード一覧
  - `ors -s writeup 2 1`
    - `2` 番目のノードの子階層をたどり、`1` 番目を表示または一覧
  - ノードが「単一 MD ファイル葉」の場合は `image_display.display_content_with_images()` で内容を表示
  - ディレクトリノードの場合は Name/Count の一覧表を表示
- `--run` / `--del` はサポートしない（エラー終了）。

### 5.13 `ors.features.query`

- コマンド記録 (`commands/`) とトラック記録 (`tracks/`) を横断して全文検索する機能です。
- フロー:
  1. `-s query <word>` で検索ワードを取得
  2. `command_dir` / `track_dir` 配下の `*.md` を走査
  3. `load_entries_generic()` で各エントリを読み込み、
     - `entry["cmd"]`, `entry["out"]`, `entry["title"]`, MD ファイル名のいずれかに
       検索ワードが含まれていればヒットとみなす
  4. ヒットしたエントリに `file_path` を付加して `matched_entries` を構築
- 使い方:
  - `-s query <word>`
    - 検索結果を ID/Title/Command のテーブルで表示
  - `-s query <word> <id> [--run|--del]`
    - 一旦 `matched_entries[id-1]` を見つけ、そこから元の MD ファイル内での
      `file_id` / `entry_id` を逆引きして `common.*` に委譲

---

## 6. 典型的な利用シナリオ

### 6.1 通常のコマンド記録

```bash
# 単純な記録
ors -m "ping test" ping -c 3 8.8.8.8

# 出力をファイルに残さずに実行のみ
ors -q -m "no recording" ls -la
```

- `-m` が未指定の場合は `(no message)` というタイトルになります。

### 6.2 トラックを使った作業ログ

```bash
# トラックを一時的にセットしてコマンド実行
ors -t "htb/awesome-room" -m "nmap" nmap -sV 10.10.10.10

# トラック解除
ors -u
```

- トラックがアクティブな間は、すべての記録が `records/tracks/<track_name>.md` に集約されます。

### 6.3 コマンド・トラックの検索と再実行

```bash
# コマンド記録の一覧
ors -s command

# 1 番目のコマンドファイルのエントリ一覧
ors -s command 1

# 1 番目のファイルの 3 番目のエントリを再実行
ors -s command 1 3 --run

# 1 番目のファイルの 3 番目のエントリを削除
ors -s command 1 3 --del
```

トラックについても `command` を `track` に置き換えた同様の操作が可能です。

### 6.4 writeup の閲覧

```bash
# writeups/ 直下の構造を一覧
ors -s writeup

# 特定の階層を辿っていく
ors -s writeup 2
ors -s writeup 2 1
ors -s writeup 2 1 3
```

### 6.5 全文検索（query）

```bash
# "ping" を含むコマンド・出力・タイトル・ファイル名を横断検索
ors -s query ping

# 3 番目のヒットを再実行
ors -s query ping 3 --run

# 3 番目のヒットを削除
ors -s query ping 3 --del
```

---

## 7. 開発時の注意点・ベストプラクティス

### 7.1 コーディングスタイル

- 旧 `AGENT.md` の方針どおり、PEP8 警告は可能な限り解消する方向で進めてください。
- 型ヒントは既存コードのスタイルに合わせ、
  - Python 3.10+ では `list[str]` 形式が使われています（`|` による Union 等）。
- 例外・エラー時は必ずユーザー向けに分かりやすいメッセージを標準エラー出力へ出し、終了コード 2 などを明示的に返してください。

### 7.2 既存仕様との整合性

- `ors.core.md` のフォーマットを変更する場合は、
  - `features.search.load_entries_generic`
  - `features.common.delete_entry_by_ids`
  - `features.common.show_entry_detail_by_ids`
  - `features.query.run`
  など、**全てが同じ前提に立っている**ことを確認した上で変更してください。
- `ors.exec.pty` のパスワード入力検知（`_PASS_PROMPT_RE`）は、
  - ログにパスワードを残さないための最低限の防波堤なので、削除しないことを推奨します。

### 7.3 OS 依存コード

- `termios` / `pty` / `fcntl` を使っているため、Windows では動作しません。
- POSIX 以外の環境サポートを増やす場合は、
  - `ors.exec` の抽象化レイヤを追加して分岐させるなど、大きめのリファクタリングが必要になります。

### 7.4 config.toml の扱い

- `config.toml` がなくても動作します（`FileNotFoundError` は握りつぶして空設定に）。
- インタラクティブコマンドを追加したい場合は `auto_interactive` にコマンド名を追記してください。
  - 例: `"ssh"`, `"mysql"`, `"psql"`, `"htop"` などは既にデフォルトで含まれています。

---

## 8. 今後の拡張候補・検討メモ

### 8.1 wiki リポジトリへの移行 (`tasks/1_wiki.md`)

- `tasks/1_wiki.md` に詳細な仕様草案があります。
- 大まかなゴール:
  - 各ユーザーのナレッジを GitHub wiki リポジトリで一元管理
  - `records/<user>/commands`, `records/<user>/tracks`, `records/<user>/writeups` へ分離
  - CLI に `--user/-u` オプションを追加し、自分の記録・全ユーザーの記録・特定ユーザーの記録を切り替えて検索できるようにする
- 課題として挙げられている点:
  - writeup の画像パスがローカル絶対パスのままだと wiki 上で表示できない問題
  - これに対して、本リポジトリでは `md_images` ディレクトリルール + `image_display.convert_image_paths()` によるパス変換を導入済み

### 8.2 テスト戦略の整備

- 現状テストコードはなく、動作確認は手動で行う前提です。
- 可能であれば以下を優先的にテスト対象にすると安心です。
  - `ors.core.md.count_md_sections` / `index_entry_ranges`
  - `ors.features.search.load_entries_generic`
  - `ors.features.query.run` の ID 解決ロジック
  - `ors.exec.stream` / `ors.exec.pty` の最小限の動作確認

### 8.3 CLI ヘルプの整備

- 現在 `argparse.ArgumentParser` の `prog` は `"ors"` に統一されており、実行コマンド名 `ors` と一致しています。
  - 将来コマンド名を変更する場合は、ヘルプ表示の `prog` も合わせて更新してください。

---

## 9. このファイルの変更履歴（メタ情報）

- 2025-11-29: 初版作成
  - 旧 `AGENT.md` の概要・技術スタック・ディレクトリ構成・PEP8 方針を統合。
  - 実コードベースでのアーキテクチャ説明、MD フォーマット仕様、インタラクティブ実行処理、`tasks/1_wiki.md` の wiki 化構想を反映。

