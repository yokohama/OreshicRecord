## ノーマル

```bash
banister@~/projects/OreshicRecord kali$ gobuster dir -u http://10.129.63.90 -w /home/banister/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt
```

```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.63.90
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /home/banister/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
Progress: 0 / 1 (0.00%)
2025/11/12 05:15:39 error on running gobuster on http://10.129.63.90/: timeout occurred during the request
```

## 拡張子で絞る

```bash
banister@~/projects/OreshicRecord kali$ gobuster dir -u http://10.129.63.90 -w /home/banister/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt -x php
```

```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.63.90
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /home/banister/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Extensions:              php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
Progress: 0 / 1 (0.00%)
2025/11/12 05:17:01 error on running gobuster on http://10.129.63.90/: timeout occurred during the request
```

## 不要なレングスやステータスを除外

```bash
banister@~/projects/oscp/thm/vulnversity Tinkpad$ gobuster dir -u http://10.48.172.237:3128 -w /usr/share/wordlists/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt --exclude-length 3594 --status-codes-blacklist 400
```

```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.48.172.237:3128
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt
[+] Negative Status codes:   400
[+] Exclude Length:          3594
[+] User Agent:              gobuster/3.8
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
```

