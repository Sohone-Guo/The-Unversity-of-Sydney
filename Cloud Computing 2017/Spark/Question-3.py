'''
spark-submit --num-executors 3 q3.py 
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

def measurement_function(record):
    cluster,number_of_cluster, Ly6C, CD11b, SCA1 = record.strip().split('\t')
    return (float(cluster),(float(number_of_cluster), float(Ly6C), float(CD11b), float(SCA1)))


def group_map_function(record):
    number_ = broad_number_of_data_each_cluster.value
    total = []
    cluster_number = record[0]
    data = sorted(list(record[1]), key=lambda tup: tup[-1])
    number_of_cluster = int(number_[cluster_number]*0.9)
    for i in data[:number_of_cluster]:
        total.append(i[:-1])
    return total


def cluster_function_1(record):
    record = record[1]
    center = broad_cluster_center.value
    data = [float(record[0]),float(record[1]),float(record[2])]
    value = []
    for i in center:
        value.append(((i[0]-data[0])**2+(i[1]-data[1])**2+(i[2]*data[2])**2)**0.5)
    
    cluster_number = value.index(min(value))
    dis = min(value)
    return (cluster_number,(float(record[0]),float(record[1]),float(record[2]),dis))

def cluster_function(record):
    center = broad_cluster_center.value
    data = [float(record[0]),float(record[1]),float(record[2])]
    value = []
    for i in center:
        value.append(((i[0]-data[0])**2+(i[1]-data[1])**2+(i[2]*data[2])**2)**0.5)
    
    cluster_number = value.index(min(value))
    return (cluster_number,(float(record[0]),float(record[1]),float(record[2])))

def map_result(record): # Map function of result
    center = broad_cluster_center.value
    data = [float(record[0]),float(record[1]),float(record[2])]
    value = []
    for i in center:
        value.append(((i[0]-data[0])**2+(i[1]-data[1])**2+(i[2]*data[2])**2)**0.5)
    
    cluster_number = value.index(min(value))
    return (cluster_number+1,1)

if __name__ == "__main__":
    sc = SparkContext(appName="Question 3 for assignment 2")
    '''Read Data'''
    
    measurements_ = sc.textFile("/share/cytometry/large").filter(measure_filter).map(extract_measurement_function)

    ''' Read the inital data which q2 used'''
    q2_center = np.asarray(sc.textFile("pyspark/q2").map(lambda x: x.strip().split('\t')).collect()).astype('float')
    initial_center = q2_center[:,-3:]
    number_of_data_each_cluster = q2_center[:,1]
    ''' Read the inital data which q2 used'''
    broad_cluster_center = sc.broadcast(initial_center)
    broad_number_of_data_each_cluster = sc.broadcast(number_of_data_each_cluster)
    '''Generate the new data which 90%'''
    new_data_9_percent = measurements_.map(cluster_function_1).groupByKey().flatMap(group_map_function)
    '''Cluster Learning '''
    number_of_cluster = 5
    initial_cluster = np.random.rand(number_of_cluster,3) # Random generate the center
    # initial_cluster = initial_center
    broad_cluster_center = sc.broadcast(initial_cluster)
    learning_time = 10
    for num in range(learning_time):
        cluster_ini = new_data_9_percent.map(cluster_function)
        new_cluster_center =  cluster_ini.groupByKey().map(lambda x : (x[0], np.sum((np.asarray(list(x[1]))),axis=0)/len(np.asarray(list(x[1])))))
        data = new_cluster_center.collect()
        data_list_tp = []
        for i in range(number_of_cluster):
            for j in data:
                if j[0] == i:
                    data_list_tp.append(j[1])
        broad_cluster_center = sc.broadcast(data_list_tp)

    ''' Finished Learning'''
    number_of_cluster = new_data_9_percent.map(map_result).repartition(1).reduceByKey(lambda before,after: int(before)+int(after)).map(lambda x : (x[0],x[1],np.asarray(broad_cluster_center.value)[x[0]-1])).sortBy(lambda record: int(record[0]))
    result = number_of_cluster.map(lambda record: str(record[0])+'\t'+str(record[1])+'\t'+str(record[2][0])+'\t'+str(record[2][1])+'\t'+str(record[2][2]))
    result.repartition(1).saveAsTextFile("pyspark/q3")

