#!/bin/bash

NAME=$(python3 -c 'print(eval(open("src/package").read())["name"])')
rm /omd/sites/cmk/var/check_mk/packages/* ||:
ln -s $WORKSPACE/src/package /omd/sites/cmk/var/check_mk/packages/$NAME

mkp -v pack $NAME
