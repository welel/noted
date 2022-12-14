#!/bin/bash

### Try ./Avatars backup and ./Avatars restore ###
###         Backup and restore avatars         ###

DUMP_PATH=
AVATARS_PATH=

case $1 in
   backup)

        cd $AVATARS_PATH && tar -czvf avatars_dump_$(date "+%Y-%m-%d").tar.gz noted_avatars/     \
        && mv avatars_dump_$(date "+%Y-%m-%d").tar.gz $DUMP_PATH && echo "Backup done..."
    ;;

   restore)
        cd $DUMP_PATH && tar -xzvf avatars_dump_$(date "+%Y-%m-%d").tar.gz \
        && cp -R noted_avatars $AVATARS_PATH \
        && echo "Deleting folder.." \
        && rm -R noted_avatars && echo "Restore done..."
    ;;

esac
