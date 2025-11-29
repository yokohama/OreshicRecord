# OreshicRecord

OreshicRecord は、コマンド実行記録や作業メモを Markdown で蓄積し、検索・再実行できるツールです。

## インストール

### 1. 環境変数 ORESHIC_RECORD_DIR の設定

`ORESHIC_RECORD_DIR` は、`records/` ディレクトリを探しに行くベースディレクトリです。通常は OreshicRecord のプロジェクトルートを指定します。

```sh
# OreshicRecord ディレクトリ内で実行
echo "export ORESHIC_RECORD_DIR=$(pwd)" >> ~/.zshrc
```

設定後、新しいシェルを開くか、次のようにして反映してください。

```sh
source ~/.zshrc
```

