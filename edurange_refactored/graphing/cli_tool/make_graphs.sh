#!/bin/bash

echo -n "Please enter the name of csv blob: "
read filename

echo -n "Please enter the <Scenario_Name>: "
read scenario

python3 batch_process_csv.py $filename

echo "Processing CSV..."

wait

echo "Creating Graphs..."

for file in ./usercsv/*
do
  python3 cli_graphing.py $file $scenario ./usergraphs/
done

echo "Look in ./usercsv/ and ./usergraphs/ for your files."


