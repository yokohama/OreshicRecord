## UI設計

usage: ors [-h] [-s SEARCH [SEARCH ...]] [--run] [--del] [--open] [-m MESSAGE] [-q] [-t NAME] [-u] ...

positional arguments:
  command               command to execute

options:
  -h, --help            show this help message and exit
  -s, --search (command|track|writeup|code) <id...> -> print result with table format.
                        with -s query: <word> <id...> -> search by word in records dir & print result with table format.
  --run                 with -s (command|track) <file_id> <entry_id> -> re-run that entry now and record
  --del                 with -s (command|track) <file_id> <entry_id> -> delete that entry (if Count becomes 0, remove file)
  --open                with -s (command|track|writeup|query|code) <id...> -> open file with $EDITOR environment
  -m, --message MSG     with -t (command|track) -> save command or track with MSG
                        optional note to save
  -q, --quiet           do not save output to file
  -t, --track NAME      (this run only) set ORESHIC_TRACK for this process
  -u, --unset           (this run only) unset ORESHIC_TRACK for this process

### command.md format

## MSG

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
コマンド
```

- output
```bash
```


