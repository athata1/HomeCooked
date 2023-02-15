from django.db import models

# Create your models here.

class Post(producerID, recipeID):
    producerID = producerID;
    recipeID = recipeID;
    available = True;
    consumerid = 0;
    timestamp = "";

    def __init__(self, producerid, recipeid):
        self.producerid = producerid
        self.recipeid = recipeid

    def update(sefl, consumerid, timestamp):
        self.available = False
        self.consumerid = consumerid
        self.timestamp = timestamp