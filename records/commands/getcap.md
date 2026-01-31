## Linux capabilityの付与されたファイル一覧

```bash
banister@~/projects/oscp/thm/linuxprivescarena Tinkpad$ getcap -r / 2>/dev/null
```

```
/usr/lib/nmap/nmap cap_net_bind_service,cap_net_admin,cap_net_raw=eip
Failed to get capabilities of file '/mnt/c/Program Files/Microsoft SQL Server/MSSQL16.SQLEXPRESS/MSSQL/Template Data/tempdb.mdf' (Permission denied)
```
