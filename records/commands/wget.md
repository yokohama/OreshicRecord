## linpeas取得

```bash
banister@~/projects/oscp/thm/basicpentestingjt Tinkpad$ wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh
```

```
--2026-01-17 17:05:49--  https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh
Resolving github.com (github.com)... 20.27.177.113
Connecting to github.com (github.com)|20.27.177.113|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://github.com/peass-ng/PEASS-ng/releases/download/20260116-d4b8a4ba/linpeas.sh [following]
--2026-01-17 17:05:49--  https://github.com/peass-ng/PEASS-ng/releases/download/20260116-d4b8a4ba/linpeas.sh
Reusing existing connection to github.com:443.
HTTP request sent, awaiting response... 302 Found
Location: https://release-assets.githubusercontent.com/github-production-release-asset/165548191/d58bdb90-a7cf-4f07-92d0-5ddbd24c8cb5?sp=r&sv=2018-11-09&sr=b&spr=https&se=2026-01-17T08%3A56%3A30Z&rscd=attachment%3B+filename%3Dlinpeas.sh&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2026-01-17T07%3A56%3A08Z&ske=2026-01-17T08%3A56%3A30Z&sks=b&skv=2018-11-09&sig=iuNepG%2FqWp5p7xrcLYkWYCQBsE9as24cPIW%2BkuEDbEY%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc2ODYzNzQxNCwibmJmIjoxNzY4NjM3MTE0LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.L_ff6KqslOcbG1-v8WmJ59SKCAeDcpqPhyJkl8yKy3g&response-content-disposition=attachment%3B%20filename%3Dlinpeas.sh&response-content-type=application%2Foctet-stream [following]
--2026-01-17 17:05:49--  https://release-assets.githubusercontent.com/github-production-release-asset/165548191/d58bdb90-a7cf-4f07-92d0-5ddbd24c8cb5?sp=r&sv=2018-11-09&sr=b&spr=https&se=2026-01-17T08%3A56%3A30Z&rscd=attachment%3B+filename%3Dlinpeas.sh&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2026-01-17T07%3A56%3A08Z&ske=2026-01-17T08%3A56%3A30Z&sks=b&skv=2018-11-09&sig=iuNepG%2FqWp5p7xrcLYkWYCQBsE9as24cPIW%2BkuEDbEY%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc2ODYzNzQxNCwibmJmIjoxNzY4NjM3MTE0LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.L_ff6KqslOcbG1-v8WmJ59SKCAeDcpqPhyJkl8yKy3g&response-content-disposition=attachment%3B%20filename%3Dlinpeas.sh&response-content-type=application%2Foctet-stream
Resolving release-assets.githubusercontent.com (release-assets.githubusercontent.com)... 185.199.110.133, 185.199.111.133, 185.199.108.133, ...
Connecting to release-assets.githubusercontent.com (release-assets.githubusercontent.com)|185.199.110.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 983276 (960K) [application/octet-stream]
Saving to: ‘linpeas.sh.1’

     0K .......... .......... .......... .......... ..........  5% 15.2M 0s
    50K .......... .......... .......... .......... .......... 10% 25.1M 0s
   100K .......... .......... .......... .......... .......... 15% 37.6M 0s
   150K .......... .......... .......... .......... .......... 20%  112M 0s
   200K .......... .......... .......... .......... .......... 26% 32.6M 0s
   250K .......... .......... .......... .......... .......... 31%  119M 0s
   300K .......... .......... .......... .......... .......... 36% 71.8M 0s
   350K .......... .......... .......... .......... .......... 41%  120M 0s
   400K .......... .......... .......... .......... .......... 46%  112M 0s
   450K .......... .......... .......... .......... .......... 52% 59.1M 0s
   500K .......... .......... .......... .......... .......... 57%  132M 0s
   550K .......... .......... .......... .......... .......... 62%  134M 0s
   600K .......... .......... .......... .......... .......... 67% 84.4M 0s
   650K .......... .......... .......... .......... .......... 72%  221M 0s
   700K .......... .......... .......... .......... .......... 78% 93.7M 0s
   750K .......... .......... .......... .......... .......... 83% 84.6M 0s
   800K .......... .......... .......... .......... .......... 88%  121M 0s
   850K .......... .......... .......... .......... .......... 93%  150M 0s
   900K .......... .......... .......... .......... .......... 98% 91.2M 0s
   950K ..........                                            100%  234M=0.02s

2026-01-17 17:05:49 (62.2 MB/s) - ‘linpeas.sh.1’ saved [983276/983276]

```

## winPEASx64.exeの取得

```bash
banister@~/projects/oscp/thm Tinkpad$ wget https://github.com/peass-ng/PEASS-ng/releases/download/20260121-aabd17ef/winPEASx64.exe
```

```

```

## winPEASx86.exeの取得

```bash
banister@~/projects/oscp/thm Tinkpad$ wget https://github.com/peass-ng/PEASS-ng/releases/download/20260121-aabd17ef/winPEASx86.exe
```

```
```

## windows用のnc.exeの取得

```bash
banister@~/projects/oscp/thm/steelmountain Tinkpad$ wget https://github.com/andrew-d/static-binaries/raw/refs/heads/master/binaries/windows/x86/ncat.exe
```

```
```

