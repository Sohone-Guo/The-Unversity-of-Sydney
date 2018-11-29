#!/bin/bash
#/share/place.txt /share/photo/n01.txt china-photo-chain

if [ $# -lt 3 ]; then
    echo "Invalid number of parameters!"
    echo "Usage: ./job_chain_driver.sh [place_file_location] [input_location] [output_location]"
    exit 1
fi

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-D stream.num.map.output.key.fields=2 \
-D map.output.key.field.separator=# \
-D mapreduce.partition.keypartitioner.options=-k1,1 \
-D mapreduce.job.name='Q1_1' \
-file Q1_join_mapper_1.py \
-mapper Q1_join_mapper_1.py \
-file Q1_join_reducer_1.py \
-reducer Q1_join_reducer_1.py \
-input $1 \
-input $2 \
-output ""$3"tmpFile" \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner



hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-mapper tag_mapper.py \
-combiner combiner.py \
-reducer tag_reducer.py \
-file tag_mapper.py \
-file tag_reducer.py \
-file combiner.py \
-input ""$3"tmpFile" \
-output $3


hdfs dfs -rm -r -f ""$3"tmpFile*"

