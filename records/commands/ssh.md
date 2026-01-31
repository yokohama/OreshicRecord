## no matching host key typeのエラーが出た場合

```bash
banister@~/projects/oscp/thm/linuxprivesc Tinkpad$ ssh -oHostKeyAlgorithms=+ssh-rsa user@10.49.169.50
```

```
** WARNING: connection is not using a post-quantum key exchange algorithm.
** This session may be vulnerable to "store now, decrypt later" attacks.
** The server may need to be upgraded. See https://openssh.com/pq.html
```

