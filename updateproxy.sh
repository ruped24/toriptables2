#!/bin/bash

#Change proxy every DELAY seconds for MAX times
FILE=./toriptables2.py
COUNTER=0
MAX=$1 #
DELAY=$2

#Check if arg was received
if [ -z "$2" ]; then 
	echo "USAGE: sudo ./updateproxy.sh <number-of-repetitions> <delay-between-repetitions>"
	exit
fi

#iptables dropping packets makes sure your real ip isn't leaked if webpage
#is being fetched during the proxy reload.
while [ $COUNTER -lt $MAX ]; do
	iptables -P OUTPUT DROP
	python $FILE -l
	iptables -P OUTPUT ACCEPT
	sleep $DELAY
	let COUNTER=COUNTER+1
done
