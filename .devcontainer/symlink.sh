#!/bin/bash
for DIR in 'agents' 'checkman' 'web' 'checks' 'doc' 'inventory' 'notifications' 'pnp-templates'; do
    rm -rfv $OMD_ROOT/local/share/check_mk/$DIR
    ln -sv $WORKSPACE/src/$DIR $OMD_ROOT/local/share/check_mk/$DIR
done;
#rm -rfv $OMD_ROOT/local/lib/check_mk/base/plugins/agent_based
#ln -sv $WORKSPACE/src/agent_based $OMD_ROOT/local/lib/check_mk/base/plugins/agent_based
rm -rfv $OMD_ROOT/local/lib/python3/cmk/base/plugins/agent_based
ln -sv $WORKSPACE/src/agent_based $OMD_ROOT/local/lib/python3/cmk/base/plugins/agent_based

mkdir -p $OMD_ROOT/local/lib/python3/cmk/base/cee/plugins
ln -sv $WORKSPACE/src/bakery $OMD_ROOT/local/lib/python3/cmk/base/cee/plugins/bakery

htpasswd -b $OMD_ROOT/etc/htpasswd cmkadmin cmkadmin
chmod +x $OMD_ROOT/local/share/check_mk/agents/special/*