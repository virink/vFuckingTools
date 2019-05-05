#!/bin/sh
SUBFIX="php"  #需要转换的目标文件后缀
if [ -z $1 ];then
    cd $PWD
else
    if [ -d $1 ];then
        cd $1
    else
        echo " $1 is not exist;"
        exit 1
    fi
fi

for i in $SUBFIX;
do
    files=`find . -name "*.$i"`
    for f in $files;
    do
        # type=`file $f|awk -F':' '{print $2}' |awk  '{print $4}'` #获取文件类型
        result=$(file $f | grep "UTF-8")
        echo $result
        # echo $f
        if [[ "$result" != "" ]]; then
        # if [ $type != "UTF-8" ];then
            cp $f "$f_bak"
            iconv -f GB2312 -t UTF-8 $f  #使用  iconv函数进行转换 
        fi
    done
done