''' Import Library '''
from pandas.io.json import json_normalize
import pandas as df
import math
from pandas.tslib import Timestamp
import numpy
import os
import numpy as np
import urllib.request
import re

'''Check if the folder exited or make the folder'''
current_address = os.getcwd()
parent_address = os.path.dirname(current_address)
output_address = parent_address + '\\output\\'
input_address = parent_address + '\\input\\'
cluster_data_address = output_address + 'Revert_cluster_data\\'
chain_data_address = output_address + 'Revert_chain_data\\'

if not os.path.exists(output_address):
    os.makedirs(output_address)  # Create the output folder
if not os.path.exists(input_address):
    os.makedirs(input_address)  # Create the input folder
if not os.path.exists(cluster_data_address):
    os.makedirs(cluster_data_address)  # Create the output folder
if not os.path.exists(chain_data_address):
    os.makedirs(chain_data_address)  # Create the input folder

'''Set the original data address'''
data_original = input_address + 'fa\\'
clear_data = input_address + 'clearn\\'

'''Check the list of file which have already been generated'''
file_list_cluster = [data_original + '.'.join(f.split('.')[:-1]) + '.json' for f in os.listdir(cluster_data_address)]
file_list_chain = [data_original + '.'.join(f.split('.')[:-1]) + '.json' for f in os.listdir(chain_data_address)]
if len(file_list_cluster) >= len(file_list_chain):
    exited_file_list = file_list_chain
else:
    exited_file_list = file_list_cluster
print('The data have already generated: ' + '\n'.join(exited_file_list))

'''Collection the label of those articles'''
response = urllib.request.urlopen('https://en.wikipedia.org/wiki/Wikipedia:Featured_articles').read()
it = re.findall('<h2><span class="mw-headline" (id=".*?)</span></h2>',str(response)) # Use the regresion
category = [i.split('>')[1].split('<')[0] for i in it]
print('The label here is:\n'+'\n'.join(category))

print('Begin to generate the data:\n')
file_name = [data_original+f for f in os.listdir(data_original)]
# json = list(set(file_name)-set(exit_file_list))
json = file_name
json_group_num = []
json_sha1_num = []
total_new_data = []

for json_name in json:
    error_list = []
    try:
        '''
        Read data and clean data
        '''
        #read json to data frame
        text = df.read_json(json_name)
        name_word = '.'.join(json_name.split('\\')[-1].split('.')[:-1])

        #read bot and admin name to list
        bot_name = [' '.join(i.split()[1:-1]) if len(i.split())>3 else i.split()[1] for i in open(clear_data+'bots_list.txt').read().split('\n')]
        admin_name = [i for i in open(clear_data+'administrators_list.txt').read().split('\n')]

        # print(text[text['timestamp'].between('2011-06-07 16:51:34', '2011-06-11 15:01:31', inclusive=True)].sort('timestamp')['user'].tolist())

        #Clearn data which user is bot or admin
        text_clean_bot = text[~text['user'].isin(bot_name)]
        text_clean_admin_bot = text_clean_bot[~text_clean_bot['user'].isin(admin_name)].reset_index()
        del text_clean_admin_bot['index']
        text = text_clean_admin_bot 

        # print(text[text['timestamp'].between('2011-06-07 16:51:34', '2011-06-11 15:01:31', inclusive=True)].sort('timestamp')['user'].tolist())

        # Clearn data which 'size' colum is 0
        without_size_0 = text[~text['size'].isin([0])].reset_index()
        del without_size_0['index']
        text = without_size_0


        # Clearn data which is edit by same person: A-A-A, A-B-B,
        grouped = text.groupby(['sha1']).aggregate(lambda x: list(x)).reset_index()

        need_deleted_num = []
        total_number = 0
        for i in range(len(grouped['timestamp'])):
            if len(grouped['timestamp'][i]) > 1:
                or_name = text[text['sha1'].isin([grouped['sha1'][i]])].index.tolist()
                or_data = text[text['timestamp'].between(min(grouped['timestamp'][i]), max(grouped['timestamp'][i]), inclusive=True)].sort('timestamp')

                user = or_data['user'].tolist()
                index = or_data.index.tolist()

                if len(list(set(user[1:]))) == 1:
                    total_number += len(user)
                    [need_deleted_num.append(i) for i in index]

        clean_same_person = text[~text.index.isin(need_deleted_num)].reset_index()
        del clean_same_person['index']
        text = clean_same_person
        text[:40]

        grouped = text.groupby(['sha1']).count().reset_index()
        x = grouped[grouped['timestamp']>1]['sha1'].tolist()

        grouped_list = text[text['sha1'].isin(x)].groupby(['sha1']).aggregate(lambda x: sorted(list(x))).reset_index()
        sha_timestamp = grouped_list[['sha1','timestamp']].sort('timestamp').reset_index()
        del sha_timestamp['index']
        time_x = sha_timestamp['timestamp'].tolist()
        sha_timestamp

        #extract catagory accounding time range
        finished_sha1 = []
        category_range_time = []
        for j in range(len(time_x)):
            match = time_x[j]
            if time_x[j] not in finished_sha1:
                for i in time_x:
                    if match[1] < min(i) or match[0]>max(i):
                        pass
                    else:
                        match = [min(match[0],min(i)),max(match[1],max(i))]
                        finished_sha1.append(i)
                category_range_time.append(match)
        category_range_time[:2]


        new_text = text[text['sha1'].isin(x)].groupby('sha1').apply(lambda x: x.to_dict(orient='records')).reset_index()
        new_text[:2]

        #merge data
        new_text = df.merge(new_text, sha_timestamp, left_on = 'sha1', right_on = 'sha1')
        new_text['group'] = None
        new_text['group_range'] = None
        new_text[:1]

        for i in range(len(category_range_time)):
            for num in range(len(new_text)):
                if new_text['timestamp'][num][0] >= category_range_time[i][0] and new_text['timestamp'][num][1] <= category_range_time[i][1]:
                    new_text['group'][num] = i
                    new_text['group_range'][num] = category_range_time[i]
        new_text

        new_text['user_number'] = None
        new_text[:3]

        for item_num in range(len(new_text['timestamp'])):
        #     print(new_text['timestamp'][item_num])
            a = text[text['timestamp'].between(min(new_text['timestamp'][item_num]), max(new_text['timestamp'][item_num]), inclusive=True)].sort('timestamp')
            new_text['user_number'][item_num] = len(a)

        #average time 
        new_text['users_average_time'] = None
        new_text[:3]

        for item_num in range(len(new_text['timestamp'])):
        #     print(new_text['timestamp'][item_num])
            a = text[text['timestamp'].between(min(new_text['timestamp'][item_num]), max(new_text['timestamp'][item_num]), inclusive=True)].sort('timestamp')
            new_text['users_average_time'][item_num] = numpy.mean(numpy.diff(a['timestamp'].tolist()))

        new_text['title'] = name_word
