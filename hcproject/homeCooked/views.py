from django.http import HttpResponse
import datetime


def index(request):
    return HttpResponse("Hello, world!")

def getPostsByUser(userid):
    # SELECT postid FROM Posts WHERE producerid=userid;
    return [];

def createPost(postid, producerid, recipeid):
    timeStamp = datetime.datetime.now();
    # verify valid ids (producer and recipe exist and post doesn't)

    # INSERT INTO Posts (postid, producerid, recipeid, available, created)
    # VALUES (postid, producerid, recipeid, True, timeStamp);

    """
    CREATE TABLE Posts(
        postid Number(8),
        producerid Number(16),
        recipeid Number(8),
        consumerid Number(8),
        available Bool(1)
        created date,
        compleated date
    );
    """
def getTransactionsByUser(userid):
    # SELECT postid FROM posts WHERE consumerid=userid OR producerid=userid;
    return

def completeTransaction(postid, consumerid):
    timeStamp = datetime.datetime.now();
    # UPDATE Posts SET consumerid=userid, available=False, compleated=timeStamp WHERE postid=postid;