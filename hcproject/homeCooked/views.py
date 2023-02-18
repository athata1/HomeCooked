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

def getPostsByUser(producer):
    return Post.objects.filter(producer__exact=producer)

def createPost(postid, user, recipeUsed):
    post = Post(producer=producercur, recipe=recipeUsed, created=datetime.datetime.now())
    post.save()
    return post

def getTransactionsByUser(cur, user):
    createdBy = Post.objects.filter(producer__exact=user)
    boughtFrom = Post.objects.filter(consumer__exact=user)
    return createdBy.union(boughtFrom)

def completeTransaction(post, user):
    timeStamp = datetime.datetime.now();

    post.consumer=user
    post.compleated=datetime.datetime.now()
    post.save()
    return post

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