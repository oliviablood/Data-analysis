import pymongo
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client['assignment2']

movies = db.movies
with open("movies.dat",encoding="utf-8") as file:
    for line in file:
        line =line.strip("\n")
        word =line.split("::")

        movieID = int(word[0])
        movieTitle = word[1].lower()
        genre = word[2].lower().split("|")

        movie ={"MovieID":movieID,
                "Title":movieTitle,
                "Genres":genre
            }
        # insert a document
        movies.insert_one(movie)

print("movies.dat loading finished")

tags = db.tags
with open("tags.dat",encoding="utf-8") as file:
    for line in file:
        line =line.strip("\n")
        word =line.split("::")

        userID = int(word[0])
        movieID = int (word[1])
        tag = word[2].lower()
        timestamp=word[3]

        tag ={"UserID": userID,
                "MovieID":movieID,
                "Tag": tag,
                "Timestamp": timestamp
            }
        # insert a document
        tags.insert_one(tag)
        
print("tags.dat loading finished")

ratings = db.ratings
with open("ratings.dat",encoding="utf-8") as file:
    for line in file:
        line =line.strip("\n")
        word =line.split("::")

        userID= int(word[0])
        movieID= int(word[1])
        rating= float(word[2])
        timestamp= word[3]

        rating ={"UserID": userID,
                "MovieID":movieID,
                "Rating": rating,
                "Timestamp": timestamp
            }
        # insert a document
        ratings.insert_one(rating)

print("ratings.dat loading finished")

