#!/bin/bash

firstTown=$1

while [ $firstTown -le 25 ]
do
python3 bnn.py $firstTown
((firstTown++))
done
exit 0