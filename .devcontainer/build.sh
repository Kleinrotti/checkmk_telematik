#!/bin/bash

NAME=$(python3 -c 'print(eval(open("src/package").read())["name"])')
rm /omd/sites/cmk/var/check_mk/packages/* ||:
ln -s $WORKSPACE/src/package /omd/sites/cmk/var/check_mk/packages/$NAME

mkp -v pack $NAME

# Set Outputs for GitHub Workflow steps
if [ -n "$GITHUB_WORKSPACE" ]; then
    echo "::set-output name=pkgfile::$(ls src/*.mkp)"
    echo "::set-output name=pkgname::${NAME}"
    VERSION=$(python3 -c 'print(eval(open("src/package").read())["version"])')
    echo "::set-output name=pkgversion::$VERSION"
fi