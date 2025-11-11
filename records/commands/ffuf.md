## サブドメイン検索

```bash
banister@~/projects/OreshicRecord kali$ ffuf -u http://FUZZ.blog.yuhei.yokohama -w /home/banister/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
```

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://FUZZ.blog.yuhei.yokohama
 :: Wordlist         : FUZZ: /home/banister/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

:: Progress: [4989/4989] :: Job [1/1] :: 29 req/sec :: Duration: [0:01:06] :: Errors: 4989 ::
```

