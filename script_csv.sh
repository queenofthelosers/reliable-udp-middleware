#!/bin/bash
var=ms
count=0
while IFS=, read -r col1 col2 col3 col4 col5
do
     echo $col1 $col2 $col3 $col4 $col5 $count

  if [[ $count -eq 0 ]]
then
count=$((count+1))
elif [[ $col4 -eq 0  ]]
then
    tc qdisc add dev lo root netem corrupt $col2% duplicate $col3% loss $col5% delay $col1$var
   wait
   export currI=$count
   wait
   parallel -u ::: './script2.sh' './script1.sh' 
   wait
    tc qdisc del dev lo root netem corrupt $col2% duplicate $col3% loss $col5% delay $col1$var
    wait
    count=$((count+1))
    wait
else
  tc qdisc add dev lo root netem gap $col4 corrupt $col2% duplicate $col3% loss $col5% delay $col1$var reorder 25% 50%
  wait
   export currI=$count
   wait
   parallel -u ::: './script2.sh' './script1.sh' 
   wait
  tc qdisc del dev lo root netem gap $col4 corrupt $col2% duplicate $col3% loss $col5% delay $col1$var reorder 25% 50%
  wait
    count=$((count+1))
    wait
fi

done < values.csv
echo count
