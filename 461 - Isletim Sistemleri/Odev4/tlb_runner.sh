#!/bin/bash

echo -e "Page_Number     Trials     Seconds"

for (( i=0; i <= 2000; ++i ))
do
    ./tlb $i "3000"
done
