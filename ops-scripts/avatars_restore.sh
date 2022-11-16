#!/bin/bash

###########################
###  Restore avatars    ###
###########################

DUMP_PATH=
AVATARS_PATH=

cd $DUMP_PATH && tar -xzvf avatars_dump_$(date "+%Y-%m-%d").tar.gz \
&& cp -R noted_avatars $AVATARS_PATH \
&& echo "Deleting folder.." \
&& rm -R noted_avatars
