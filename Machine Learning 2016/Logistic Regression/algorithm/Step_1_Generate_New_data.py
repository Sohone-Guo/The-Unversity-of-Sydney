import pandas as pd  # Read Data
import numpy as np  # Deal data
import math  # Log function
import numpy  # Deal data
import os # If file existed

'''Check if the folder exited or make the folder'''
current_address = os.getcwd()
parent_address = os.path.dirname(current_address)
output_address = parent_address+'\\output\\'
input_address = parent_address+'\\input\\'

if not os.path.exists(output_address):
    os.makedirs(output_address) # Create the output folder
if not os.path.exists(input_address):
    os.makedirs(input_address) # Create the input folder

'''Setting the files address'''
data_address = input_address+'training_data.csv'  # The address of the original data
label_address = input_address+'training_labels.csv'  # The address of the original data
read_data_address = input_address+'new_data.csv'  # The address of merged data

'''Check if the original data exited '''
if os.path.isfile(data_address):
    pass
else:
    print('The training_data.csv did not exited at %s. ' % data_address)
    exit()

''' Check if the new data generated or it will generate the data'''
if os.path.isfile(read_data_address):
    print('Found the new_data exited on %s, Then you can use it for training model' % read_data_address)
    # label = pd.read_csv(label_address, header=None)
else:
    print('Do not found the new_data exited on %s, Will generate the new_data.csv' % read_data_address)
    data = pd.read_csv(data_address, header=None)  # Read training data to'data' and training 'labels'
    label = pd.read_csv(label_address, header=None)
    new_data = pd.merge(data, label, left_on=0, right_on=0)  # Merge data and labels to 'new_data'
    data = None  # Released 'data'
    del new_data[0]  # Delete the first column of data which is the name of article
    new_data.to_csv(read_data_address, header=False, index=False)  # Save it to 'new_data'
    new_data = None  # Released the new_data
    print('Finished the data generation, it will break for save the memory, please go the next file again.')
    exit()