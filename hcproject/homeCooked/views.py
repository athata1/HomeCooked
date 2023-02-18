from django.http import HttpResponse, JSONResponse, HTTPRequest
import datetime
import sqlite3
import json

def index(request):
    return HttpResponse("Hello, world!")

def getPostsByUser(producer):
    return Post.objects.filter(post_producer__exact=producer)

def createPost(user, recipeUsed):
    post = Post(post_producer=producercur, post_recipe=recipeUsed, post_created=datetime.datetime.now())
    post.save()

def getTransactionsByUser(cur, user):
    createdBy = Post.objects.filter(post_producer__exact=user)
    boughtFrom = Post.objects.filter(post_consumer__exact=user)
    return createdBy.union(boughtFrom)

def completeTransaction(id, user):
    post=Post.objects.get(post_id__exact=post)

    post.post_consumer=user
    post.post_compleated=datetime.datetime.now()
    post.save()
    return post