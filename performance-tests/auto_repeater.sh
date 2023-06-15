#!/bin/bash


script="sshpy.py"

for i in $(seq 1 5); do
	mkdir "p$i.logs"
	cd "p$i.logs"
	echo "starting n $i"
	python3 $script > "p$i.log.txt" 2>&1 &
	cd ..
done

wait

echo "complete"
