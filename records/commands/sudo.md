## sudoで実行できるファイル一覧

```bash
banister@~/projects/OreshicRecord kali$ sudo -l
```

```
既定値のエントリと照合中 (ユーザー名 banister) (ホスト名 kali):
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

ユーザー banister は kali 上で コマンドを実行できます
    (ALL : ALL) ALL
```

## 1階層指定でディスク使用量の確認

```bash
banister@~ Tinkpad$ sudo du -h -d 1 /opt
```

```
876M	/opt/BurpSuitePro
12M	/opt/mdcat-2.7.1-x86_64-unknown-linux-gnu
60M	/opt/nvim-linux-x86_64
12K	/opt/containerd
947M	/opt
```

## NFS: マウント

```bash
# NFSサーバーの設定により、vers=を、2 / 3 / 4 や、nolockをなくしてみたり調整する。
sudo mount -t nfs -o vers=3,nolock  10.49.164.155:/tmp ./mount
```

```
```

## SUID: setuidのみつける

```bash
banister@~/projects/oscp/thm/networkservices2/mount/cappucino Tinkpad$ sudo chmod u+s ./bash
```

```
```

## SGID: setgidのみつける

```bash
banister@~/projects/oscp/thm/networkservices2/mount/cappucino Tinkpad$ sudo chmod g+s ./bash
```

```
```

## ルート(/)配下のデスク使用量の確認

```bash
banister@~ Tinkpad$ sudo du -xh / --max-depth=1 | sort -h
```

```
6.9M	/etc
230M	/tmp
947M	/opt
3.0G	/home
2.0M	/boot
16G	/var
4.0K	/media
9.9G	/usr
8.0K	/mnt
140K	/root
16K	/lost+found
4.0K	/srv
30G	/
```

