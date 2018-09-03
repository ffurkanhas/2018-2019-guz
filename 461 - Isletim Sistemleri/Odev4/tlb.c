#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sched.h>
#include <time.h>

double run(int, int);

int PAGESIZE = 0;

int main(int argc, char *argv[]){
  PAGESIZE = getpagesize();
  int page_number, trials_number;
  double result;

  if (argc != 3) {
    exit(0);
  }

  page_number = atoi(argv[1]);
  trials_number = atoi(argv[2]);

  result = run(page_number, trials_number);

  printf("%3d             %3d       %8.8f\n", page_number, trials_number, result);
}

double run(int page_number, int trials){
  int elements, i, j;
  int *arr, arr_size;
  
  elements = (PAGESIZE * page_number) / sizeof(int);
  arr = (int*) calloc(elements, sizeof(int));

  int jump = PAGESIZE / sizeof( int ) ;

  clock_t start_time = clock();

  for (j = 0; j < trials; j++) {
    for (i = 0; i < page_number * jump; i += jump) {
            arr[i] += 1;
    }
  }

  clock_t end_time = clock();

  double total_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;

  free(arr);

  return total_time;
}
