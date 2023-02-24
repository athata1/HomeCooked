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

'''.git\
TODO:
1. change to a class based model
2. urls to have:
posts/
    /author, 
    /all user
    /new user, recipe, title, desc
    /buy id, consumer
    /complete id, producer, recipe, title, desc, consumer
'''

def post_produced_by(request):
    if request.method == 'GET':
        pk = request.GET.get('user', None)
        return JsonResponse(serializers.serialize('json', Post.objects.filter(post_producer__exact=pk)), safe=False)

def post_new_post(request):
    if request.method == 'POST':
        producer = request.POST.get('producer', None)
        created = request.POST.get('recipe', None)
        title = request.POST.get('title', None)
        desc = reqeusts.POST.get('desc', None)
        post = Post(post_producer=producer, post_recipe=recipe, post_created=datetime.datetime.now(), post_title=title, post_desc=desc)
        post.save()
        return JsonResponse(serializers.serialize('json', post), safe=False)

def post_post_has(request):
    if request.method == 'GET':
        user=request.GET.get('user', None)
        print(user)
        createdBy = Post.objects.filter(post_producer__exact=user)
        boughtFrom = Post.objects.filter(post_consumer__exact=user)
        data = createdBy.union(boughtFrom)
        return JsonResponse(serializers.serialize('json', data), safe=False)

def post_complete(request):
    if request.method == 'POST':
        post = requests.POST.get('id', None)
        consumer = requests.POST.get('consumer', None)

        post=Post.objects.get(post_id__exact=post)

        post.post_consumer=user
        post.post_compleated=datetime.datetime.now()
        post.post_available=False
        post.save()
        return JsonResponse(serializers.serialize('json', post), safe=False)

def post_get(requst):
    if request.method == 'GET':
        post = request.GET.get('id', None)
        return JsonResponse(serializers.serialize('json', Post.objects.filter(post_id__exact=post)), safe=False)

def post_update(request):
    if request.method == 'POST':
        postid = request.POST.get('id', False)
        title = request.POST.get('title', False)
        desc = request.POST.get('desc', False)
        producer = request.POST.get('producer', False)
        consumer = request.POST.get('consumer', False)
        recipe = request.POST.get('recipe', False)

        post = Post.objects.filter(post_id__exact=postid)
        if 'title' in request.POST:
            post.post_title = request.POST.get('title', 'ERROR!!')
        if 'desc' in request.POST:
            post.post_desc = request.POST.get('desc', 'ERROR!!')
        if 'producer' in request.POST:
            post.post_producer = request.POST.get('producer', 'ERROR!!')
        if 'consumer' in request.POST:
            post.post_consumer = request.POST.get('consumer', 'ERROR!!')
        if 'recipe' in request.POST:
            post.post_recipe = request.POST.get('recipe', 'ERRROR!')
        
        post.save()

        return JsonResponse(serializers.serialize('json', post), safe=False)
        