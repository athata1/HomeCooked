from django.db import models

# Create your models here.

class Post(postid, producerID, recipeID):
    postid = 0
    producerid = 0
    recipeid = 0
    available = True
    consumerid = 0
    created = ""
    compleated = ""

    def __init__(self, cur, producerid, recipeid, timeStamp, available=True, consumerid=0, compleated=""):
        self.postid = cur.execute("SELECT ROW_NUMBER() FROM Posts WHERE created=%s AND producerid=%d", timeStamp, producerid).fetchone()
        self.producerid = producerid
        self.recipeid = recipeid
        self.created = timeStamp
        self.available = available
        self.consumerid = consumerid
        self.compleated = compleated
    
    def toJson():
        return json.loads({
            "postid":postid,
            "producerid":producerid,
            "recipeid":recipeid,
            "available":available,
            "created":created,
            "compleated":compleated,
            "status":1,
        })