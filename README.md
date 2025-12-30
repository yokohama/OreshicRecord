# OreshicRecord

## 概要

OreshicRecord は、AkashicRecordsの概念をもとに、全利用者共通のナレッジプラットフォームを目指します。
対象者はLinuxのCLI上で作業する前エンジニアで、Powershellは今後の拡張です。

主なポイントは以下です。

### ナレッジ蓄積

CLI上でストレスなく実行コマンドとメモを記録。

- command: 日々の調査・作業コマンドを「再実行可能なログ」として残す
- track: 作業トラック（現在取り組んでいるタスク）単位でログを紐づける
- writeup: 自由形式の writeup を全文検索・一覧表示できるようにする

*将来的には利用者全員のナレッジを1箇所に蓄積、誰もがアクセス可能な世界観を目指す。*

例
```sh
ors -m "pingを3回実行" ping -c 3 8.8.8.8

```

### ナレッジの活用

検索オプションにより必要なコマンドを抽出し、実行可能。

例
```sh
ors -s query ping 1 --run

```


## インストール

### 1. clone

```
git clone git@github.com:yokohama/OreshicRecord.git
```

### 2. venvの設定

開発用にはプロジェクト直下に `.venv` を作成し、このリポジトリを editable モードでインストールすると、`ors` コマンドがパスに入ります。

```sh
cd OreshicRecord

# venv 作成
python -m venv .venv

# venv 有効化（シェルに応じて適宜変更）
source .venv/bin/activate

# このリポジトリをインストール（開発用）
pip install --upgrade pip
pip install -e .

# 動作確認
ors --help
```

### 3. 環境変数 ORESHIC_RECORD_DIR の設定

`ORESHIC_RECORD_DIR` は、`records/` ディレクトリを探しに行くベースディレクトリです。
OreshicRecord のプロジェクトルートを指定します。

```sh
cd OreshicRecord

# OreshicRecord ディレクトリ内で実行
echo "export ORESHIC_RECORD_DIR=$(pwd)" >> ~/.zshrc

# 設定を反映
source ~/.zshrc
```

