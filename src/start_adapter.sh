#!/bin/sh

while [ 1 ]; do
	nc -z sprc3_broker 1883 2> /dev/null \
	&& break;

	sleep 1;
done

python3 -u adapter.py