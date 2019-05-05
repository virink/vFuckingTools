#!/bin/bash
for file in $(find . -name '*.php');do
    sed -i "2c
    require_once('/usr/share/nginx/html/WordPress/phpwaf.php');" $file;
done
