#!/bin/bash

echo "Enter date in FORMAT YYYY-MM-DD"
read date 

PGPASSWORD=
export PGPASSWORD
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_HOST=
dumpPATH=

set -e
	gzip -d $dumpPATH/pgsql_$date.sql.gz \
        && psql -U $POSTGRES_USER -h $POSTGRES_HOST -d $POSTGRES_DB < $dumpPATH/pgsql_$date.sql > /dev/null 2>&1
set +e

unset PGPASSWORD
 


