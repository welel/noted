#!/bin/bash

PGPASSWORD=
export PGPASSWORD

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_HOST=
pathToDump=

cd $pathToDump
if [ -f PostgreSQL_dump_$(date "+%Y-%m-%d-%HH").sql.gz ]; then
    gzip -d -f PostgreSQL_dump_$(date "+%Y-%m-%d-%HH").sql.gz
fi

psql -U $POSTGRES_USER -h $POSTGRES_HOST -d $POSTGRES_DB < PostgreSQL_dump_$(date "+%Y-%m-%d-%HH").sql > /dev/null 2>&1


unset PGPASSWORD