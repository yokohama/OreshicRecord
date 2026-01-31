- 以下のレスポンスが返ってこない

```
ors -m "sambaに接続" smbclient //10.49.170.179/profiles -U Anonymous

```

- writeupsが、-s queryの対象になっていない。

- wslに移行したせいで、vimの、:ClipPasteImgコマンドが動いていない。

kaliからwindowsのクリップボードには以下のコマンドでアクセスできるので、nvim/lua/yokohama/clip-paste-img.luaを修正

```
powershell.exe Get-Clipboard -Format Image

Tag                  :
PhysicalDimension    : {Width=284, Height=214}
Size                 : {Width=284, Height=214}
Width                : 284
Height               : 214
HorizontalResolution : 96
VerticalResolution   : 96
Flags                : 335888
RawFormat            : [ImageFormat: b96b3caa-0728-11d3-9d7b-0000f81ef32e]
PixelFormat          : Format32bppRgb
Palette              : System.Drawing.Imaging.ColorPalette
FrameDimensionsList  : {7462dc86-6180-4c7e-8e3f-ee7333a7a483}
PropertyIdList       : {}
PropertyItems        : {}
```


上記クリップボードの画像をセーブ

```
powershell.exe -Command "Add-Type -AssemblyName System.Windows.Forms;  [System.Windows.Forms.Clipboard]::GetImage().Save('/tmp/a.png')"
```

- --writeで、vimで編集

## UI設計


usage: ors [-h] [-s SEARCH [SEARCH ...]] [--run] [--del] [-m MESSAGE] [-q] [-t NAME] [-u] ...

Execute a command and save its output to Markdown.

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


