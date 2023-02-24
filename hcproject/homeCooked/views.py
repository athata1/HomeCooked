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


def post_manager(request):
    """
    GET
        posts(producer) - posts produced by a user
        posts(user) - posts including a user
        posts(id) - a specific post with a specific id
        posts() - all posts
    POST:
        posts(producer, recipe, title, desc) - creates a new post with the above description
        posts(id, title|desc|producer|consumer|recipe) - updates an existing post
            if the consumer is updated and post_available is true, marks post as non avialable and sets post_completed
    Returns:
        post[]: a list of posts found
    """
    if request.method == 'GET':
        posts = None
        if 'producer' in request.GET:
            producer = request.GET.get('producer', None)
            posts = Post.objects.filter(post_producer__exact=producer)
        elif 'user' in request.GET:
            user = request.GET.get('user', None)
            posts = Post.objects.filter(post_producer__exact=user) | Post.objects.filter(post_consumer__exact=user)
        elif 'id' in request.GET:
            postid = request.GET.get('id', None)
            posts = Post.objects.filter(post_id__exact=postid)
        else:
            posts=Post.objects.all()
        return JsonResponse(serializers.serialize('json', posts), safe=False)
    elif request.method == 'POST':
        post = None
        if 'id' in request.POST:
            postid = request.POST.get('id', None)
            post = Post.objects.filter(post_id__exact=postid)
            if 'title' in request.POST:
                post.post_title = request.POST.get('title', 'ERROR!!')
            if 'desc' in request.POST:
                post.post_desc = request.POST.get('desc', 'ERROR!!')
            if 'producer' in request.POST:
                post.post_producer = request.POST.get('producer', 'ERROR!!')
            if 'consumer' in request.POST:
                if not post.post_available:
                    post.post_available = False
                    post.post_completed = datetime.datetime.now()
                post.post_consumer = request.POST.get('consumer', 'ERROR!!')
            if 'recipe' in request.POST:
                post.post_recipe = request.POST.get('recipe', 'ERRROR!')
            post.save
        elif ('producer' in request.POST) and ('recipe' in request.POST) and ('title' in request.POST) and ('desc' in request.POST):
            producer = request.POST.get('producer', None)
            recipe = request.POST.get('recipe', None)
            title = request.POST.get('title', None)
            desc = reqeusts.POST.get('desc', None)
            post = Post(post_producer=producer, post_recipe=recipe, post_created=datetime.datetime.now(), post_title=title, post_desc=desc)
            post.save()
        return JsonResponse(serializers.serialize('json', post), safe=False)