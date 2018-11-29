'''Import library'''
from pandas.io.json import json_normalize
import plotly
# plotly.tools.set_credentials_file(username='sohone', api_key='upwu3D8WNIogVrReA12o')
plotly.tools.set_credentials_file(username='XuhongGuo', api_key='EAOxsP5iRxJHrkFPb69W')
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as df
import math
import os


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

'''
Read data and clean data
'''
#read json to data frame
text = df.read_json(data_original+'Mitt Romney.json')
# text = df.read_json(data_original+'Australia.json')

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

#extract sha1 name with timestamp > 1 as x using new data
grouped = text.groupby(['sha1']).count().reset_index()
x = grouped[grouped['timestamp']>1]['sha1'].tolist()

#Extract sha1 and timestamp range with min and max for each sha1 which timestamp more than 1
grouped_list = text[text['sha1'].isin(x)].groupby(['sha1']).aggregate(lambda x: sorted(list(x))).reset_index()
sha_timestamp = grouped_list[['sha1','timestamp']].sort('timestamp').reset_index()
del sha_timestamp['index']
time_x = sha_timestamp['timestamp'].tolist()

#extract catagory accounding time range
finished_sha1 = []
catagory_range_time = []
for j in range(len(time_x)):
    match = time_x[j]
    if time_x[j] not in finished_sha1:
        for i in time_x:
            if match[1] < min(i) or match[0]>max(i):
                pass
            else:
                match = [min(match[0],min(i)),max(match[1],max(i))]
                finished_sha1.append(i)
        catagory_range_time.append(match)

new_text = text[text['sha1'].isin(x)].groupby('sha1').apply(lambda x: x.to_dict(orient='records')).reset_index()

#merge data
new_text = df.merge(new_text, sha_timestamp, left_on = 'sha1', right_on = 'sha1')
new_text['group'] = None
new_text['group_range'] = None

for i in range(len(catagory_range_time)):
    for num in range(len(new_text)):
        if new_text['timestamp'][num][0] >= catagory_range_time[i][0] and new_text['timestamp'][num][1] <= catagory_range_time[i][1]:
            new_text['group'][num] = i
            new_text['group_range'][num] = catagory_range_time[i]

new_text['user_number'] = None

for item_num in range(len(new_text['timestamp'])):
#     print(new_text['timestamp'][item_num])
    a = text[text['timestamp'].between(min(new_text['timestamp'][item_num]), max(new_text['timestamp'][item_num]), inclusive=True)].sort('timestamp')
    new_text['user_number'][item_num] = len(a)

result_data = new_text.groupby(['group']).apply(lambda x: x.to_dict(orient='records'))

date = [i[0]['group_range'][0] for i in result_data]
size = []
cicle_size = []

for i in result_data:
    num = 0
    for j in i:
        num += len(j[0])
    size.append(num)
    days = (i[0]['group_range'][1]-i[0]['group_range'][0]).days
    cicle_size.append(days)        

# result_data[62]
trace0 = go.Scatter(
    x=date,
#     y=size,
    y = size,
    mode='markers',
    marker=dict(
        size = [i/4 for i in cicle_size],
        color = ['rgba(152, 0, 0, .8)' if i>max(size)/2 else 'rgba(152, 152, 0, .8)'  for i in size],
        colorscale = 'Viridis'
#         showscale =True
    )
)

layout = go.Layout(
    yaxis = dict(
        type = 'log'
    )

)

data = [trace0]
fig = go.Figure(data=data,layout = layout)
py.plot(fig)


group_nums = []
yyy = sorted(cicle_size)
for number in yyy[-5:]:
    group_nums.append(cicle_size.index(number))

for group_num in group_nums:
    drawing = []
    for k in range(len(result_data[group_num])):
        x_1 = result_data[group_num][k]['timestamp']
        y_1 = result_data[group_num][k]['timestamp'][0]
        
        trace2 = go.Scatter(
            x = x_1,
            y = [y_1 for i in range(len(x_1))],
            mode = 'lines',
            name = 'Revered %s'%str(k)
        )
        
        drawing.append(trace2)

    py.plot(drawing, filename='scatter-mode')
