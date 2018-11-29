#!/bin/bash
#/share/place.txt /share/photo/n01.txt china-photo-chain

if [ $# -lt 2 ]; then
    echo "Invalid number of parameters!"
    echo "Usage: ./job_chain_driver.sh [q1 data] [output_location]"
    exit 1
fi


hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-D stream.num.map.output.key.fields=1 \
-D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
-D mapred.text.key.comparator.options=-nr \
-mapper tag_mapper.py \
-reducer tag_reducer.py \
-file tag_mapper.py \
-file tag_reducer.py \
-input $1 \
-output $2




