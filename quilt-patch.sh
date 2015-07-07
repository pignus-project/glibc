#!/bin/bash
# Patches are in the current directory.
export QUILT_PATCHES=$PWD
# Extract source file name from sources file,
# and assume it's the same name as the directory.
source=`cat sources | sed -e 's,^.*  ,,g'`
tar zxvf $source
srcdir=${source%.tar.gz}
echo "Entering $srcdir"
pushd $srcdir
# Apply all patches.
quilt push -a
popd
