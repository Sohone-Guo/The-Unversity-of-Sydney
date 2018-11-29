from pymongo import MongoClient
from bson.son import SON
import pymongo
client = MongoClient('localhost',27017)
db = client.assignment
friend = db.friend
weight = db.weight
tag = db.tag
#
# for tagValue in artists.find({'name': 'Diary of Dreams'}).sort("weight", -1).limit(10).distinct('userID'):
#     print(tagValue)

print('Simple query:')
print('1: Given a user id, find all artists the user\'s friends listen.')
print('2: Given an artist name, find the most recent 10 recent 10 tags that have been assigned to it.')
print('3: Given an artist name, find the top 10 users based on their respective listening counts of this artist. Display both the user id and the listening count.')
print('4: Given a user id, find the most recent 10 artists the user has assigned tag to.')
print('Complex query')
print('5: Find the top 5 artists ranked by the number of users listening to it')
print('6: Given an artist name. find the top 20 tags assigned to it. The tags are ranked by the number of times it has been assigned to this artist.')
print('7: Given a user id, find the top 5 artists listened by his friends but not him. We rank artists by the sum of friends listening counts of the artist.')
print('8: Given an artist name, find the top 5 similar artists. Here similarity between a pair of artists is defined by the number of unique users that have listened both. The higher the number, the more similar the two artists are.')
question = int(input('Which Question: '))


# Simple query 1
if question == 1:
    friend_artist = []
    userID = int(input('   Input the userID: '))
    # find user's friend
    for doc in friend.find({'userID':userID}): 
        # find artists listened by user's friends
        for artist in weight.find({'userID': doc['friendID']},{'id':1,'name':1,'url':1,'pictureURL':1}):
            print(artist)

# Simple query 2
elif question == 2:
    tagValue_matrix = []
    artist_name = input('   Input the artist name: ')
    for tagValue in tag.find({'name': artist_name}, {'tagValue': 1}).sort("timestamp", -1).limit(10):
        tagValue_matrix.append(tagValue['tagValue'])
    print('   The most recent 10 recent 10 tags that have been assigned to it:')
    print('  ',tagValue_matrix)

# Simple query 3
elif question == 3:
    artist_name = input('   Input the artist name: ')
    for user_ID in weight.find({'name': artist_name},{'userID':1,'weight':1}).sort("weight", -1).limit(10):
        print(user_ID)

# Simple query 4
elif question == 4:
    n = 0
    k=''
    userID = int(input('   Input the userID: '))
    for artist_name in tag.find({'userID':userID},{'name':1,'userID':1,'tagValue':1,'timestamp':1}).sort('timestamp',-1):
        if n<=10 and k != artist_name['name']:
            print('    name: ', artist_name['name'], ' time: ', artist_name['timestamp'])
            n += 1
            k = artist_name['name']

# Complex query 1
elif question == 5:
    for artist_name in weight.aggregate([{"$group":{'_id':'$name',"count":{'$sum':1}}},{'$sort':{'count':-1}},{'$limit':5}]):
        print(artist_name)

# Complex query 2
elif question == 6:
    artist_name = input('   Input the artist name: ')
    for tag_Value in tag.aggregate([{'$match':{'name':artist_name}},{'$group':{'_id':'$tagValue','count':{'$sum':1}}},{'$sort':{'count':-1}},{'$limit':20}]):
        print('  ',tag_Value)

# Complex query 3
elif question == 7:
    friend_ID_matrix = []
    self_artist_matrix = []
    name_matrix = {}
    userID = int(input('   Input the userID: '))
    # find user's friends
    for friend_ID in friend.find({'userID': userID}):
        friend_ID_matrix.append(friend_ID['friendID'])
    # find artists listened by user
    for self_artist in weight.find({'userID':userID}):
        self_artist_matrix.append(self_artist['name'])
    count =0
    # find artists listened by user's friends
    for user_weight in weight.aggregate([{'$match':{'userID':{'$in':friend_ID_matrix}}},{'$group':{'_id':'$name','weight':{'$sum':'$weight'}}},{'$sort':{'weight':-1}},{'$limit':10}]):
        # exclude artists listened by user from artists listened by user's friends        
        if user_weight['_id'] not in self_artist_matrix and count<5:
            print(user_weight)
            count += 1

# Complex query 4
elif question == 8:
    user_ID_matrix = []
    artist_rank = {}
    artist_name = input('   Input the artist name: ')
    # find users who listen to this artist    
    for artistsname in weight.aggregate([{'$match':{'name':artist_name}},{'$group':{'_id':'$name','user':{'$push':'$userID'}}}]):
        user_ID_matrix = artistsname['user']
    k = 0
    # find top 6 similar artists
    for artistsname_all in weight.aggregate([{'$match':{'userID':{'$in':user_ID_matrix}}},{'$group':{'_id':'$name','count':{'$sum':1}}},{'$sort':{'count':-1}},{'$limit':6}]):
        # exclude this artist
        if k != 0:
            print(artistsname_all)
        k+=1
else:
    print('It is nothing ')