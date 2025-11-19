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


