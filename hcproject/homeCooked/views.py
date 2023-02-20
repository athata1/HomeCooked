from django.http import HttpResponse
from django.shortcuts import render
from .models import Post, Recipe, User
# import datetime
# import sqlite3
# import json

def index(request):
    latest_user_list = User.objects.order_by('-user_id')[:5]
    context = {'latest_user_list': latest_user_list}
    return render(request, 'homeCooked/index.html', context)

def user(request, user_id):
    return HttpResponse("You're looking at user %s." % user_id)
    

# def getPostsByUser(producer):
#     return Post.objects.filter(post_producer__exact=producer)

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