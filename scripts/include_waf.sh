function includewaf(){
    local pa=$1
    local ig=$2
    local fi=$3
    find $pa -path $ig -prune -o -type f -name '*.php'|xargs sed -i "1i<?php require_once('$fi');?>"
}