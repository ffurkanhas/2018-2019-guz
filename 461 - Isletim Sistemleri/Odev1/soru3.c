#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main(){

  char *args[] = {"/bin/echo", "Hello FFH", NULL};

  int p = fork();

  if(p == 0){
    //child proccess
    execvp("echo", args);
  }

  else {
    //main proccess
  }
}
