#!/bin/bash

for i in {10..90..10}
do
   sudo tc qdisc add dev lo root netem loss $i%
   wait
   export currI=$i
   wait
   parallel -u ::: './script2.sh' './script1.sh' 
   wait
   sudo tc qdisc del dev lo root netem loss $i%
   wait
done
