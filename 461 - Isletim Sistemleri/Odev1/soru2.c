#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main(){

  int p = fork();
  if( p == 0 ) {
    int i;
    //this is child
    printf("child is working\n");
    for (i = 0; i < 10; i++) {
      printf("%d\n", i);
    }
  }
  else{
    //this is parent
    int i;

    printf("parent is working\n");
    for (i = 10; i < 100; i++) {
      printf("%d\n", i);
    }
  }
}