#         print(json_name)

        #statistic gourp number, sha1 number of each article
    #     print(len(new_text.groupby['group'].count().index))
        json_group_num.append(len(new_text.groupby('group').count().index))
        json_sha1_num.append(len(new_text.groupby('sha1').count().index))

        
#         Add label
        new_text['Category'] = None
        for k in range(len(category)-1):
            item = re.findall('>%s(.*?)%s<'%(category[k],category[k+1]),str(response))
#             print(json_name.split('/')[1].split('.')[0])
            if item[1].find('>%s<'%name_word) >=0:
#                 print(catagory[k])
                new_text['Category'] = category[k]
                break
    

    #     Revert chain data
    #     time
        new_text['start_time'] = None
        new_text['end_time'] = None
        new_text['duration'] = None
        new_text['longest_revert_interval'] = None
        new_text['shortest_revert_interval'] = None
        new_text['medium_revert_interval'] =None

        new_text['number_of_reverts'] = None
        new_text['number_of_anonymous_reverts']= None
        new_text['number_of_unique_registered_users'] = None
        

        for item_num in range(len(new_text['timestamp'])):
            new_text['start_time'][item_num] = new_text['timestamp'][item_num][0]
            new_text['end_time'][item_num] = new_text['timestamp'][item_num][-1]
            new_text['duration'][item_num] = new_text['timestamp'][item_num][-1]-new_text['timestamp'][item_num][0]
            new_text['longest_revert_interval'][item_num] = numpy.max(numpy.diff(new_text['timestamp'][item_num]))
            new_text['shortest_revert_interval'][item_num] = numpy.min(numpy.diff(new_text['timestamp'][item_num]))
            new_text['medium_revert_interval'][item_num] = numpy.median(numpy.diff(new_text['timestamp'][item_num]))
            new_text['number_of_reverts'][item_num] = len(new_text['timestamp'][item_num])-1
            if 'anon' in text:
                new_text['number_of_anonymous_reverts'][item_num] = len(text[text['sha1'].isin([new_text['sha1'][item_num]]) & text['anon'].isin([''])])
                new_text['number_of_unique_registered_users'][item_num] = len(text[text['sha1'].isin([new_text['sha1'][item_num]]) & text['anon'].isin([np.nan])].groupby(['user']).count()) 
            else:
                new_text['number_of_anonymous_reverts'][item_num] = 0
                new_text['number_of_unique_registered_users'][item_num] = len(text[text['sha1'].isin([new_text['sha1'][item_num]])].groupby(['user']).count()) 
                
        Revert_chain_data = new_text[['title','start_time','end_time','duration','longest_revert_interval','shortest_revert_interval','medium_revert_interval','number_of_reverts','number_of_anonymous_reverts','number_of_unique_registered_users','Category']]
        outputfilename = chain_data_address+name_word+'.csv'
