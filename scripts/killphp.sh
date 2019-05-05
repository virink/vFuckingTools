#!/bin/sh
while 1
do
    # 重启php-fpm
    killall -9 php-fpm || ps -ef | grep php | grep -v 'grep' | awk '{print $2}' | xargs -n1 kill
    sleep 10s
done