#!/bin/sh
# Given a git source repo, generate a tarball from the desired branch, modify
# the spec file and upload it to lookaside cache if the tarball unpacks and
# gets patched cleanly.
#
# Usage:
#
#     1. Invoke the script as follows:
#
#           ./sync-upstream.sh upstream-repo
#
#       where upstream-repo is the path to the synced upstream git repo.
#
#    2. Watch the script run.  If it proceeds to building the package, then
#       everything seems good and you just need to test the build after it
#       is complete.  If it exits before the build (you'll know if you read
#       the output of the script) then manual intervention is required to
#       complete the sync.  This will typically happen when a patch fails
#       to apply on the new sources.
#
# Development branch:
#
# * As long as the branch is "master" the repository is treated as
#   development and synchronization updates are fully automatic.
#
# Stable branches:
#
# * Once you branch to a stable Fedora release adjust branch.
#   e.g. release/2.23/master
#
# * Set branch_name to the name of the relase
#   e.g. 2.23
#
# * The sync script will automatically stop before commit, push, build
#   for production branches, so you have to review the results and then
#   do those steps yourself.
#

set -e

# We want to sync from master by default.  Change this if you want to sync from
# another branch.
branch=master
# Avoid slashes in branch name.
branch_name=master

# We can't do anything without an upstream repo
if [ $# -ne 1 ]; then
	echo "Usage: $0 <path-to-upstream-repo>" 1>&2
	exit 1
fi

upstream=$1

srcdir=$(git --git-dir=$upstream/.git describe $branch)
cursrc=$(sed -ne 's/^%define glibcsrcdir  \(.*\)/\1/p' glibc.spec)

# Upstream has not moved forward since the last sync.
# TODO: Some time in the future, we might want to only sync when upstream has
# advanced more than a certain number of commits, say, 42.
if [ "$cursrc" = "$srcdir" ]; then
	echo "+ Already in sync with upstream."
	exit 0
fi

# Generate and gzip the tarball from the desired branch of the repository.
echo "+ Generating tarball."
git --git-dir="$upstream/.git" archive --prefix="$srcdir/" "$branch" \
	> "$srcdir.tar"
gzip -9 "$srcdir.tar"
echo "+ Created $srcdir.tar.gz"

# Our changelog header
cldate=$(date +'%a %b %d %Y')
clname=$(git config --get user.name)
clemail=$(git config --get user.email | sed 's/@/\\@/')

# Getting our version and release number from the spec file.
nv=$(perl -ne 's/^%define glibcversion (.+)/printf("%s-", $1)/e;' \
	  -e 's/^%define glibcrelease ([0-9]+).*/printf("%d\n", $1 + 1)/e;' \
	  glibc.spec)

# Our changelog entry.
changelog="* $cldate $clname <$clemail> - $nv\n- Auto-sync with upstream $branch.\n"

# Change the glibcsrcdir variable, bump up the release number and add an extra
# entry to the changelog.
echo "+ Updating spec file."
perl -pi \
	-e "s/^(%define glibcsrcdir  ).+/\$1$srcdir/;
	    s/^(%define glibcrelease )(\d+)/print(\$1); print(\$2 + 1);'';/e;
	    s/^(%changelog)$/\$1\n$changelog/" \
	glibc.spec

function prep_failed {
	# fedpkg prep failed.
	if [ $? -ne 0 ]; then
		echo "+ Source prep failed."
		echo "+ Check the output in $tmpfile and fix things before committing."
		false
	fi
}

function build_failed {
	# fedpkg build failed.
	if [ $? -ne 0 ]; then
		echo "+ Building the package failed (or was interrupted)."
		echo "+ Check the koji logs for final status."
		false
	fi
}

echo "+ Testing if fedpkg prep works."
tmpfile=$(mktemp fedpkg-prep.out-XXXX)

trap prep_failed EXIT
fedpkg prep > "$tmpfile" 2>&1
# Remove mess created by fedpkg prep
rm -f "$tmpfile"
rm -rf "$srcdir"
echo "+ Source prep is clean, so we're good to go."
fedpkg new-sources "$srcdir.tar.gz"
if [ $branch == "master" ]; then
	git commit -a -m "Auto-sync with upstream $branch."
	fedpkg push
	trap build_failed EXIT
	fedpkg build
	echo "+ Done!"
else
	echo "+ This is a non-development branch."
	echo "+ Please review the results of the sync."
	echo "+ Once reviewed you need to commit, push, and build."
fi
