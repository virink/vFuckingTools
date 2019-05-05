#!/bin/bash
if [ -z $1 ];then
    echo './bak.sh webroot'
else
    echo "WWWROOT : $1"
    tar -zcvf /tmp/webbak_`basename $1`_`date|md5 -q`.tar.gz $1
    echo "Backup : /tmp/webbak_`basename $1`_`date|md5 -q`.tar.gz"
fi
