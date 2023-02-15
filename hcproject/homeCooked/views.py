from django.http import HttpResponse
import datetime
import sqlite3

def index(request):
    return HttpResponse("Hello, world!")

def getPostsByUser(cur, userid):
    return cur.execute("SELECT ROW_NUMBER() FROM Posts WHERE producerid=%d;", userid).fetchmany();

def createPost(cur, postid, producerid, recipeid):
    timeStamp = datetime.datetime.now();

    if (cur.execute("Select 1 FROM Posts where producerid=%d", producerid).fetchone() == 1):
        raise ValueError("Producerid is invalid")

    if (cur.execute("Select 1 FROM Posts where recipeid=%d", recipeid).fetchone() != 1):
        raise ValueError("Recipeid is invalid")

    cur.execute("INSERT INTO Posts (producerid, recipeid, available, created) VALUES (%d, %d, %d, %s);", (producerid, recipeid, 1, timestamp))
    return True

    """
    CREATE TABLE Posts(
        producerid Number(16),
        recipeid Number(16),
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
    return True;