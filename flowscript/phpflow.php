<?php

error_reporting(0);

define("DS", DIRECTORY_SEPARATOR);


class PhpFlowLog
{
    public function __construct($table='test')
    {
        // $this->checkips = array('127.0.0.1');
        $this->flowdata = array();
        // Redirect
        $this->redirect = false;
        // Mysql
        $this->dbhost = '127.0.0.1';
        $this->dbport = '32768';
        $this->dbuser = 'root';
        $this->dbpass = 'root';
        $this->dbname = 'flowlog';
        $this->table = "phpflow_".$table;
        $this->db = $this->initdb();
        // files
        // $this->logfiles = $_SERVER['DOCUMENT_ROOT'].DS.'logfiles/';
        $this->logfiles = "/tmp/logfiles/";
        if(!file_exists($this->logfiles)){
            mkdir($this->logfiles,0777,true);
        }
        // Run
        $this->Flow();
    }

    public function initdb(){
        $db = mysql_connect($this->dbhost.":".$this->dbport, $this->dbuser, $this->dbpass);
        mysql_select_db($this->dbname, $db) or die(mysql_error());
        // if not $table then create
        $sql = <<<EOF
create table if NOT EXISTS %s
(
    id int not null auto_increment primary key,
    keyword varchar(128) null,
    method varchar(8) null,
    host varchar(128) null,
    useragent varchar(255) null,
    referer varchar(255) null,
    uri varchar(255) null,
    protocol varchar(20) null,
    rip varchar(15) null,
    cip varchar(255) null,
    xff varchar(255) null,
    time datetime null,
    ctype varchar(56) null,
    filedata text null,
    post text null,
    constraint %s_id_uindex unique (id)
);
EOF;
        $sql = sprintf($sql,$this->table,$this->table);
        mysql_query($sql) or die(mysql_error());
        return $db;
    }

    public function Flow()
    {
        /* Method */
        $this->flowdata['method'] = $_SERVER['REQUEST_METHOD'];
        /* Header */
        $arr = array(
            'HTTP_HOST',
            'HTTP_REFERER',
            'HTTP_USER_AGENT'
            // wtf
            // 'HTTP_ACCEPT',
            // 'HTTP_ACCEPT_LANGUAGE',
            // 'HTTP_ACCEPT_ENCODING',
            // 'HTTP_CONNECTION'
        );
        foreach($arr as $key){
            $this->flowdata['header'][ucwords(strtolower(str_replace("HTTP_", "", $key)))] = $_SERVER[$key];
        }
        /* Url */
        $this->flowdata['uri'] = $_SERVER['REQUEST_URI'];
        /* Protocol */
        $this->flowdata['protocol'] = $_SERVER['SERVER_PROTOCOL'];
        /* IP */
        $this->flowdata['ip'] = array(
            'REMOTE_ADDR'=>$_SERVER['REMOTE_ADDR'],
            'CLIENT_IP'=>$_SERVER['HTTP_CLIENT_IP'],
            'X_FORWARDED_FOR'=>$_SERVER['HTTP_X_FORWARDED_FOR']
        );
        /* Time */
        $this->flowdata['time'] = date('Y-m-d H:i:s',$_SERVER['REQUEST_TIME']);
        /* CONTENT_TYPE */
        $this->flowdata['ctype'] = $_SERVER['CONTENT_TYPE'];
        /* GetData ??? */
        /* PostData */
        if(isset($_POST) or strtolower($this->flowdata['Method']) == 'post' ){
            if($this->flowdata['ctype'] == 'application/x-www-form-urlencoded'){
                $this->flowdata['post'] = json_encode($_POST);
            }else{
                $this->flowdata['post'] = file_get_contents('php://input');
            }
        }
        /* File */
        if(isset($_FILES)){
            foreach ($_FILES as $key => $fileobj){
                $bn = $this->logfiles.md5(time()).'_'.basename($fileobj['file_name']);
                $this->this->flowdata['filedata'][$key]['name'] = $bn;
                $filedata = file_get_contents($fileobj['tmp_name']);
                if($fileobj['file_size'] < 1024 ){
                    $this->this->flowdata['filedata'][$key]['data'] = $filedata;
                }else{
                    file_put_contents($bn, $filedata);
                    $this->Scan($filedata);
                }
            }
        }
        // test
        // $this->Send("test");
        foreach ($this->flowdata as $key => $value) {
            $this->Scan($value);
        }
        //  => fuck  Location  最好的那个队伍
        if($this->redirect){
            header("Location: http://".$this->redirect.$_SERVER['REQUEST_URI']);
            exit('this is waf.....');
        }
    }

    public function RandStr(){
        return md5(time());
    }

    public function Scan($input){
        $pattern = "select|insert|update|delete|and|union|load_file|outfile|dumpfile|sub|hex"; // sql inject
        $pattern .= "|file_put_contents|fwrite|eval|assert|file:\/\/";
        $pattern .="|passthru|exec|system|chroot|scandir|chgrp|chown|shell_exec|proc_open|proc_get_status|popen|ini_alter|ini_restore";
        $pattern .="|`|dl|openlog|syslog|readlink|symlink|popepassthru|stream_socket_server|pcntl_exec";
        if (preg_match_all( "/$pattern/i", $input, $matches)){
            // $this->Send(print_r($matches,true));
            $this->Send(json_encode($matches[0]));
            exit(json_encode($matches[0]));
            // WAF
            // foreach ($this->checkips as $key => $value) {
            //     if(strpos(json_encode($this->flowdata['ip']), $value) === false){
            //         header("Location: /index.php");
            //     }
            // }
        }
    }

    public function Send($keyword)
    {
        // header('Content-Type: application/json');
        // echo json_encode($this->flowdata);
        $data = $this->flowdata;
        file_put_contents($this->logfiles.date("d-h").".log","\r\n".$keyword."\r\n".print_r($data,true)."\r\n=====================================\r\n",FILE_APPEND);
        $sql = "insert {$this->table} (id, keyword, rip, cip, xff, time, method, uri, protocol, host, referer, useragent, ctype, post, filedata) ";
        $sql .= "value (null, '{$keyword}','{$data['ip']['REMOTE_ADDR']}','{$data['ip']['CLIENT_IP']}','{$data['ip']['X_FORWARDED_FOR']}','{$data['time']}','{$data['method']}','{$data['uri']}','{$data['protocol']}','{$data['header']['Host']}','{$data['header']['Referer']}','{$data['header']['User_agent']}','{$data['ctype']}','{$data['post']}','{$data['filedata']}');";
        mysql_query($sql, $this->db);
        return 0;
    }

    public function __destruct(){
        mysql_close($this->db);
    }
}

new PhpFlowLog('fuck2');

?>
