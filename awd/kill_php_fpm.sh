ps -ed | grep 'php-fpm' | awk '{print $1}' | xargs kill -9


ps -ed | grep 'sshd' | awk '{print $1}' | xargs kill -9


