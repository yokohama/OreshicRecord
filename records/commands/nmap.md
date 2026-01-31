## well-known ports(0-1023)

```bash
banister@~/projects/OreshicRecord kali$ nmap xx.xx.xx.xx
```

```
```

## registed ports(-49151)

```bash
banister@~/projects/OreshicRecord kali$ nmap -p-49151 xx.xx.xx.xx
```

```
```

## all ports(-65535)

```bash
banister@~/projects/OreshicRecord kali$ nmap -p- xx.xx.xx.xx
```

```
```

## ライブホストスキャン。pingスキャンのみをおこない、OSやポートスキャンをおこなわない

```bash
banister@~/projects/OreshicRecord kali$ nmap -sn xx.xx.xx.xx/24
```

```
```


## ARPスキャン

```bash
banister@~/projects/OreshicRecord kali$ sudo nmap -PR -sn xx.xx.xx.xx/24
```

```
```


## ICMP Echoスキャン

```bash
banister@~/projects/OreshicRecord kali$ sudo nmap -PE -sn xx.xx.xx.xx/24
```

```
```


## ICMP Timestampスキャン

```bash
banister@~/projects/OreshicRecord kali$ sudo nmap -PP -sn xx.xx.xx.xx/24
```

```
```


## ICMP Address Maskスキャン

```bash
banister@~/projects/OreshicRecord kali$ sudo nmap -PM -sn xx.xx.xx.xx/24
```

```
```


## ライブホストスキャン。SYN pingスキャン。指定ポートにSYNを送っている。実際のpingではない。F/Wで空いてそうなポートを指定して、試してみる時に使う。

```bash
banister@~/projects/OreshicRecord kali$ sudo nmap -PS22,80,443 -sn xx.xx.xx.xx
```

```
```


## ライブホストスキャン。ACK pingスキャン。指定ポートにACKを送っている。実際のpingではない。F/Wで空いてそうなポートを指定して、試してみる時に使う。

```bash
banister@~/projects/OreshicRecord kali$ sudo nmap -PA22,80,443 -sn xx.xx.xx.xx
```

```
```


## ライブホストスキャン。UDP pingスキャン。指定ポートに空のUDPパケットを送っている。実際のpingではない。F/Wで空いてそうなポートを指定して、試してみる時に使う。

```bash
banister@~/projects/OreshicRecord kali$ sudo nmap -PU53 -sn xx.xx.xx.xx
```

```
```


## IPアドレス範囲指定

```bash
banister@~/projects/oscp/thm Tinkpad$ nmap 192.168.0.1-10
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-06 09:04 JST
```

## ライブホストスキャン(内部でICMP / ARP / TCPを自動で使用)

```bash
banister@~/projects/oscp/thm Tinkpad$ nmap -sn 192.168.1.1
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-06 09:08 JST
Nmap scan report for 192.168.1.1
Host is up (0.0011s latency).
Nmap done: 1 IP address (1 host up) scanned in 0.10 seconds
```

## 範囲指定した場合の対象のIPを見たい場合

```bash
banister@~ Tinkpad$ nmap -sL 192.168.0.1/27
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-06 09:24 JST
Nmap scan report for 192.168.0.0
Nmap scan report for 192.168.0.1
Nmap scan report for 192.168.0.2
Nmap scan report for 192.168.0.3
Nmap scan report for 192.168.0.4
Nmap scan report for 192.168.0.5
Nmap scan report for 192.168.0.6
Nmap scan report for 192.168.0.7
Nmap scan report for 192.168.0.8
Nmap scan report for 192.168.0.9
Nmap scan report for 192.168.0.10
Nmap scan report for 192.168.0.11
Nmap scan report for 192.168.0.12
Nmap scan report for 192.168.0.13
Nmap scan report for 192.168.0.14
Nmap scan report for 192.168.0.15
Nmap scan report for 192.168.0.16
Nmap scan report for 192.168.0.17
Nmap scan report for 192.168.0.18
Nmap scan report for 192.168.0.19
Nmap scan report for 192.168.0.20
Nmap scan report for 192.168.0.21
Nmap scan report for 192.168.0.22
Nmap scan report for 192.168.0.23
Nmap scan report for 192.168.0.24
Nmap scan report for 192.168.0.25
Nmap scan report for 192.168.0.26
Nmap scan report for 192.168.0.27
Nmap scan report for 192.168.0.28
Nmap scan report for 192.168.0.29
Nmap scan report for 192.168.0.30
Nmap scan report for 192.168.0.31
Nmap done: 32 IP addresses (0 hosts up) scanned in 0.04 seconds
```

## UDPスキャン

