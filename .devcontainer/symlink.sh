#!/bin/bash
NAME=$(python3 -c 'print(eval(open("package").read())["name"])')
mkdir $OMD_ROOT/local/lib/python3/cmk/plugins/$NAME
ln -s $WORKSPACE/src/* $OMD_ROOT/local/lib/python3/cmk/plugins/$NAME

echo "cmkadmin" | $OMD_ROOT/bin/cmk-passwd -i cmkadmin