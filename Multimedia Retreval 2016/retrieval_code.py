import os
import urllib
import re
import csv
from sklearn import svm
import cv2
from sklearn.neighbors import KNeighborsRegressor

#Initial the list
data_x=[]
data_y=[]
probi_result=[]
data_result=[]
# clf = svm.SVC(gamma=0.001,C=100)
neigh = KNeighborsRegressor(n_neighbors=2)
#Read Date for SVM
def trainning():
    global data_x
    global data_y
    with open('data_x.csv', 'r') as p:
        data_x = [list(map(int, rec)) for rec in csv.reader(p, delimiter=',')]
    with open('data_y.csv', 'r') as p:
        data_y = [list(map(int, rec)) for rec in csv.reader(p, delimiter=',')]
    neigh.fit(data_x, data_y)

#Read the Image and mark the image
def readImage(file_name):
    print(file_name)
    data = []
    img1 = cv2.imread('personal\\%s' % file_name)
    try:
        histr01 = cv2.calcHist([img1], [0], None, [256], [0, 256])
        for i in range(len(histr01)):
            data.append(histr01[i][0])

        histr02 = cv2.calcHist([img1], [1], None, [256], [0, 256])
        for j in range(len(histr01)):
            data.append(histr02[j][0])

        histr03= cv2.calcHist([img1], [2], None, [256], [0, 256])
        for k in range(len(histr01)):
            data.append(histr03[k][0])
    except cv2.error as e:
        # print('e')
        data=[]
    return data


def webCraw():
    global data

    # First step: read the gps site
    site = open("position.txt", "r").read().split('\n')

    for i in range(len(site)): # Read the website and find the personal id in each place

        data_result=[]
        lat, lng= site[i].split(',')
        # Create data

        url = "https://api.instagram.com/v1/media/search?\
        max_timestamp=&min_timestamp=&distance=10000&lat=%s&lng=%s\
        &access_token=3176778431.b59fbe4.7a3b21cc00a24377a30341f6f9aa40e9\
        &callback=jQuery18307052452579672583_1463412863546&_=1463412864385" %(lat,lng)
        try:
            tp = urllib.urlopen(url)
            html = tp.read()
            personal_ID = re.findall('"id": "(.*?)", "full_name', html)

            probi_result.append([site[i]])
            # Second find the image
            tavaling_num=0
            non_travaling_num=0

            for id in personal_ID:# Using the personal ID find the picture in personal

                if id.find(',') == -1 and id.find('_') ==-1:
                    # print('ID:',id)


                    # print('personal_ID.index(id):',personal_ID.index(id))
                    url = "https://api.instagram.com/v1/users/%s/media/recent?\
                    max_timestamp=&min_timestamp=&access_token=3176778431.b59fbe4.7a3b21cc00a24377a30341f6f9aa40e9\
                    &callback=jQuery183019499685873576866_1463412914034&_=1463412915278" %id

                    personal_Information = "https://api.instagram.com/v1/users/%s?client_id=b59fbe4563944b6c88cced13495c0f49&callback=jQuery18308307411822024733_1463722060957&_=1463722061379"%id

                    try:
                        data_result.append(['%s'%id])

                        handle = urllib.urlopen(url)

                        html = handle.read()

                        image_name = re.findall('standard_resolution": {"url": "(.*?)", "width', html)

                        person_Image_num = 0
                        for image in image_name:
                            # print(image)
                            try:
                                urllib.urlretrieve(image, 'personal\\%d.jpg' % person_Image_num)
                                person_Image_num += 1
                            except IOError as e:
                                print(e)

                        index_num = len(data_result)-1
                        print(index_num)
                        data_result[index_num].append(person_Image_num)

                        likes_num = re.findall('likes": {"count": (.*?), "data', html)
                        comments_num = re.findall('comments": {"count": (.*?), "data', html)
                        total_like_num = 0
                        total_count_num = 0
                        for likes in range(len(likes_num)):
                            total_like_num += int(likes_num[likes])
                        data_result[index_num].append(total_like_num)

                        for comment in range(len(comments_num)):
                            total_count_num += int(comments_num[comment])
                        data_result[index_num].append(total_count_num)

                        #Mark the image
                        if person_Image_num > 0:
                            count=0
                            like_num_travel = 0
                            comments_num_travel = 0
                            for image_num in range(person_Image_num):
                                data = readImage('%s.jpg'%image_num)
                                if data != []:
                                    # print('PREDICT: ',int(neigh.predict(data)[0]))
                                    if int(neigh.predict(data)[0]) == 1:
                                        count += 1
                                        # print('image_num',image_num)
                                        # img = cv2.imread('personal\\%s.jpg'%image_num, 1)
                                        # cv2.imshow('Traveling', img)
                                        # cv2.waitKey(2000)
                                        # cv2.destroyAllWindows()
                                        try:
                                            like_num_travel += int(likes_num[image_num])
                                            comments_num_travel += int(comments_num[image_num])
                                        except IndexError as e:
                                            like_num_travel += 0
                                            comments_num_travel += 0
                                    # else:
                                    #     try:
                                    #         print('image_num', image_num)
                                    #         img = cv2.imread('personal\\%s.jpg' %image_num, 0)
                                    #         cv2.imshow('Not Traveling', img)
                                    #         cv2.waitKey(300)
                                    #         cv2.destroyAllWindows()
                                    #     except cv2.error as c:
                                    #         print(c)

                            data_result[index_num].append('%s' %count)
                            Probility_Predict = float(count) / person_Image_num

                            data_result[index_num].append('%s'%like_num_travel)
                            data_result[index_num].append('%s'%comments_num_travel)

                            # print(Probility_Predict)
                            if Probility_Predict > 0.01:
                                # print('%s like traveling.'%id,)
                                tavaling_num+=1
                            else:
                                # print('%s do not like traveling.' %id,)
                                non_travaling_num+=1



                            # Delete the image
                            # for delete_num in range(person_Image_num):
                            #     os.remove('personal\\%d.jpg' % delete_num)
                    except IOError as e:
                        print(e)

                    try:
                        follower_Url = urllib.urlopen(personal_Information)

                        follower_Url_html = follower_Url.read()
                        # print(follower_Url_html)

                        follower_follows = re.findall('follows": (.*?)}, "id', follower_Url_html)
                        follower_followby = re.findall('followed_by": (.*?), "follows', follower_Url_html)
                        data_result[index_num].append(follower_follows)
                        data_result[index_num].append(follower_followby)

                    except IOError as e:
                        print(e)
                print(data_result)

            savefile(site[i],data_result)
            probi_result[i].append(tavaling_num)
            probi_result[i].append(non_travaling_num)
            print(tavaling_num,non_travaling_num)
            print("probi_result:",probi_result)

        except IOError as e:
            print(e)

def savefile(name,site):
    myfile = open('site_document\\%s.csv'%name, 'wb')
    wr = csv.writer(myfile, dialect=("excel"))
    for i in range(len(site)):
        wr.writerow(site[i])
    myfile.close()

trainning()
webCraw()

