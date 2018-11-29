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

'''Set labels'''
labels = pd.read_csv(label_address, header = None)
row_len = labels.shape[0]
labels = list(set(labels[1]))
print('The data size is: '+str(row_len))

'''Check feature size'''
one_data = pd.read_csv(read_data_address, header = None, nrows = 1)
col_len = one_data.shape[1]
print('The feature size: '+str(col_len))

'''Set functions'''
def logistic_function(x): # Logistic function
    return 1. / (1 + np.exp(-x))

def cost_func(w, x, y): # Cost function
    lg = logistic_function(x.dot(w)) # Transfer to logistic function
    return np.mean(-y * np.log(lg) - (1 - y) * np.log(1 - lg)) # Return the cost function

def predict_label(x): # Prediction
    w_log = [logistic_function(x.dot(w_list[w])) for w in range(len(w_list))] # Calculate each wx value
    label_loc = w_log.index(max(w_log)) # Find the max value and index the max value
    return label_loc # Return it


def evaluation(true_y, predict_y,labels): # Evaluation the model base on precision recall and f-value
    evaluated = {}
    for label in labels: # Evaluation each label,one vs all.
        TP = sum(1 for p,t in zip(predict_y, true_y) if p==label and t==label) # Calculate TP
        TN = sum(1 for p,t in zip(predict_y, true_y) if p!=label and t!=label) # Calculate TN
        FP = sum(1 for p,t in zip(predict_y, true_y) if p==label and t!=label) # Calculate FP
        FN = sum(1 for p,t in zip(predict_y, true_y) if p!=label and t==label) # Calculate FN
        if TP + FN != 0:
            recall = TP / float(TP + FN)
        else:
            recall = 0
        if TP + FP != 0:
            precision = TP / float(TP + FP)
        else:
            precision = 0
        if precision + recall != 0:
            fscore = 2*precision*recall / (precision + recall)
        else:
            fscore = 0
        if len(true_y) != 0:
            accuracy = (TP + TN) / float(len(true_y))
        else:
            accuracy = 0
        evaluated[label] = [accuracy,precision,recall,fscore] # Add all data to dictionary 
    total_evaluated = [] # Create list for calculate the total values

    total_accuracy = 0 
    total_precision = 0
    total_recall = 0
    total_fscore = 0

    total_number = len(labels)
    for item in evaluated: # Calculate total value
        total_accuracy+=evaluated[item][0] # accuracy
        total_precision+=evaluated[item][1] # precision
        total_recall +=evaluated[item][2] # recall
        total_fscore +=evaluated[item][3] # fscore

    return total_accuracy/total_number ,total_precision/total_number ,total_recall/total_number ,total_fscore/total_number # return avage of each value

start_time = time.time()
chunk_size = int(math.ceil(row_len/10)) # Setting the IO size.
converge_change = 0.7 # Setting the step rate

for fold in range(1): # Setting the folder numbers
    fold_num = 0 # if the fold should be test
    w_list = [np.zeros(col_len-1) for lable in labels] # Set the W value list for each label
    accuracy = 0 # Count accuracy each 1000 times
    number_of_training = 0 # Count the training number
    for fold_data in pd.read_csv(read_data_address, header = None, chunksize = chunk_size):
        if fold_num != fold: # if the folder should be test 
            for data in fold_data.index: # Read data index
                number_of_training+=1
                change_cost = 1 # Changed cost
                row_data = fold_data[fold_data.index.isin([data])].values[0] # Read data
                
                true_label = labels.index(row_data[-1]) # the true label
                pred_label = predict_label(row_data[:-1]) # the predicted label

                if true_label == pred_label:  # Count the accuracy numbers
                    accuracy += 1
                while change_cost > converge_change: # if keep learning the data
                    start_cost = cost_func(w_list[pred_label], row_data[:-1], 1) # set the cost value
                    
                    log_true = logistic_function(row_data[:-1].dot(w_list[true_label]))
                    log_pred = logistic_function(row_data[:-1].dot(w_list[pred_label]))
                    
                    w_list[true_label] = w_list[true_label]+converge_change * np.dot(row_data[:-1].T, 1 - log_true) # Update the W
                    w_list[pred_label] = w_list[pred_label]-0.1*converge_change * np.dot(row_data[:-1].T, 1 - log_pred) # update the W
                    end_cost = cost_func(w_list[pred_label], row_data[:-1], 1)
                    change_cost = start_cost - end_cost # count the cost changed
                    
                    pred_label = predict_label(row_data[:-1])

                if number_of_training % 1000 == 0:  # How many time print once
                    print('This data: ', number_of_training, ', the learing accuracy: %0.2f' % (accuracy / 1000), '%')
                    accuracy = 0  # Clear the accuracy number

        else:
            pred_data = fold_data.values
    
        fold_num += 1
    
    ''' Save the label and W '''
    np.savetxt('W_%s.csv' % fold, np.asarray(w_list), delimiter=',')  # Save the b value list
    with open('label_%s.csv' % fold, 'w') as file:  # Save the label list
        for line in labels:
            file.write(line + '\n')


    ''' Evaluation the model '''
    y_true = []
    y_pred = []
    for pred in pred_data:
        true_label = labels.index(pred[-1])
        pred_label = predict_label(pred[:-1]) # Prediction the test data

        y_true.append(labels[true_label])
        y_pred.append(labels[pred_label]) 
        

    accuracy,precision,recall,fscore = evaluation(y_true, y_pred, labels)
    print('total/average: '+',precision: %0.2f,'%precision+',recall: %0.2f,'%recall+',f-score: %0.2f.'%fscore)
    
    # elapsed_time = int((time.time() - start_time)/60)
    # print('To fold %s total cost %s mins. \n' % (fold+1, elapsed_time))
    
    # with open('results/LR_class_report.csv', 'a+') as csv_file:
    #     csv_file.write("Classification Report(Fold %s):\n" % (fold+1)+clas_report+'\n')
    #     csv_file.write("Micro-average: "+str(precision_recall_fscore_support(y_true, y_pred, average='micro'))+'\n')
    #     csv_file.write("Macro-average: "+str(precision_recall_fscore_support(y_true, y_pred, average='macro'))+'\n')
    #     csv_file.write("Accurancy: "+str(accuracy_score(y_true, y_pred))+'\n\n')