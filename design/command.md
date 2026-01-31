# command

ors -m "MSG" <command> を実行したときに、records/commandsに保存される内容。

例えば、`ors -m "MSG" ping 8.8.8.8` としたら、records/commands/ping.mdが作成される。ファイル名は実行されたコマンド名になる。既にファイルが存在する場合は、追記される。
以下が、ors -m "MSG” を実行した時に追加される、ユニット。

例： `ors -m "回数指定" -t "TAG1,TAG2,TAG3" -d "説明、説明・・・・" ping -c 3 8.8.8.8

--- ここから

## 回数指定

- タグ

```tag
TAG1,TAG2,TAG3
```

- 説明

```desc
説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、 説明、
```

- コマンド

```bash
ping -c 3 8.8.8.8
```

- output

```bash
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=116 time=4.10 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=116 time=4.30 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=116 time=4.09 ms
^C
--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 4.090/4.163/4.304/0.099 ms
                                                                                                                                                                                                           
```

--- ここまで

-mは必須。
-t -dは任意。指定されなかった場合は、tagコードスニペット、descスニペットが空で作成される。
また、-q / --quitがつけられた時は、outpuのbashコードスニペットは空で作成される。


# track

commandが、実行コマンド名で `records/commands/<実行コマンド名>.md` でファイルが作成されるのに対して、
trackは、track名を指定して、一連の `ors -m "MSG" 実行コマンド`を、`records/tracks/<トラック名>.md` に保存する。

track名のつけ方は、 `ors -t/--track "トラック名"` で、値は、`ORESHIC_TRACK` に保存される。
`ORESHIC_TRACK` が存在する間は、全ての `ors -m "MSG" コマンド` は、track名.mdに保存される。
解除するときは、 `ors -u/--unset "トラック名"` を実行する。

commandと、trackの違いはファイルを指定するかしないかであり、保存されるフォーマットは全く一緒である。

ORESHIC_TRACKが存在しない場合は、`records/command<実行コマンド名>.md` に保存される。
