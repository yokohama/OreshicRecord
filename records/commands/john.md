## フォーマット一覧

```bash
banister@~/projects/OreshicRecord kali$ john --list=formats
```

```
descrypt, bsdicrypt, md5crypt, md5crypt-long, bcrypt, scrypt, LM, AFS, 
416 formats (149 dynamic formats shown as just "dynamic_n" here)
tripcode, AndroidBackup, adxcrypt, agilekeychain, aix-ssha1, aix-ssha256, 
aix-ssha512, andOTP, ansible, argon2, as400-des, as400-ssha1, asa-md5, 
AxCrypt, AzureAD, BestCrypt, BestCryptVE4, bfegg, Bitcoin, BitLocker, 
bitshares, Bitwarden, BKS, Blackberry-ES10, WoWSRP, Blockchain, chap, 
Clipperz, cloudkeychain, dynamic_n, cq, CRC32, cryptoSafe, sha1crypt, 
sha256crypt, sha512crypt, Citrix_NS10, dahua, dashlane, diskcryptor, Django, 
django-scrypt, dmd5, dmg, dominosec, dominosec8, DPAPImk, dragonfly3-32, 
dragonfly3-64, dragonfly4-32, dragonfly4-64, Drupal7, eCryptfs, eigrp, 
electrum, EncFS, enpass, EPI, EPiServer, ethereum, fde, Fortigate256, 
Fortigate, FormSpring, FVDE, geli, gost, gpg, HAVAL-128-4, HAVAL-256-3, hdaa, 
hMailServer, hsrp, IKE, ipb2, itunes-backup, iwork, KeePass, keychain, 
keyring, keystore, known_hosts, krb4, krb5, krb5asrep, krb5pa-sha1, krb5tgs, 
krb5-17, krb5-18, krb5-3, kwallet, lp, lpcli, leet, lotus5, lotus85, LUKS, 
MD2, mdc2, MediaWiki, monero, money, MongoDB, scram, Mozilla, mscash, 
mscash2, MSCHAPv2, mschapv2-naive, krb5pa-md5, mssql, mssql05, mssql12, 
multibit, mysqlna, mysql-sha1, mysql, net-ah, nethalflm, netlm, netlmv2, 
net-md5, netntlmv2, netntlm, netntlm-naive, net-sha1, nk, notes, md5ns, 
nsec3, NT, o10glogon, o3logon, o5logon, ODF, Office, oldoffice, 
OpenBSD-SoftRAID, openssl-enc, oracle, oracle11, Oracle12C, osc, ospf, 
Padlock, Palshop, Panama, PBKDF2-HMAC-MD4, PBKDF2-HMAC-MD5, PBKDF2-HMAC-SHA1, 
PBKDF2-HMAC-SHA256, PBKDF2-HMAC-SHA512, PDF, PEM, pfx, pgpdisk, pgpsda, 
pgpwde, phpass, PHPS, PHPS2, pix-md5, PKZIP, po, postgres, PST, PuTTY, 
pwsafe, qnx, RACF, RACF-KDFAES, radius, RAdmin, RAKP, rar, RAR5, Raw-SHA512, 
Raw-Blake2, Raw-Keccak, Raw-Keccak-256, Raw-MD4, Raw-MD5, Raw-MD5u, Raw-SHA1, 
Raw-SHA1-AxCrypt, Raw-SHA1-Linkedin, Raw-SHA224, Raw-SHA256, Raw-SHA3, 
Raw-SHA384, restic, ripemd-128, ripemd-160, rsvp, RVARY, Siemens-S7, 
Salted-SHA1, SSHA512, sapb, sapg, saph, sappse, securezip, 7z, Signal, SIP, 
skein-256, skein-512, skey, SL3, Snefru-128, Snefru-256, LastPass, SNMP, 
solarwinds, SSH, sspr, Stribog-256, Stribog-512, STRIP, SunMD5, SybaseASE, 
Sybase-PROP, tacacs-plus, tcp-md5, telegram, tezos, Tiger, tc_aes_xts, 
tc_ripemd160, tc_ripemd160boot, tc_sha512, tc_whirlpool, vdi, OpenVMS, vmx, 
VNC, vtp, wbb3, whirlpool, whirlpool0, whirlpool1, wpapsk, wpapsk-pmk, 
xmpp-scram, xsha, xsha512, zed, ZIP, ZipMonster, plaintext, has-160, 
HMAC-MD5, HMAC-SHA1, HMAC-SHA224, HMAC-SHA256, HMAC-SHA384, HMAC-SHA512, 
dummy, crypt
```

## 高速化。CUPコア数指定。フォーマット指定。リスト指定。

```bash
banister@~/projects/oscp/thm/networkservices2 Tinkpad$ john --fork=14 --format=mysql-sha1 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

```
Loaded 1 password hash (mysql-sha1, MySQL 4.1+ [SHA1 256/256 AVX2 8x])
Created directory: /home/banister/.john
doggie           (?)     
Using default input encoding: UTF-8
Node numbers 1-14 of 14 (fork)
6 1g 0:00:00:00 DONE (2026-01-13 09:21) 20.00g/s 2400p/s 2400c/s 2400C/s annie..ingeras
Press Ctrl-C to abort, or send SIGUSR1 to john process for status
3 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 3104Kp/s 3104Kc/s 3104KC/s   3879.ie168
2 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 3201Kp/s 3201Kc/s 3201KC/s xCvBnM,
13 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 3201Kp/s 3201Kc/s 3201KC/s  32500000 ..                  
12 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 2926Kp/s 2926Kc/s 2926KC/s        1
14 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 3201Kp/s 3201Kc/s 3201KC/s  3117548331..            
10 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 3201Kp/s 3201Kc/s 3201KC/s  0188579722..      7
5 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 3201Kp/s 3201Kc/s 3201KC/s    3197337.a6_123
7 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 3012Kp/s 3012Kc/s 3012KC/s  08 22 0128..     mara
9 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 3304Kp/s 3304Kc/s 3304KC/s    0109381602..     123d
4 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 3012Kp/s 3012Kc/s 3012KC/s  8751617171854.abygurl69
8 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 3012Kp/s 3012Kc/s 3012KC/s  _ 09..     54321
11 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 2845Kp/s 2845Kc/s 2845KC/s   cq90000..       1234567
1 0g 0:00:00:00 DONE (2026-01-13 09:21) 0g/s 2695Kp/s 2695Kc/s 2695KC/s    667306   ..           
Waiting for 13 children to terminate
Session completed. 
```

