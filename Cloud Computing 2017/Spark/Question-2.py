'''
spark-submit --num-executors 3 q2.py 
'''

from pyspark import SparkContext
import numpy as np
import math

def measure_filter(record): # Selected the valid measurement
    data = record.strip().split(',')
    sample,FSC,SSC = data[0],data[1],data[2]
    if FSC != 'FSC-A': # If this is a tilte
        if int(FSC) >=0 and int(FSC)<=150000 and int(SSC)>=0 and int(SSC)<=150000:
            return True
        else:
            return False
    else:
        return False

def extract_measurement_function(record): # data ---> (sample,(Ly6C,CD11b,SCA1))
    data = record.strip().split(',')
    sample,Ly6C,CD11b,SCA1 = data[0],data[11],data[7],data[6]
    return (sample,(Ly6C,CD11b,SCA1))
    
def cluster_function(record): # Calculate the argmin distant
    center = broad_cluster_center.value
    data = [float(record[1][0]),float(record[1][1]),float(record[1][2])]
    value = []
    for i in center:
        value.append((i[0]-data[0])**2+(i[1]-data[1])**2+(i[2]*data[2])**2)
    
    cluster_number = value.index(min(value))
    return (cluster_number,(float(record[1][0]),float(record[1][1]),float(record[1][2])))

def map_result(record):
    center = broad_cluster_center.value
    data = [float(record[1][0]),float(record[1][1]),float(record[1][2])]
    value = []
    for i in center:
        value.append((i[0]-data[0])**2+(i[1]-data[1])**2+(i[2]*data[2])**2)
    
    cluster_number = value.index(min(value))
    return (cluster_number+1,1)

if __name__ == "__main__":
    sc = SparkContext(appName="Question 2 for assignment 2")
    ''' Read Data '''
    measurements = sc.textFile("/share/cytometry/large")
    after_filter_measurement = measurements.filter(measure_filter).map(extract_measurement_function) # with valid data ---> (sample,(Ly6C,CD11b,SCA1))

    ''' Initial the cluster center '''
    number_of_cluster = 5
    initial_cluster = np.random.rand(number_of_cluster,3) # Random generate the center
    broad_cluster_center = sc.broadcast(initial_cluster) # As broadcast
    
    ''' Cluster Learning '''
    learning_time = 10
    for num in range(learning_time): #Learning numbers
        cluster_ini = after_filter_measurement.map(cluster_function)
        new_cluster_center = cluster_ini.groupByKey().map(lambda x : (x[0], np.sum((np.asarray(list(x[1]))),axis=0)/len(np.asarray(list(x[1])))))
        data = new_cluster_center.collect()
        data_list_tp = []
        for i in range(number_of_cluster):
            for j in data:
                if j[0] == i:
                    data_list_tp.append(j[1])
        broad_cluster_center = sc.broadcast(data_list_tp)

    ''' Finished Learning '''
    new_cluster_center_result = after_filter_measurement.map(map_result).repartition(1).reduceByKey(lambda before,after: int(before)+int(after)) # Give the data a cluster number
    number_of_cluster = new_cluster_center_result.map(lambda x : (x[0],x[1],np.asarray(broad_cluster_center.value)[x[0]-1])).sortBy(lambda record: int(record[0]))
    result = number_of_cluster.map(lambda record: str(record[0])+'\t'+str(record[1])+'\t'+str(record[2][0])+'\t'+str(record[2][1])+'\t'+str(record[2][2]))
    result.repartition(1).saveAsTextFile("pyspark/q2")
