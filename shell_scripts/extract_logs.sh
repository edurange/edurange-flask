#!/bin/bash


DATABASE_NAME=$1 #takes database name as a cli arg

if [ "$#" -ne 1 ]; then
    echo "Usage: './extract_logs.sh <database_name>'"
fi

#queries database and runs extract_logs.py on result
sudo -u postgres -H -- psql -d $DATABASE_NAME -R "+" -Atc "SELECT * FROM responses;" 2>/dev/null | ../py_scripts/extract_logs.py
