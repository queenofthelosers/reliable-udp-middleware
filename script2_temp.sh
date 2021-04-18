#!/bin/bash
var=$(pwd)
echo $var
 cd server
 python server.py 200.gif
 wait