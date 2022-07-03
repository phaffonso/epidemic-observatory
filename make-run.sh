#!/bin/bash
#make-run.sh
#make sure a process is always running.
#SET UP with cron

export DISPLAY=:0 #needed if you are running a simple gui app.

process=YourProcessName
makerun="python3 /dev/epidemic-observatory/collect_data.py"

if ps ax | grep -v grep | grep $process > /dev/null
then
    exit
else
    $makerun &
fi

exit