```bash
banister@~ Tinkpad$ nmap -sU -p53 192.168.1.1
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-06 09:31 JST
Nmap scan report for 192.168.1.1
Host is up (0.0072s latency).

PORT   STATE SERVICE
53/udp open  domain

Nmap done: 1 IP address (1 host up) scanned in 0.26 seconds
```

## OSスキャン

```bash
banister@~ Tinkpad$ nmap -O 192.168.1.1
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-06 09:52 JST
Nmap scan report for 192.168.1.1
Host is up (0.0020s latency).
Not shown: 995 closed tcp ports (reset)
PORT      STATE    SERVICE
23/tcp    filtered telnet
53/tcp    open     domain
80/tcp    open     http
443/tcp   open     https
52869/tcp open     unknown
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.14
Network Distance: 2 hops

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 2.67 seconds
```

## 解放ポートのバージョンスキャン

```bash
banister@~ Tinkpad$ nmap -sV 192.168.1.1
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-06 09:53 JST
Nmap scan report for 192.168.1.1
Host is up (0.0030s latency).
Not shown: 995 closed tcp ports (reset)
PORT      STATE    SERVICE   VERSION
23/tcp    filtered telnet
53/tcp    open     domain    Unbound
80/tcp    open     http
443/tcp   open     ssl/https
52869/tcp open     upnp      Portable SDK for UPnP devices 1.6.22 (UPnP 1.0)
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port80-TCP:V=7.95%I=7%D=1/6%Time=695C5D11%P=x86_64-pc-linux-gnu%r(GetRe
SF:quest,4C8,"HTTP/1\.0\x20302\x20Moved\x20Temporarily\r\nConnection:\x20c
SF:lose\r\nCache-Control:\x20no-cache,no-store\r\nPragma:\x20no-cache\r\nC
SF:ontent-Length:\x20793\r\nSet-Cookie:\x20SID=c8b7cf2508f51ba54e299d2af62
SF:ab06e889ed7173308a9a2f25de7dac6704959;\x20PATH=/;\x20HttpOnly;\x20SameS
SF:ite=strict\r\nServer:\x20\r\nAccept-Ranges:\x20bytes\r\nX-Content-Type-
SF:Options:\x20nosniff\r\nX-XSS-Protection:\x201;\x20mode=block\r\nX-Frame
SF:-Options:\x20SAMEORIGIN\r\nLocation:\x20https:///\r\nContent-Type:\x20t
SF:ext/html;\x20charset=utf-8\r\n\r\n\n<html>\n<head>\n<title>302\x20Found
SF:</title>\n</head>\n<body\x20bgcolor=\"#FFFFFF\"\x20text=\"#000000\"\x20
SF:link=\"#2020ff\"\x20vlink=\"#4040cc\">\n<h2>302\x20Found</h2>\n<span>Th
SF:e\x20requested\x20URL\x20is\x20going\x20to\x20be\x20https\.</span>\n<di
SF:v\x20style=\"display:none\">\n<span>Padding\x20so\x20that\x20MSIE\x20de
SF:igns\x20to\x20show\x20this\x20error\x20instead\x20of\x20its\x20own\x20c
SF:anned\x20one\.</span>\n<span>Padding\x20so\x20that\x20MSIE\x20deigns\x2
SF:0to\x20show\x20this\x20error\x20instead\x20of\x20its\x20own\x20canned\x
SF:20one\.</span>\n<span>Padding\x20so\x20that\x20MSIE\x20deigns\x20to\x20
SF:show\x20this\x20error\x20instead\x20of\x20its\x20o")%r(HTTPOptions,594,
SF:"HTTP/1\.1\x20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-
SF:Type:\x20text/html;\x20charset=iso-8859-1\r\nX-Content-Type-Options:\x2
SF:0nosniff\r\nX-XSS-Protection:\x201;\x20mode=block\r\nX-Frame-Options:\x
SF:20SAMEORIGIN\r\nCache-Control:\x20no-cache,no-store\r\nPragma:\x20no-ca
SF:che\r\n\r\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20<html>\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20<head><title>400\x20Bad\x20Request</title></head>\n\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<body\x20bgcolor
SF:=\"#FFFFFF\"\x20text=\"#000000\"\x20link=\"#2020ff\"\x20vlink=\"#4040cc
SF:\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:<h2>400\x20Bad\x20Request</h2>\nYour\x20request\x20has\x20bad\x20syntax
SF:\x20or\x20is\x20inherently\x20impossible\x20to\x20satisfy\.\n<div\x20st
SF:yle=\"display:none\">\n<ajax_response_xml_root>\n<IF_ERRORSTR>SessionTi
SF:meout</IF_ERRORSTR>\n<IF_ERRORPARAM>SUCC</IF_ERRORPARAM>\n<IF_ERRORTYPE
SF:>SUCC</IF_ERRORTYPE>\n</ajax_response_xml_root>\n<span>Padding\x20so\x2
SF:0that\x20MSIE\x20deigns\x20to\x20show\x20this\x20e");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port443-TCP:V=7.95%T=SSL%I=7%D=1/6%Time=695C5D13%P=x86_64-pc-linux-gnu%
SF:r(GetRequest,41F1,"HTTP/1\.0\x20200\x20OK\r\nConnection:\x20close\r\nCa
SF:che-Control:\x20no-cache,no-store\r\nPragma:\x20no-cache\r\nContent-Len
SF:gth:\x20155838\r\nSet-Cookie:\x20SID_HTTPS_=0f1968d1d2f57aba228035cbd58
SF:82d3ebbdb2c29a03e55bd695bda27ed79420e;\x20PATH=/;\x20Secure;\x20HttpOnl
SF:y;\x20SameSite=strict\r\nSet-Cookie:\x20_TESTCOOKIESUPPORT_HTTPS_=1;\x2
SF:0PATH=/;\x20Secure;\x20HttpOnly;\x20SameSite=strict\r\nServer:\x20\r\nA
SF:ccept-Ranges:\x20bytes\r\nX-Content-Type-Options:\x20nosniff\r\nX-XSS-P
SF:rotection:\x201;\x20mode=block\r\nX-Frame-Options:\x20SAMEORIGIN\r\nCon
SF:tent-Type:\x20text/html;\x20charset=utf-8\r\n\r\n<!DOCTYPE\x20HTML\x20P
SF:UBLIC\x20\"-//W3C//DTD\x20HTML\x204\.01\x20Transitional//EN\"\x20\"http
SF:://www\.w3\.org/TR/html4/transitional\.dtd\">\n<html\x20xmlns=\"http://
SF:www\.w3\.org/1999/xhtml\">\n<head>\n<meta\x20http-equiv=\"Content-Type\
SF:"\x20content=\"text/html;\x20charset=utf-8\"\x20/>\n<meta\x20http-equiv
SF:=\"X-UA-Compatible\"\x20content=\"IE=edge\">\n\n<link\x20rel=\"shortcut
SF:\x20icon\"\x20href=\"/img/favicon\.ico\"\x20/>\n\n<title>&#70;&#54;&#54
SF:;&#48;&#80;</title>\n<style\x20type=\"text/css\"")%r(FourOhFourRequest,
SF:587,"HTTP/1\.0\x20404\x20Not\x20Found\r\nConnection:\x20close\r\nConten
SF:t-Type:\x20text/html;\x20charset=iso-8859-1\r\nX-Content-Type-Options:\
SF:x20nosniff\r\nX-XSS-Protection:\x201;\x20mode=block\r\nX-Frame-Options:
SF:\x20SAMEORIGIN\r\nCache-Control:\x20no-cache,no-store\r\nPragma:\x20no-
SF:cache\r\n\r\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:\x20\x20<html>\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20<head><title>404\x20Not\x20Found</title></head>\n\x20\x20\x2
SF:0\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20<body\x20bgcolor
SF:=\"#FFFFFF\"\x20text=\"#000000\"\x20link=\"#2020ff\"\x20vlink=\"#4040cc
SF:\">\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x
SF:20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\
SF:x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20
SF:<h2>404\x20Not\x20Found</h2>\n<span>The\x20requested\x20URL\x20was\x20n
SF:ot\x20found\x20on\x20this\x20server\.</span>\n<div\x20style=\"display:n
SF:one\">\n<ajax_response_xml_root>\n<IF_ERRORSTR>SessionTimeout</IF_ERROR
SF:STR>\n<IF_ERRORPARAM>SUCC</IF_ERRORPARAM>\n<IF_ERRORTYPE>SUCC</IF_ERROR
SF:TYPE>\n</ajax_response_xml_root>\n<span>Padding\x20so\x20that\x20MSIE\x
SF:20deigns\x20to\x20show\x20this\x20error\x20instead\x20");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.39 seconds
```

## ICMPを返さないホストをスキャンする

```bash
banister@~ Tinkpad$ nmap -Pn 192.168.1.1
```

```
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-06 09:55 JST
Nmap scan report for 192.168.1.1
Host is up (0.0037s latency).
Not shown: 995 closed tcp ports (reset)
PORT      STATE    SERVICE
23/tcp    filtered telnet
53/tcp    open     domain
80/tcp    open     http
443/tcp   open     https
52869/tcp open     unknown

Nmap done: 1 IP address (1 host up) scanned in 1.29 seconds
```

