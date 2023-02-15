from django.http import HttpResponse, HTTPRequest
import datetime
import sqlite3
import json

def index(request):
    return HttpResponse("Hello, world!")

def convert_to_post(producerid, recipeid, timeStamp):
    postid = cur.execute("SELECT ROW_NUMBER() FROM Posts WHERE created=%s AND producerid=%d", timeStamp, producerid)
    return Post(postid, producerid, recipeid, timeStamp)

def create_post_resp(request):
    if request.method != 'POST':
        return HttpResponse("Failed to create a new post")
    post = createPost(request.data["producerid"], request.data["producerid"], request.data["recipeid"])

def getPostsByUser(cur, userid):
    return cur.execute("SELECT ROW_NUMBER() FROM Posts WHERE producerid=%d;", userid).fetchmany();

def createPost(cur, postid, producerid, recipeid):
    timeStamp = datetime.datetime.now();

    if (cur.execute("Select 1 FROM Posts where producerid=%d", producerid).fetchone() == 1):
        raise ValueError("Producerid is invalid")

    if (cur.execute("Select 1 FROM Posts where recipeid=%d", recipeid).fetchone() != 1):
        raise ValueError("Recipeid is invalid")

    cur.execute("INSERT INTO Posts (producerid, recipeid, available, created) VALUES (%d, %d, %d, %s);", (producerid, recipeid, 1, timestamp))
    return convert_to_post(producerid, recipeid, timeStamp)

    """
    CREATE TABLE Posts(
        producerid Number(1000000),
        recipeid Number(1000000),
        consumerid Number(1000000),
        available Bool(1)
        created String(255),
        compleated String()
    );
    """

def getTransactionsByUser(cur, userid):
    postids = cur.execute("SELECT ROW_NUMBER() FROM posts WHERE consumerid=userid OR producerid=userid;").fetchmany()
    posts=[]
    for i in range(0, len(postids)):
        # "SELECT * FROM Posts WHERE ROW_NUMBER()=%d", postid
        posts[i] = Post(postid, producerid, recipeid, timeStamp);

    return posts

def completeTransaction(cur, postid, consumerid):
    timeStamp = datetime.datetime.now();
    cur.execute("UPDATE Posts SET consumerid=userid, available=False, compleated=timeStamp WHERE ROW_NUMBER()=postid;")
    return post; # TODO: return the updated post object.