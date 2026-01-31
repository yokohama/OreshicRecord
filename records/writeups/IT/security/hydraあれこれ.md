# Hydraあれこれ

## sshがパスワード認証を許可しているか？

```
└─$ hydra -l hogehogehoge -P /usr/share/wordlists/john.lst ssh://10.48.186.231 -s 22 -Fv
```

```
Hydra v9.6 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-01-17 15:00:23
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 3559 login tries (l:1/p:3559), ~223 tries per task
[DATA] attacking ssh://10.48.186.231:22/
[VERBOSE] Resolving addresses ... [VERBOSE] resolving done
[INFO] Testing if password authentication is supported by ssh://hogehogehoge@10.48.186.231:22
[INFO] Successful, password authentication is supported by ssh://10.48.186.231:22
^C[ERROR] Received signal 2, going down ...
The session file ./hydra.restore was written. Type "hydra -R" to resume session.
```

以下の2行が出ているため、パスワード認証を許可していると判断できる。 

```
[INFO] Testing if password authentication is supported by ssh://hogehogehoge@10.48.186.231:22
[INFO] Successful, password authentication is supported by ssh://10.48.186.231:22
```
