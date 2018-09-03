#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main(){

    int p = fork();

    if (p == 0){
      fclose(stdout);
      printf("Child deneme");
    }
    else{
      printf("Parent calisti\n");
      wait(NULL);
      printf("Child sonladi\n");
    }
}
