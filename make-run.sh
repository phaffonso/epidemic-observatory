#!/bin/bash
#make-run.sh
#make sure a process is always running.
#SET UP with cron

#export DISPLAY=:0 #needed if you are running a simple gui app.

process=python3
makerun="/usr/bin/python3 ${HOME}/dev/epidemic-observatory/collect_data.py"

if pgrep $process > /dev/null
then
    printf "Process '%s' is running.\n" "$process"
    exit
else
    printf "Starting process '%s' with command '%s'.\n" "$process" "$makerun"
    $makerun &
fi

exit
