<?php

$code = file_get_contents('showflageveryphp.php');
$code = file_get_contents('nodieshell.php');
$code = file_get_contents('s1.php');
$code = file_get_contents('s2.php');
$code = file_get_contents('s3.php');
$code = file_get_contents('s4.php');
// echo $code;
echo base64_encode($code);