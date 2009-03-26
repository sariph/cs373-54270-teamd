#!/bin/sh


# check for an optional command line variable
if [ $# -le 0 ]; then
	echo >&2 "No command line args, running svnversion from current directory"
	dir="./"
elif [ $1 = "-h" -o $1 = "--help" -o $# -gt 1 ]; then
	/bin/echo -e "Usage: $0 [path]\n\tOutputs a running diff of a subversion checkout directory.\n\tpath is optional, defaulting to the current directory\n\tPlease note that the path must be a directory from which 'svn log' returns useful text."
else
	dir=$1
	echo >&2 "Running svnversion on this path: $dir"
fi

# get the current version
latestVersion=`svnversion $dir | grep -oE "[0-9]+" | tail -1`

# check whether the version we got is sane
if [ -z $latestVersion ]; then
	echo >&2 "Error: svnversion does not return a number.  Are you in the correct directory?"
	exit
elif [ $latestVersion -eq 1 ]; then
	echo >&2 "Error: svnversion returns $latestVersion.  There aren't going to be any changes.  Maybe you forgot to commit some files?"
	exit
fi

# output the information
/bin/echo -e "Current version = $latestVersion\n"

i=2
while [ $i -le "$latestVersion" ]
do
	echo "***************************"
	echo "* Changes in revision $i "
	/bin/echo -e "***************************\n"
	svn log -r $i $dir
	echo ""
	svn diff -c$i $dir --diff-cmd /usr/bin/diff -x "-Bw --suppress-common-lines"
	echo ""
	i=$(($i+1))
done
