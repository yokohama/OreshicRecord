## SMBサーバーの情報を全て列挙

```bash
banister@~/projects/oscp/thm Tinkpad$ enum4linux -a 10.49.158.159
```

```
```
## SMBサーバーのグループ一覧を取得

```bash
banister@~/projects/oscp/thm/basicpentestingjt Tinkpad$ enum4linux -G 10.49.158.159
```

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Sat Jan 17 16:09:39 2026

 =========================================( Target Information )=========================================

Target ........... 10.49.158.159
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ===========================( Enumerating Workgroup/Domain on 10.49.158.159 )===========================


[E] Can't find workgroup/domain



 ===================================( Session Check on 10.49.158.159 )===================================

```

## SMBサーバーのグループ一覧を取得

```bash
banister@~/projects/oscp/thm/basicpentestingjt Tinkpad$ enum4linux -G 10.49.158.159
```

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Sat Jan 17 16:10:27 2026

 =========================================( Target Information )=========================================

Target ........... 10.49.158.159
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ===========================( Enumerating Workgroup/Domain on 10.49.158.159 )===========================


[E] Can't find workgroup/domain



 ===================================( Session Check on 10.49.158.159 )===================================

```

## SMBサーバーのshare一覧を取得

```bash
banister@~/projects/oscp/thm/basicpentestingjt Tinkpad$ enum4linux -S 10.49.158.159
```

```
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Sat Jan 17 16:11:22 2026

 =========================================( Target Information )=========================================

Target ........... 10.49.158.159
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ===========================( Enumerating Workgroup/Domain on 10.49.158.159 )===========================

```

