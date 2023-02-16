from django.http import HttpResponse, JSONResponse, HTTPRequest
import datetime
import sqlite3
import json

def index(request):
    return HttpResponse("Hello, world!")

"""
CREATE TABLE Posts(
    producerid Number(1000000),
    recipeid Number(1000000),
    created String(255),
    consumerid Number(1000000),
    available Bool(1)
    compleated String()
);
"""

# TODO: add error protection around sql (sqlite3.Error)
# TODO: properly read and return requests and responses
# TODO: test to make sure it works. :(

# interact with database:

def getPostsByUser(cur, producerid):
    postids = cur.execute("SELECT ROW_NUMBER FROM posts WHERE producerid=%d;", producerid).fetchall()
    posts=[]
    for i in range(0, len(postids)):
        row = cur.execute("SELECT * FROM Posts WHERE ROW_NUMBER()=%d",postids[i]).fetchone()
        posts[i] = Post(cur, row[0], row[1], row[2]);
    return posts

def createPost(cur, postid, producerid, recipeid):
    if (cur.execute("Select 1 FROM Posts where producerid=%d;", producerid).fetchone()[0] == 1):
        raise ValueError("Producerid is invalid")
    if (cur.execute("Select 1 FROM Posts where recipeid=%d;", recipeid).fetchone()[0] <= 1):
        raise ValueError("Recipeid is invalid")

    timeStamp = datetime.datetime.now();
    cur.execute("INSERT INTO Posts (producerid, recipeid, available, created) VALUES (%d, %d, %d, %s);", (producerid, recipeid, 1, timestamp))

    return Post(cur, producerid, recipeid, timeStamp)

def getTransactionsByUser(cur, userid):
    postids = cur.execute("SELECT ROW_NUMBER FROM posts WHERE consumerid=userid OR producerid=userid;").fetchall()
    posts=[]
    for i in range(0, len(postids)):
        row = cur.execute("SELECT * FROM Posts WHERE ROW_NUMBER()=%d",postids[i]).fetchone()
        posts[i] = Post(cur, row[0], row[1], row[2]);
    return posts

def completeTransaction(cur, postid, consumerid):
    timeStamp = datetime.datetime.now();
    cur.execute("UPDATE Posts SET consumerid=userid, available=False, compleated=timeStamp WHERE ROW_NUMBER()=postid;")
    row = cur.execute("SELECT * FROM Posts where ROW_NUMBER()=%d",postid).fetchone()
    return Post(cur, row[0], row[1], row[2]);

# interact w/ user

def create_post_resp(cur, request):
    if request.method != 'POST':
        return JSONResponse(json.loads({"status":0}))
    try:
        post = createPost(cur, request.args.get("producerid"), request.args.get("producerid"), request.args.get("recipeid"))
    except ValueError() as E:
        return JSONResponse(json.loads({"status":0}))
    return JSONResponse(json.loads(post.toJson()))

def update_post_resp(cur, request):
    if request.method != 'POST':
        return JSONResponse(json.loads({"status":0}))
    try:
        post = completeTransaction(cur, request.args.get("postid"), request.args.get("consumerid"))
    except ValueError() as E:
        return JSONResponse(json.loads({"status":0}));
    return JSONResponse(json.loads(post.toJson()))

def get_posts_by_user_resp(cur, request):
    if request.method != "GET":
        return JSONResponse(json.loads({"status":0}))

    posts = getPostsByUser(cur, request.args.get("producerid"))
    out = []
    for post in posts:
        out.append(post.toJson);
    
    return JSONResponse(json.loads({"posts":out}))

def get_transactions_by_user_resp(cur, request):
    if request.method != "GET":
        return JSONResponse(json.loads({"status":0}))

    posts = getTransactionsByUser(cur, request.args.get("producerid"))
    out = []
    for post in posts:
        out.append(post.toJson);
    
    return JSONResponse(json.loads({"posts":out}))