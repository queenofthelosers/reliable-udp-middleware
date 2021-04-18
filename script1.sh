#!/bin/bash
var=$(pwd)
echo $var
export PYTHONPATH="${PYTHONPATH}:C:\Users\Deepak George\Desktop\Projects\reliable-udp-middleware\rudp"
 cd client
 python client.py 200.gif
 wait