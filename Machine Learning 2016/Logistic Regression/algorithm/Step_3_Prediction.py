import pandas as pd  # Read Data
import numpy as np  # Deal data
import math  # Log function
import numpy  # Deal data
import os # If file existed
import time

'''Named the folder address'''
current_address = os.getcwd()
parent_address = os.path.dirname(current_address)
output_address = parent_address+'\\output\\'
input_address = parent_address+'\\input\\'


'''Setting the files address'''
data_address = input_address+'training_data.csv'  # The address of the original data
label_address = input_address+'training_labels.csv'  # The address of the original data
read_data_address = input_address+'new_data.csv'  # The address of merged data



W = pd.read_csv('W_0.csv',header=None).values # Read files W and label values
label = pd.read_csv('label_0.csv',header=None).values.flatten()

test_data = pd.read_csv(input_address+'test_data.csv',header=None) # Read the test_data

def Logistic(x): # Logistic function
    return 1. / (1 + numpy.exp(-x))

def predict(x): # Prediction function
    tp = []
    for i in range(len(W)):
        y_ = Logistic(x.dot(W[i]))
        tp.append(y_)
    predict_num = tp.index(max(tp))
    return(predict_num)

test_data['predict_label'] = None # add a column name to test data/test_data


data = test_data.values
for i in range(len(test_data)): # Add the result to dataframe
    test_data['predict_label'][i] = label[predict(data[i,1:-1])]

test_data.to_csv(output_address+'predicted_labels.csv',header=False,index=False) # Save the result
print('Prediction finished.')