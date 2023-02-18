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
# TODO: test to make sure it works. :(

# interact with database:

def getPostsByUser(request, producer):
    return Post.objects.filter(producer__exact=producer)

def createPost(user, recipeUsed):
    post = Post(producer=producercur, recipe=recipeUsed, created=datetime.datetime.now())
    post.save()

def getTransactionsByUser(cur, user):
    createdBy = Post.objects.filter(producer__exact=user)
    boughtFrom = Post.objects.filter(consumer__exact=user)
    return createdBy.union(boughtFrom)

def completeTransaction(postid, user):
    post=Post.objects.get(id__exact=post)

    post.consumer=user
    post.compleated=datetime.datetime.now()
    post.save()
    return post