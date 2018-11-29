import csv

import cv2
data=[]
file_name=[]
def read():
    csvfile = open('image\\index.txt', 'r')
    for line in csvfile:
        file_name.append(list(line.strip().split(',')))
    print(file_name)

def readImage(a,k):
    img1 = cv2.imread('image\\%s' % a)
    histr01 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    for i in range(len(histr01)):
        data[k].append(histr01[i][0])
    histr02 = cv2.calcHist([img1], [1], None, [256], [0, 256])
    for j in range(len(histr02)):
        data[k].append(histr02[j][0])
    histr03 = cv2.calcHist([img1], [2], None, [256], [0, 256])
    for j in range(len(histr03)):
        data[k].append(histr03[j][0])

def savefile():
    myfile = open('new_index.csv', 'wb')
    wr = csv.writer(myfile, dialect=("excel"))
    for i in range(len(data)):
        wr.writerow(data[i])
    myfile.close()

read()
for i in range(len(file_name)):
    data.append([file_name[i][0]])
for k in range(len(file_name)):
    readImage(file_name[k][0],k)
# print (data)
savefile()

