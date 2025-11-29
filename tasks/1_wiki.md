# データストアのwiki化

## Why?

- 利用者全員が一箇所にナレッジの蓄積ができるようにすため
- 全ての利用者が他の利用者のナレッジも検索対象にできるようにするため
- 後に、データストアの差し替えを(例えばDBとかS3とか)に簡単にするため

## What?

- recordsにためているmdを、OreshicRecord.wkiリポジトリに移行する。
- wikiリポジトリには、各ユーザーのgithubユーザー名のホルダを作成して、各ユーザーのナレッジはその中に保存される。
- リポジトリ構成

```
AsIs:

OreshicRecord/
 |- ors/ #コード
 |- records/ #md置き場
     |- commands
     |- tracks
     |- writeups #この中にユーザーは画像を自由に保存可

```


```
ToBe:

OreshicRecord/
 |- ors/ #コード
 |- .gitignore #recordsを記載
 |- records(git clone OreshicRecord.wiki)/ #全ユーザー共通のmd置き場
     |- user名
         |- commands
         |- tracks
         |- writeups #この中にユーザーは画像を自由に保存可

```

## How

### CLI

#### 記録

`ors -t トラック名` や、`ors -m "コメント" ping -c 3 8.8.8.8` で作成されていたmdは、
全て、wiki/<user(self)/の中の、commandsやtracksホルダに記録されるようにする。

#### 検索

| コマンド | AsIs | ToBe |
| ---- | ---- | ---- |
| ors -s command | records/commands/md一覧 | wiki/<user(self)>/commands/md一覧 |
| ors -s command 1 | records/commands/1のmdの中身一覧 | wiki/<user(self)>/commands/1のmdの中身一覧 |
| ors -s command 1 5 | records/commands/1のmdの5を表示 | wiki/<user(self)>/commands/1のmdの5を表示 |
| ors -s command 1 5 --del | 1の5を削除 | wiki/<user(self)>/commands/1のmdの5を削除 |
| ors -s command 1 5 --run | 1の5を実行 | wiki/<user(self)>/commands/1のmdの5を実行 |
| ors -s command --user/-u | | エラー表示 |
| ors -s command --user/-u * | | wiki/<user(全て)>/commands/md一覧 |
| ors -s command --user/-u * 1 | | wiki/<user(全て)>/commands/1のmdの中身一覧 |
| ors -s command --user/-u * 1 5 | | wiki/<user(全て)>/commands/1のmdの5を表示 |
| ors -s command --user/-u * 1 5 --del | | エラー表示 |
| ors -s command --user/-u * 1 5 --run | | wiki/<user(全て)>/commands/1のmdの5を実行 |
| ors -s command --user/-u user名 | | wiki/user名/commands/md一覧 |
| ors -s command --user/-u user名 1 | | wiki/user名/commands/1のmdの中身一覧 |
| ors -s command --user/-u user名 1 5 | | wiki/user名/commands/1のmdの5を表示 |
| ors -s command --user/-u user名 1 5 --del | | エラー表示 |
| ors -s command --user/-u user名 1 5 --run | | wiki/user名/commands/1のmdの5を実行 |
| ors -s track | records/tracks/md一覧 | wiki/<user(self)>/tracks/md一覧 |
| ors -s track 1 | records/tracks/1のmdの中身一覧 | wiki/<user(self)/tracks/1のmdの中身一覧 |
| ors -s track 1 3 | records/tracks/1のmdの3を表示 | wiki/<user(self)/tracks/1のmdの3を表示 |
| ors -s track 1 3 --del | 1の3を削除 | wiki/<user(self)>/tracks/1のmdの3を削除 |
| ors -s track 1 3 --run | 1の3を実行 | wiki/<user(self)>/tracks/1のmdの3を実行 |
| ors -s track --user/-u | | エラー表示 |
| ors -s track --user/-u * | | wiki/<user(全て)>/tracks/md一覧 |
| ors -s track --user/-u * 1 | | wiki/<user(全て)>/tracks/1のmdの中身一覧 |
| ors -s track --user/-u * 1 5 | | wiki/<user(全て)>/tracks/1のmdの5を表示 |
| ors -s track --user/-u * 1 5 --del | | エラー表示 |
| ors -s track --user/-u * 1 5 --run | | wiki/<user(全て)>/tracks/1のmdの5を実行 |
| ors -s track --user/-u user名 | | wiki/user名/tracks/md一覧 |
| ors -s track --user/-u user名 1 | | wiki/user名/tracks/1のmdの中身一覧 |
| ors -s track --user/-u user名 1 5 | | wiki/user名/tracks/1のmdの5を表示 |
| ors -s track --user/-u user名 1 5 --del | | エラー表示 |
| ors -s track --user/-u user名 1 5 --run | | wiki/user名/tracks/1のmdの5を実行 |
| ors -s writeup | records/writeups/(ホルダ&md)一覧 | wiki/<user(self)/writeups/(ホルダ&md)一覧 |
| ors -s writeup 1 | records/writeups/(ホルダ ? 中身一覧 : md内容表示) | wiki/<user(self)/writeups/(ホルダ ? 中身一覧 : md内容表示) |
| ors -s writeup --user/-u | | エラー表示 |
| ors -s writeup --user/-u * | | wiki/user(全て)/writeups/(ホルダ&md)一覧 |
| ors -s writeup --user/-u * 1 | |  wiki/user名/writeups/(ホルダ ? 中身一覧 : mdの内容表示) |
| ors -s writeup --user/-u user名 | | wiki/user名/writeups/(ホルダ&md)一覧 |
| ors -s writeup --user/-u user名 1 | |  wiki/user名/writeups/(ホルダ ? 中身一覧 : mdの内容表示) |
| ors -q query ping | records/commands+tracksの検索結果一覧 | wiki/<user(self)/commands+tracksの検索結果一覧 |
| ors -q query ping 1 | 検索結果の1を表示 | 検索結果の1を表示 |
| ors -q query ping 1 --del | 検索結果の1を削除 | 検索結果の1を削除 |
| ors -q query ping 1 --run | 検索結果の1を実行 | 検索結果の1を実行 |
| ors -q query --user/-u | | エラー表示 |
| ors -q query --user/-u * ping | | wiki/user(全て)/commands+tracksの検索結果一覧 |
| ors -q query --user/-u * ping 1 | | 検索結果の1を表示 |
| ors -q query --user/-u * ping 1 --del | | エラー表示 |
| ors -q query --user/-u * ping 1 --run | | 検索結果の1を実行 |
| ors -q query --user/-u user名 ping | | wiki/user名/commands+tracksの検索結果一覧 |
| ors -q query --user/-u user名 ping 1 | | 検索結果の1を表示 |
| ors -q query --user/-u user名 ping 1 --del | | エラー表示 |
| ors -q query --user/-u user名 ping 1 --run | | 検索結果の1を実行 |


#### 顕在している課題

1. writeupはいわば自由なmdであり、ユーザーはローカルで好きな場所に画像をおいて、mdから参照させることが可能。この場合、ローカルでは画像が表示されるが、wikiにアップするとパス(url)が合わずに、wiki上では画像が表示されない。

