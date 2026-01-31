## smtpユーザーの列挙

```bash
banister@~ Tinkpad$ smtp-user-enum -U /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt -t 10.49.154.224
```

```
Starting smtp-user-enum v1.2 ( http://pentestmonkey.net/tools/smtp-user-enum )

 ----------------------------------------------------------
|                   Scan Information                       |
 ----------------------------------------------------------

Mode ..................... VRFY
Worker Processes ......... 5
Usernames file ........... /usr/share/wordlists/seclists/Usernames/top-usernames-shortlist.txt
Target count ............. 1
Username count ........... 17
Target TCP port .......... 25
Query timeout ............ 5 secs
Target domain ............ 

######## Scan started at Mon Jan 12 10:10:33 2026 #########
10.49.154.224: root exists
10.49.154.224: administrator exists
10.49.154.224: vagrant exists
######## Scan completed at Mon Jan 12 10:10:35 2026 #########
3 results.

17 queries in 2 seconds (8.5 queries / sec)
```

