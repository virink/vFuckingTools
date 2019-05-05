#!/bin/bash
ftp -n <<- EOF
open 211.71.232.55
user anonymous 123
cd log
bin
get s.txt
bye
EOF