#         print ('Writing ' + outputfilename)
#         with open(outputfilename,'w') as outfile:
#             outfile.write(Revert_chain_data.to_json(date_format='iso', orient = 'records',lines=True))
        Revert_chain_data.to_csv(outputfilename)

        # Revert cluster data
        # Revert cluster data
        tptp = new_text[['title','start_time','end_time','duration','longest_revert_interval','shortest_revert_interval','medium_revert_interval','number_of_reverts','number_of_anonymous_reverts','number_of_unique_registered_users','group','group_range','Category']]
        # outputfilename = 'result/'+'tp.json'
        # print ('Writing ' + outputfilename)
        # with open(outputfilename,'a+') as outfile:
        #     outfile.write(tptp.to_json(date_format='iso', orient = 'records',lines=2))
        gourp_time = new_text.groupby(['group']).aggregate(lambda x: sorted(list(x))).reset_index()
        gourp_time
        cluster_data_tp = tptp.groupby(['group']).apply(lambda x: x.to_dict(orient='records')).reset_index()

        num = new_text.groupby('group').count()
        num_tp = num[num['sha1']>1].index.tolist()
        cluster_data = cluster_data_tp[cluster_data_tp.index.isin(num_tp)]

        cluster_data['title'] = name_word
        cluster_data['group_range'] = None
        cluster_data['start_time'] = None
        cluster_data['end_time'] = None
        cluster_data['duration'] = None
        cluster_data['longest_revert_interval'] = None
        cluster_data['shortest_revert_interval'] = None
        cluster_data['medium_revert_interval'] =None
        cluster_data['number_of_chains'] =None
        cluster_data['number_of_reverts'] =None
        cluster_data['number_of_anonymous_reverts'] =None
        cluster_data['number_of_unique_registered_users'] = None
        cluster_data['longest_chain_duration'] = None
        cluster_data['shortest_chain_duration'] = None
        cluster_data['medium_chain_duration'] = None
        cluster_data['most_number_reverted']=None
        cluster_data['medium_number_reverted']=None
        cluster_data['min_number_reverted']=None
        cluster_data['Category'] = None

        for item_num in cluster_data.index.tolist():
            data_read_diction_tp = df.DataFrame.from_dict(cluster_data[0][item_num])

            cluster_data['group_range'][item_num] = data_read_diction_tp['group_range'][0]
            cluster_data['start_time'][item_num] =  data_read_diction_tp['group_range'][0][0]
            cluster_data['end_time'][item_num] =  data_read_diction_tp['group_range'][0][1]
            cluster_data['duration'][item_num] = data_read_diction_tp['group_range'][0][1] - data_read_diction_tp['group_range'][0][0]
            cluster_data['longest_revert_interval'][item_num] = df.DataFrame.max(data_read_diction_tp['longest_revert_interval'])
            cluster_data['shortest_revert_interval'][item_num] = df.DataFrame.min(data_read_diction_tp['shortest_revert_interval'])
            cluster_data['medium_revert_interval'][item_num] = df.DataFrame.median(data_read_diction_tp['medium_revert_interval'])
            cluster_data['number_of_chains'][item_num] = len(data_read_diction_tp)
            cluster_data['number_of_reverts'][item_num] = df.DataFrame.sum(data_read_diction_tp['number_of_reverts'])
            cluster_data['number_of_anonymous_reverts'][item_num] = df.DataFrame.sum(data_read_diction_tp['number_of_anonymous_reverts'])
            cluster_data['number_of_unique_registered_users'][item_num] = df.DataFrame.sum(data_read_diction_tp['number_of_unique_registered_users'])
            cluster_data['longest_chain_duration'][item_num] = df.DataFrame.max(data_read_diction_tp['duration'])
            cluster_data['shortest_chain_duration'][item_num] = df.DataFrame.min(data_read_diction_tp['duration'])
            cluster_data['medium_chain_duration'][item_num] = df.DataFrame.median(data_read_diction_tp['duration'])
            cluster_data['most_number_reverted'][item_num] = df.DataFrame.max(data_read_diction_tp['number_of_reverts'])
            cluster_data['medium_number_reverted'][item_num] = df.DataFrame.median(data_read_diction_tp['number_of_reverts'])
            cluster_data['min_number_reverted'][item_num] = df.DataFrame.min(data_read_diction_tp['number_of_reverts'])
            cluster_data['Category'][item_num] =  data_read_diction_tp['Category'][0]
        cluster_data
        new_cluster_data = cluster_data[['title','group_range','start_time','end_time','duration','longest_revert_interval','shortest_revert_interval','medium_revert_interval','number_of_chains','number_of_reverts','number_of_anonymous_reverts','number_of_unique_registered_users','longest_chain_duration','shortest_chain_duration','medium_chain_duration','most_number_reverted','medium_number_reverted','min_number_reverted','Category']]
        outputfilename = cluster_data_address+name_word+'.csv'
#         print ('Writing ' + outputfilename)
#         with open(outputfilename,'w') as outfile:
#             outfile.write(cluster_data.to_json(date_format='iso', orient = 'records',lines=True))
        new_cluster_data.to_csv(outputfilename)
        print('Finish '+ name_word+',The Whole file have already been finished: '+'%0.2f'%(len(os.listdir(chain_data_address))/len(file_name)))
        
    except Exception as e:
        outputfilename = output_address+'error.txt'
        print ('Writing ' + outputfilename)
        with open(outputfilename,'a+') as outfile:
            outfile.write(json_name+'---reason:'+str(e)+'\n')
        pass


