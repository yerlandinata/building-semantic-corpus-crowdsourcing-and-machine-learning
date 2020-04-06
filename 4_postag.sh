#!/bin/bash

WORKER=$1
IDS=$WORKER
let "IDS--"

for i in $(seq 0 $IDS);
do 
    setsid python tagger.py $WORKER $i > logs/tagger$i.log 2>&1 < /dev/null & 
done

