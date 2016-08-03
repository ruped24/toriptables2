#!/bin/bash

#Change proxy every DELAY seconds for MAX times
FILE=./toriptables2.py
COUNTER=0
MAX=$1 #
DELAY=$2

#Check if arg was received
if [ -z "$2" ]; then 
	echo "USAGE: ./updateproxy.sh <number-of-repetitions <delay-between-repetitions>"
	exit
fi

while [ $COUNTER -lt $MAX ]; do
	python $FILE -l
	sleep $DELAY
	let COUNTER=COUNTER+1
done
