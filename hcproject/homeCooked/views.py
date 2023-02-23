from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render
from django.core import serializers
from .models import Post, Recipe, User
# import datetime
# import sqlite3
import json

def index(request):
    user = User.objects.all

    use = {
        "username" : user
    }
    return render(request, "homeCooked\index.html", use)

def post_request(request):
    posts = Post.objects.all

    context = {
        "post_list" : posts
    }
    return render(request, "homeCooked\posts.html", context)

def post_byUser_request(request, pk):
    return JsonResponse(serializers.serialize('json', Post.objects.filter(post_producer__exact=pk)), safe=False)

# def createPost(user, recipeUsed):
#     post = Post(post_producer=producercur, post_recipe=recipeUsed, post_created=datetime.datetime.now())
#     post.save()

# def getTransactionsByUser(cur, user):
#     createdBy = Post.objects.filter(post_producer__exact=user)
#     boughtFrom = Post.objects.filter(post_consumer__exact=user)
#     return createdBy.union(boughtFrom)

# def completeTransaction(id, user):
#     post=Post.objects.get(post_id__exact=post)

#     post.post_consumer=user
#     post.post_compleated=datetime.datetime.now()
#     post.save()
#     return post