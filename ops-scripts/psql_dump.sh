#!/bin/bash
PGPASSWORD=
export PGPASSWORD
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_HOST= 
dumpPATH=

pg_dump -U $POSTGRES_USER -h $POSTGRES_HOST $POSTGRES_DB | gzip > $dumpPATH/pgsql_$(date "+%Y-%m-%d").sql.gz

unset PGPASSWORD
