# OreshicRecord

OreshicRecord は、コマンド実行記録や作業メモを Markdown で蓄積し、検索・再実行できるツールです。

## インストールとセットアップ

以下は、このリポジトリを初めて clone したユーザーが `ors` コマンドを使い始めるまでの最低限の手順です。

### 1. リポジトリの取得

```sh
git clone https://github.com/<owner>/OreshicRecord.git
cd OreshicRecord
```

### 2. GitHub Wiki（records リポジトリ）の clone

OreshicRecord では、記録ストレージとして GitHub Wiki を利用します。Wiki リポジトリを `records/` ディレクトリとして clone してください。

```sh
git clone https://github.com/<owner>/OreshicRecord.wiki.git records
```

これにより、`OreshicRecord/records/.git` を持つ独立した Git リポジトリとして Wiki が配置されます。

### 3. 環境変数 ORESHIC_RECORD_DIR の設定

`ORESHIC_RECORD_DIR` は、`records/` ディレクトリを探しに行くベースディレクトリです。通常は OreshicRecord のプロジェクトルートを指定します。

```sh
# OreshicRecord ディレクトリ内で実行
echo "export ORESHIC_RECORD_DIR=$(pwd)" >> ~/.zshrc
```

設定後、新しいシェルを開くか、次のようにして反映してください。

```sh
source ~/.zshrc
```

### 4. 環境変数 ORESHIC_RECORD_GITHUB_USER の設定

`records/<user>/...` の `<user>` 部分となる GitHub ユーザー名を環境変数で指定します。

```sh
echo "export ORESHIC_RECORD_GITHUB_USER=<your-github-username>" >> ~/.zshrc
```

GitHub ユーザー名は、自分の GitHub プロフィール URL（例: `https://github.com/alice` の `alice` 部分）を確認して指定してください。

`ORESHIC_RECORD_GITHUB_USER` が設定されていない場合、`ors` 実行時にエラーとなります。

### 5. （任意）config.toml でのユーザー名設定

環境変数ではなく `config.toml` で GitHub ユーザー名を指定することもできます。

優先順位は次のとおりです。

1. 環境変数 `ORESHIC_RECORD_GITHUB_USER`
2. `config.toml` の `github_user`
3. `config.toml` の `[user].github`

例:

```toml
# いずれか一方、または両方を定義

github_user = "<your-github-username>"

[user]
github = "<your-github-username>"
```

### 6. パッケージとしてインストール（任意）

`ors` コマンドをシステムにインストールしたい場合は、プロジェクトルートで次を実行します。

```sh
pip install .
```

`pyproject.toml` の `[project.scripts]` で `ors = "ors.__main__:main"` が定義されているため、インストール後は次のように CLI を実行できます。

```sh
ors -h
```

### 7. 動作確認

新しいシェルで環境変数が設定されていることを確認します。

```sh
echo $ORESHIC_RECORD_DIR
echo $ORESHIC_RECORD_GITHUB_USER
```

そのうえで、簡単なコマンドを記録してみてください。

```sh
ors ls
```

問題なく実行できれば、記録は次のようなパスに保存されます。

- `ORESHIC_RECORD_DIR/records/<your-github-username>/commands/`
- `ORESHIC_RECORD_DIR/records/<your-github-username>/tracks/`
- `ORESHIC_RECORD_DIR/records/<your-github-username>/writeups/`

この時点で、`records/` 以下はあなた自身の GitHub Wiki リポジトリとして扱える状態になっているので、通常どおり `git add/commit/push` で変更を push して構いません（メインリポジトリとは別の Git 管理になります）。

