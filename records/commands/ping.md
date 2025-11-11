## ほげ

```bash
banister@~/projects/OreshicRecord kali$ ping localhost
```

```
PING localhost (::1) 56 data bytes
64 bytes from localhost (::1): icmp_seq=1 ttl=64 time=0.013 ms
64 bytes from localhost (::1): icmp_seq=2 ttl=64 time=0.015 ms
64 bytes from localhost (::1): icmp_seq=3 ttl=64 time=0.046 ms
^C
--- localhost ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2040ms
rtt min/avg/max/mdev = 0.013/0.024/0.046/0.015 ms
```

## ほげ

```bash
banister@~/projects/OreshicRecord kali$ ping -c 3 localhost
```

```
PING localhost (::1) 56 data bytes
64 bytes from localhost (::1): icmp_seq=1 ttl=64 time=0.019 ms
64 bytes from localhost (::1): icmp_seq=2 ttl=64 time=0.059 ms
64 bytes from localhost (::1): icmp_seq=3 ttl=64 time=0.066 ms

--- localhost ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2045ms
rtt min/avg/max/mdev = 0.019/0.048/0.066/0.020 ms
```

