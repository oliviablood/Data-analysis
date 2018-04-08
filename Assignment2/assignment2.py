import pymongo
from bson.code import Code
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
import pprint
from pprint import pprint

# connect to MongoDB, change the <<MONGODB URL>> to reflect your own connection string
# client=MongoClient('mongodb://localhost:27017/')
client = MongoClient('localhost',27017)

# getting a database
db = client['assignment2']
# getting a collection
movies = db.movies
tags = db.tags
ratings = db.ratings

#question 1) What genre is the movie CopyCat in?

for movie in movies.find({'Title': {'$regex':'CopyCat'.lower()}}):
    print(movie)

print("Finished!")

#2)what genre has the most movies?

mapper = Code("""
              function(){
                  this.Genres.forEach(function(genre){
                      emit(genre,1);
                  });
               }
               """)

reducer = Code("""
               function( key, values) {
                   var total = 0;
                   for (var i=0; i<values.length; i++) {
                       total += values[i];
                   }
                   return total;
                }
                """)
genres = db.movies.map_reduce(mapper, reducer,"myresults")

for genre in genres.find({}).sort("value",-1).limit(1):
    print (genre)

print("Finished!")
'''
for genre in genres.aggregate([{"$group":{"_id":"null","max_num_genre":{"$max":"$value"}}}])
'''

#3)what tags did user 146 use to describe the movie "2001: A Space Odyssey”

findMovie = movies.find({'Title':{'$regex':'^2001: a space odyssey'}})
print(findMovie)
for movie in findMovie:
    movieID = movie['MovieID']    

findUser = tags.find({'UserID': 146,'movieID': int(movieID)})
for user in findUser:
    print(user['Tag'])

print("finished!")

#4)What are the top 5 movies with the highest avg rating?  


'''
find the top 5 movies' information with the highest avg rating
'''
res = ratings.aggregate([
    {"$group":
     {"_id":"$MovieID",
      "ratingAve":{"$avg":"$Rating"}
      }
     },
    {"$sort":{"ratingAve":-1}},
    {"$limit":5}
    ])

'''
find the top 5 movies' movieID and movieName
'''
movieIDs = []
movieNames = []

for item in res:
    id = item["_id"]
    movieIDs.append(id)
    
    name=movies.find_one({"MovieID":id})["Title"]
    movieNames.append(name)

print(movieIDs)
print(movieNames)
print("Finished!")
    

#5) Write 3 different queries of your choice to demonstrate that your data storage is working.

'''
get all tags user 20 used to decribe movies
'''
userTags=[]
user20 = tags.find({"UserID":20})
for user in user20:
    tag = user['Tag']
    userTags.append(tag)

print(userTags)
print("Finished!")
        
'''
find 5 movies with largest number of ratings
'''
res = ratings.aggregate([
    {"$group":
        {"_id":"$MovieID",
        "rating_num": {"$sum":1}
        }
    },
        {"$sort":{"rating_num":-1}},
        {"$limit":5}
 ])
movieIDs =[]
movieNames = []
for group in res:
    id = group["_id"]
    movieIDs.append(id)
    name = movies.find_one({"MovieID": id})["Title"]
    movieNames.append(name)
print(movieIDs)
print(movieNames)
print("Finished!")

'''
find all the movies with rating over than 3 rated by user 2
'''

res = ratings.find({
    "Rating": {"$gte":3, "$lte":5},
    "UserID": 2
})
movieIDs =[]
movieNames = []
for parts in res:
    id = parts["MovieID"]
    movieIDs.append(id)

    name = movies.find_one({"MovieID": id})["Title"]
    movieNames.append(name)

print(movieIDs)
print(movieNames)


    
