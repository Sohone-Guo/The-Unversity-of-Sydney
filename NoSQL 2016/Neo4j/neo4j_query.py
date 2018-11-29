from py2neo import Graph


graph = Graph(password = 'neo4jneo4j')

print('Simple query:')
print('1: Given a user id, find all artists the user\'s friends listen.')
print('2: Given an artist name, find the most recent 10 recent 10 tags that have been assigned to it.')
print('3: Given an artist name, find the top 10 users based on their respective listening counts of this artist. Display both the user id and the listening count.')
print('4: Given a user id, find the most recent 10 artists the user has assigned tag to.')
print('Complex queries')
print('5: Find the top 5 artists ranked by the number of users listening to it')
print('6: Given an artist name. find the top 20 tags assigned to it. The tags are ranked by the number of times it has been assigned to this artist')
print('7: Given a user id, find the top 5 artists listened by his friends but not him. We rank artists by the sum of friends listening counts of the artist.')
print('8: Given an artist name, find the top 5 similar artists. Here similarity between a pair of artists is defined by the number of unique users that have listened both. The higher the number, the more similar the two artists are.')
question = int(input('Which Question: '))

# Simple query 1
if question == 1:
    friend_artist_matrix = []
    user_ID = str(input('Input your user ID: '))
    # find user's friends
    friend_raw = graph.data('match (:user{userID:{id}}) - [:friend]->(n) return (n.userID)',id=user_ID)
    for user_ID_length in range(len(friend_raw)):
        # find artists listened by user's friends
        friend_artist = graph.data('match (:user{userID:{f_id}}) - [:weight] ->(n) return n.name, n.url, n.pictureURL',f_id = friend_raw[user_ID_length]['(n.userID)'] )
        print(friend_artist)
     
# Simple query 2
elif question == 2:
    artist_name = input('Input artist name: ')
    print(graph.data('match (:user) - [n:tags] ->(:artist{name:{name}}) return n.tagValue,n.time order by n.time desc limit 10',name = artist_name ))

# Simple query 3
elif question == 3:
    weightnumber_dic = {}
    artist_name = input('Input artist name: ')
    # find listening counts of users
    weightnumber = graph.data('match (u:user) - [n:weight] ->(:artist{name:{name}}) return u.userID,n.weightnumber order by n.weightnumber desc ',name=artist_name)
    for i in range(len(weightnumber)):
        weightnumber_dic['useID:%s'%weightnumber[i]['u.userID']]=int(weightnumber[i]['n.weightnumber'])
    # print top 10 users
    for i in range(10):
        print(sorted(weightnumber_dic, key=weightnumber_dic.__getitem__ ,reverse = True)[i],weightnumber_dic[sorted(weightnumber_dic, key=weightnumber_dic.__getitem__ ,reverse = True)[i]])

# Simple query 4
elif question == 4:
    user_ID = str(input('Input your user ID: '))
    print(graph.data('match (u:user{userID:{id}}) - [n:tags] ->(a:artist) with n,a order by n.time desc return distinct a.name limit 10',id=user_ID))

# Complex query 1
elif question == 5 :
    print(graph.data('match (u:user) - [n:weight] ->(a:artist) return a.name,count(n) order by count(n) desc limit 5'))

# Complex query 2
elif question == 6:
    artist_name = input('Input artist name: ')
    print(graph.data('match (p:user) - [n:tags] ->(:artist{name:{name}}) return n.tagValue, count(n) order by count(n) desc  limit 20',name=artist_name))

# Complex query 3
elif question == 7:
    friend_matrix = []
    self_artist_matrix =[]
    user_ID = str(input('Input your user ID: '))
    # find user's friends
    friend_raw = graph.data('match (:user{userID:{id}}) - [:friend]->(n) return (n.userID)', id=user_ID)
    for i in range(len(friend_raw)):
        friend_matrix.append(friend_raw[i]['(n.userID)'])
    # find artists listened by user
    self_artist = graph.data('match (:user{userID:{id}}) - [:weight]->(n) return (n.name)', id=user_ID)
    for j in range(len(self_artist)):
        self_artist_matrix.append(self_artist[j]['(n.name)'])
    # find artists listened by user's friends and listening counts
    artist = graph.data('match (u:user) - [n:weight] ->(a:artist) where u.userID IN {matrix} return a.name,sum(toInt(n.weightnumber)) order by sum(toInt(n.weightnumber)) desc limit 10',matrix = friend_matrix)
    count = 0
    # exclude artists listened by user
    for k in range(len(artist)):
        if artist[k]['a.name'] not in self_artist_matrix and count < 5:
            print(artist[k])
            count +=1

# Complex query 4
elif question == 8:
    user_ID_matrix =[]
    artist_name = input('Input artist name: ')
    # find users who listen to this artist
    user_ID = graph.data('match (p:user) - [n:weight] ->(:artist{name:{name}}) return p.userID',name=artist_name)
    for i in range(len(user_ID)):
        user_ID_matrix.append(user_ID[i]['p.userID'])
    # find top 6 similar artists
    artist = graph.data('match (p:user) - [n:weight] ->(a:artist) where p.userID IN {matrix} return a.name, count(n) order by count(n) desc limit 6',matrix = user_ID_matrix)
    # exclude this artist
    print(artist[1:])


