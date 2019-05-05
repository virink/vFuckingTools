<?php
    error_reporting(0);
    class WafLog
    {
        public function __construct($filepath)
        {
            $this->filepath = $filepath;
            $this->header = array();
        }

        public function Flow()
        {
            $arr = array('HTTP_HOST','HTTP_USER_AGENT','HTTP_ACCEPT','HTTP_ACCEPT_LANGUAGE','HTTP_ACCEPT_ENCODING','HTTP_REFERER','HTTP_COOKIE','HTTP_X_FORWARDED_FOR','HTTP_CONNECTION');
            $HTTP_Method = $_SERVER['REQUEST_METHOD'];
            $server = $_SERVER;
            $Allfilepath = $this->filepath.'/'.date('Y-m-d-h').".log";
            foreach($arr as $value){
                $this->header[$value] = $server[$value];
            }
            $head = '';
            foreach ($this->header as $key => $value){
                if(stripos($key, 'HTTP_') == -1){
                    $key = ucwords(strtolower($key));
                }else{
                    $key = ucwords(strtolower(substr($key, 5)));
                }
                $head.= $key.': '.$value."\r\n";
            }
            $request_url = $_SERVER['REQUEST_URI'];
            $protocol = $_SERVER['SERVER_PROTOCOL'];
            $post = file_get_contents('php://input');
            $ip = $_SERVER['REMOTE_ADDR'];
            $time = date('Y/m/d h:i:s');
            $content = $ip."\t".$time."\t\n".$HTTP_Method.' '.$request_url.' '.$protocol."\r\n".$head."\n\n".$post."\n\n";
            $this->WriteFile($Allfilepath,$content,FILE_APPEND);
        }

        public function WriteFile($filepath,$content,$FILE_APPEND=FILE_APPEND)
        {
            file_put_contents($filepath,$content,$FILE_APPEND);
        }
    }

    $Catchs = new WafLog('/tmp/');
    $Catchs->Flow();
?>