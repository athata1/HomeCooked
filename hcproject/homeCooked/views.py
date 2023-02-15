from django.http import HttpResponse
import datetime
import sqlite3




def index(request):
    return HttpResponse("Hello, world!")

def getPostsByUser(cur, userid):
    return cur.execute("SELECT ROW_NUMBER() FROM Posts WHERE producerid=userid;").fetchmany();

def createPost(cur, postid, producerid, recipeid):
    timeStamp = datetime.datetime.now();

    # verify valid ids (producer and recipe exist and post doesn't)

    cur.execute("INSERT INTO Posts (producerid, recipeid, available, created) VALUES (producerid, recipeid, True, timeStamp);")

    """
    CREATE TABLE Posts(
        producerid Number(16),
        recipeid Number(8),
        consumerid Number(8),
        available Bool(1)
        created date,
        compleated date
    );
    """

def getTransactionsByUser(cur, userid):
    return cur.execute("SELECT ROW_NUMBER() FROM posts WHERE consumerid=userid OR producerid=userid;").fetchmany()

def completeTransaction(cur, postid, consumerid):
    timeStamp = datetime.datetime.now();
    cur.execute("UPDATE Posts SET consumerid=userid, available=False, compleated=timeStamp WHERE ROW_NUMBER()=postid;")