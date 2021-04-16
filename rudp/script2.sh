#!/bin/bash
var=$(pwd)
echo $var
export PYTHONPATH="${PYTHONPATH}:$var"

 cd server
 python server.py loss $currI
 wait