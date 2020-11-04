#!/bin/bash

while read user; do
	for filename in /usr/local/src/logs/*/ttylog.*.*.*; do
		cat $filename > /usr/local/src/logs/$user/alltty.$(hostname).$user
    done

	python3 /usr/local/src/ttylog/analyze.py /usr/local/src/logs/$user/alltty.$(hostname).$user /usr/local/src/logs/$user/.cli.csv
	python3 /usr/local/src/ttylog/makeTsv.py /usr/local/src/logs/$user/.cli.csv /usr/local/src/logs/$user/.cli.log

done</usr/local/src/user_names.txt
	
