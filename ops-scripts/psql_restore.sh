#!/bin/bash

###########################
### Restore psql dump   ###
###########################

PGPASSWORD=
export PGPASSWORD

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_HOST=
DUMP_PATH=

cd $DUMP_PATH

set -e
gzip -d -f psql_dump_$(date "+%Y-%m-%d").sql.gz
set +e

psql -U $POSTGRES_USER -h $POSTGRES_HOST -d $POSTGRES_DB < psql_dump_$(date "+%Y-%m-%d").sql > /dev/null 2>&1


unset PGPASSWORD
