#!/bin/bash
var=$(pwd)
echo $var

 cd client
 python client.py Loss_% $currI
 wait