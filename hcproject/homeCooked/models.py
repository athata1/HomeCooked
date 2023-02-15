from django.db import models

# Create your models here.

class Post(postid, producerID, recipeID):
    postid = 0
    producerID = 0
    recipeID = 0
    available = True
    consumerid = 0
    created = ""
    compleated = ""

    def __init__(self, postid, producerid, recipeid, timeStamp, available=True, consumerid=0, compleated=""):
        self.postid = postid
        self.producerid = producerid
        self.recipeid = recipeid
        self.created = timeStamp
        self.available = available
        self.consumerid = consumerid
        self.compleated = compleated