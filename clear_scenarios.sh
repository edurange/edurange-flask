#!/bin/bash

DATABASE_NAME=$1

if [ "$#" -ne 1 ]; then
    echo "Usage: './clear_scenarios.sh <database_name>'"
fi



sudo -u postgres -H -- psql -d $DATABASE_NAME -c "DELETE FROM scenario_groups"
sudo -u postgres -H -- psql -d $DATABASE_NAME -c "DELETE FROM scenarios"

