#!/bin/bash

###########################
###     Dump avatars    ###
###########################

DUMP_PATH=
AVATARS_PATH=

cd $AVATARS_PATH && tar -czvf avatars_dump_$(date "+%Y-%m-%d").tar.gz noted_avatars/     \
&& mv avatars_dump_$(date "+%Y-%m-%d").tar.gz $DUMP_PATH
