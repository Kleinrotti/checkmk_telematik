#!/bin/bash

for DIR in 'agents' 'checkman' 'web' 'checks'; do
    rm -rfv $OMD_ROOT/local/share/check_mk/$DIR
    ln -sv $WORKSPACE/src/$DIR $OMD_ROOT/local/share/check_mk/$DIR
done;

rm -rfv $OMD_ROOT/local/lib/check_mk/base/plugins/agent_based
ln -sv $WORKSPACE/src/agent_based $OMD_ROOT/local/lib/check_mk/base/plugins/agent_based

htpasswd -b $OMD_ROOT/etc/htpasswd cmkadmin cmkadmin