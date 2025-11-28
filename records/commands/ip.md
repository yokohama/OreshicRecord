## ルーティングの確認

```bash
banister@~/projects/OreshicRecord kali$ ip route show
```

```
default via 192.168.1.1 dev eth0 onlink 
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown 
172.18.0.0/16 dev br-58ba8baef5b8 proto kernel scope link src 172.18.0.1 linkdown 
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.105 
```

