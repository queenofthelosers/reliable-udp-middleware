#!/bin/bash
var=$(pwd)
echo $var
export PYTHONPATH="${PYTHONPATH}:$var"
 cd client
 python client.py 200.gif
 wait