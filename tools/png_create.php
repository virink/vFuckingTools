<?php

$im = imagecreate(50, 20) or die("Cannot Initialize new GD image stream");
imagecolorallocate($im, 255, 255, 255);
$text_color = imagecolorallocate($im, 233, 14, 91);
imagestring($im, 1, 5, 5,  "Virink", $text_color);
imagepng($im);
imagedestroy($im);

?>