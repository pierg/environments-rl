#!/usr/bin/env bash

# Pull latest changes in the repositories
echo "...updating repositories..."
pwd
git git reset --hard HEAD
git clean -f
git pull
pwd

if [ $# -eq 0 ]
  then
    source launch_script.sh
else
    source launch_script.sh "$@"
fi

