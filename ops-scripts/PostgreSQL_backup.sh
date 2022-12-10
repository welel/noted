#!/bin/bash

PGPASSWORD=
export PGPASSWORD

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_HOST=
pathToSaveDump=


pg_dump -U $POSTGRES_USER -h $POSTGRES_HOST $POSTGRES_DB | gzip > $pathToSaveDump/PostgreSQL_dump_$(date "+%Y-%m-%d-%HH").sql.gz

if [ $? -eq 0 ]; then
    echo "PostgreSQL dump saved to $pathToSaveDump";
else 
    echo "Error..Debug and try again."; 
    exit 1;
fi

unset PGPASSWORD