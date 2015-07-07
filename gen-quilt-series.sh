#!/bin/bash
# Autogeneries the quilt `series` from the patch order in the spec file.
# We don't use `quilt setup` because it makes a huge mess and doesn't work.
rm -f series.new
count=0
# Filter out the patches, and use `_` as our pseudo-IFS to prevent expansion.
for i in `grep '%patch' glibc.spec | sed -e 's,%patch,,g' -e 's, ,_,g'`; do
    # Split the patch into number and arguments.
    # 1 - Patch number.
    # 2-N - Patch arguments.
    # Get back our elements by undoing pseudo-IFS change.
    elements=(`echo $i | sed -e 's,_, ,g'`)
    num=${elements[0]}
    args=${elements[@]:1}
    grep "Patch${num}" glibc.spec | sed -e 's,Patch.*: ,,g' -e "s,\$, ${args[@]},g" >> series.new
    ((count++))
done
fcount=`wc -l series.new | sed -e 's, .*$,,g'`
if [ $fcount -ne $count ]; then
    echo "Error! Processed less patches than in spec file ($fcount != $count)."
    exit 1
fi
echo "Processed $count patches."
mv series.new series
echo "Generated quilt ./series file, please commit."
exit 0
