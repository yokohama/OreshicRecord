# showで、最終的なmdを表示したときの、imgの相対パス問題

## 問題

- 表示されたパスが、mdファイルを起点として相対パスになっている。これ自体はデータの保存や関連として正しい。
- しかし、ユーザーが表示しようとした時、ユーザーのカレントディレクトリからの相対になるため、mdcatなどにパイプした場合、当然画像は表示されない。


## 解決案

- mdに記載されているパス(そのmdからimageまでの相対パス)は、正しいので、
- 表示時に、今自分がいるディレクトリと、そのmdが存在する場所を起点とした、./md_imagesのパスを変換させて表示する。
- これにより、ors -s command 1 1 などを実行した、標準出力を、| mdcatなどに渡し、画像も表示できる。

## 対象ソース

/ors/features/common.py#show_entry_detail_by_ids()
/ors/features/writeup.py#_show_writeup_by_indices()

show_entry_detail_by_ids()は中で加工している。むしろ、_show_wirteup_by_indices()に寄せたほうがシンプル。


# リダイレクトの後が記録されない

|や,>など

```
ors -m "クリップボードの中身を削除" echo -n | xclip -selection clipboard
ors -m "SUID検索" find / -perm -4000 -type f 2>/dev/null
```

# リダイレクトを含むコマンドの、--runが失敗する
