#!/bin/bash

PGPASSWORD=
export PGPASSWORD

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_HOST=
DUMP_PATH=

pg_dump -U $POSTGRES_USER -h $POSTGRES_HOST $POSTGRES_DB | gzip > $DUMP_PATH/psql_dump_$(date "+%Y-%m-%d").sql.gz

unset PGPASSWORD

