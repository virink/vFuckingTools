<?php

//  898589723
//  
//  
//  348875787
//  461155728
//  662215242
//  184131677
//  
//  
//  348875787xxxxxxxxx461155728xxxxxxxxx
//  
//  662215242xxxxxxxxx184131677xxxxxxxxx
//  
echo "\n";

// $seed = 184131677;
// srand($seed);

function rand_str($len=9)
{
    $rand = [];
    $_str = "0123456789";
    for($i = 0; $i < $len; $i++) {
        $n = rand(0, strlen($_str) - 1);
        $rand[] = $_str{$n};
    }
    return implode($rand);
} 
$now = rand_str();
// $next = rand_str();
echo "\n";
echo $now;
// echo "\n";
// echo $next;

$ss = '662215242xxxxxxxxx184131677xxxxxxxxx';


?>