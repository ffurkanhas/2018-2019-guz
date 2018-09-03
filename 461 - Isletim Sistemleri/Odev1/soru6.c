#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>
#include <stdlib.h>

int main (){

  int fd[2];
  int temp;
  pipe (fd);
  char string[80];
  char readbuffer[80];

  int p = fork ();

  if (p == 0) {
    close(fd[0]);
    printf("Bir string giriniz: ");
    scanf("%s", string);
    write(fd[1], string, (strlen(string)+1));
    exit(0);
  }
  else {
    close(fd[1]);
    temp = read(fd[0], readbuffer, sizeof(readbuffer));
    printf("Cocuktan gelen: %s\n", readbuffer);
  }

return 0;
}
