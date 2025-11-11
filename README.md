# OreshicRecord

## Installation

1. Download

```
git clone git@github.com:yokohama/OreshicRecord.git

```

2. install

```
cd OreshicRecord
./install.sh
```


3. Quick start

```
# print help
ors

# command recoding with comment message
ors -m "test ping" ping localhost

# show list my commands
ors -s command

# show my command ditail
ors -s command ping -v 1

# run command from my command list
ors -s command ping --run 1
```
