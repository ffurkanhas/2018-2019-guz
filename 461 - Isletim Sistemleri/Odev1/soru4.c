#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main(){

    int p = fork();

    if (p == 0)
        printf("Child calisti\n");
    else{
        printf("Parent calisti\n");
        wait(NULL);
        printf("Child sonladi\n");
    }
}
