#! /usr/bin/bash

curr_dir=`pwd`
mubiao_server="${curr_dir}/server.py"
py="/root/python/Python-3.7.6/python"
#echo $mubiao_server
#echo $py
#echo "$py $mubiao_server"

$py $mubiao_server &

