#!/bin/bash
NAME=$(python3 -c 'print(eval(open("package").read())["name"])')
rm /omd/sites/cmk/var/check_mk/packages/* ||:
rm /omd/sites/cmk/var/check_mk/packages_local/* ||:
ln -s $WORKSPACE/package /omd/sites/cmk/tmp/check_mk/$NAME

mkp -v package /omd/sites/cmk/tmp/check_mk/$NAME
cp /omd/sites/cmk/var/check_mk/packages_local/$NAME*.mkp .
