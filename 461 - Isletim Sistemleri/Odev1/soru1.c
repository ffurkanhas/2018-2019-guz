#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int counter = 0;

int main(){

  int p = fork();
  if( p == 0 ) {
    //this is child
    printf("child is working counter is: %d\n", counter);
    for (int i = 0; i < 5; i++) {
      counter++;
    }
    printf("%d\n", counter);
  }
  else{
    //this is parent
    counter = 0;
    printf("parent is working working counter is: %d\n", counter);
    for (int i = 0; i < 5; i++) {
      counter++;
    }
    printf("%d\n", counter);
  }
}
