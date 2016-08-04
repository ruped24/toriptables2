#!/bin/bash

#Change proxy every DELAY seconds for MAX times
FILE=toriptables2.py
COUNTER=0
MAX=$1 #
DELAY=$2

#Check if args was received
if [ $# -ne 2 ]; then 
	echo "USAGE: sudo ${0} <number-of-repetitions> <delay-between-repetitions>"
	exit
fi

#iptables dropping packets makes sure your real ip isn't leaked if webpage
#is being fetched during the proxy reload.
while [ ${COUNTER} -lt ${MAX} ]; do
	iptables -w -P OUTPUT DROP
	${FILE} -l
	iptables -w -P OUTPUT ACCEPT
	sleep ${DELAY}
	let "COUNTER += 1"
done
