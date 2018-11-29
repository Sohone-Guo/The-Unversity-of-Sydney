#!/bin/bash
#/share/place.txt /share/photo/n01.txt china-photo-chain

if [ $# -lt 3 ]; then
    echo "Invalid number of parameters!"
    echo "Usage: ./job_chain_driver.sh [place_file_location] [input_location] [output_location]"
    exit 1
fi



hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-D stream.num.map.output.key.fields=2 \
-D mapreduce.job.maps=7 \
-D mapreduce.job.reduces=6 \
-D map.output.key.field.separator=# \
-D mapreduce.partition.keypartitioner.options=-k1,1 \
-D mapreduce.job.name='Q3_1' \
-file map_1.py \
-mapper map_1.py \
-file reducer_1.py \
-reducer reducer_1.py \
-input $1 \
-input $2 \
-output ""$3"tmpFile_1" \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner



hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-D mapreduce.job.maps=7 \
-D mapreduce.job.reduces=6 \
-mapper map_2.py \
-reducer reducer_2.py \
-file map_2.py \
-file reducer_2.py \
-input ""$3"tmpFile_1" \
-output ""$3"tmpFile_2"





hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-D stream.num.map.output.key.fields=2 \
-D mapreduce.job.maps=7 \
-D mapreduce.job.reduces=1 \
-D map.output.key.field.separator=# \
-D mapreduce.partition.keypartitioner.options=-k1,1 \
-D mapreduce.job.name='Q3_1' \
-file map_3.py \
-mapper map_3.py \
-file reducer_3.py \
-reducer reducer_3.py \
-input ""$3"tmpFile_2" \
-input q2 \
-output ""$3"tmpFile_3" \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner



hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar \
-D stream.num.map.output.key.fields=1 \
-D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
-D mapred.text.key.comparator.options=-nr \
-mapper map_4.py \
-reducer reducer_4.py \
-file map_4.py \
-file reducer_4.py \
-input ""$3"tmpFile_3" \
-output $3


hdfs dfs -rm -r -f ""$3"tmpFile_1"
hdfs dfs -rm -r -f ""$3"tmpFile_2"
hdfs dfs -rm -r -f ""$3"tmpFile_3"
# rm -r part-00000

