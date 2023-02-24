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
    | = one or more of
    GET
        posts(producer) - posts produced by a user
        posts(user) - posts including a user
        posts(id) - a specific post with a specific id
        posts() - all posts
    POST:
        posts(producer, recipe, title, desc) - creates a new post with the above description
            TODO: make desc optional
        posts(id, title||desc||producer||consumer||recipe) - updates an existing post
            if the consumer is updated and post_available is true, marks post as non avialable and sets post_completed
    Returns:
        post[]: a list of posts found
    """
    if request.method == 'GET':
        posts = None
        if 'producer' in request.GET:
            producer = request.GET.get('producer')
            posts = Post.objects.filter(post_producer__exact=producer)
        elif 'user' in request.GET:
            user = request.GET.get('user')
            posts = Post.objects.filter(post_producer__exact=user) | Post.objects.filter(post_consumer__exact=user)
        elif 'id' in request.GET:
            postid = request.GET.get('id')
            posts = Post.objects.filter(post_id__exact=postid)
        else:
            posts=Post.objects.all()
        return JsonResponse(serializers.serialize('json', posts), safe=False)
    elif request.method == 'POST':
        post = None
        if 'id' in request.POST:
            postid = request.POST.get('id')
            post = Post.objects.filter(post_id__exact=postid)
            if 'title' in request.POST:
                post.post_title = request.POST.get('title')
            if 'desc' in request.POST:
                post.post_desc = request.POST.get('desc')
            if 'producer' in request.POST:
                post.post_producer = request.POST.get('producer')
            if 'consumer' in request.POST:
                if not post.post_available:
                    post.post_available = False
                    post.post_completed = datetime.datetime.now()
                post.post_consumer = request.POST.get('consumer')
            if 'recipe' in request.POST:
                post.post_recipe = request.POST.get('recipe')
            post.save
        elif ('producer' in request.POST) and ('recipe' in request.POST) and ('title' in request.POST) and ('desc' in request.POST):
            producer = request.POST.get('producer')
            recipe = request.POST.get('recipe')
            title = request.POST.get('title')
            desc = reqeusts.POST.get('desc')
            post = Post(post_producer=producer, post_recipe=recipe, post_created=datetime.datetime.now(), post_title=title, post_desc=desc)
            post.save()
        return JsonResponse(serializers.serialize('json', post), safe=False)

def user_manager(request):
    """
    * = optional argument
    | = one argument or the other
    TODO
    GET:
        users(email|username) - returns a user object coresponding to the correct email
        users(id) - returns the user coresponding to the user id
        users(email|username, password) - confirms if the email / password combo is valid (TODO: update to password hash)
    POST:
        users(email, username, password, *address, *biography) - creates a new user
        users(id|email|username, email|username|password|address|biography)
    """
    if request.method == 'GET':
        if 'id' in request.GET:
            return JsonResponse(serializers.serialize('json', USER.objects.filter(user_id__exact=request.GET.get('id'))), safe=False)
        if 'username' in request.GET and 'pass' in request.GET:
            #find username & verify password
            return "TO Be Completed later!"
        if 'email' in request.GET and 'pass' in request.GET:
            #find email & verify password
            return "TO Be Completed later!"
        if 'username' in request.GET:
            return JsonResponse(serializers.serialize('json', USER.objects.filter(user_uname__exact=request.GET.get('username'))), safe=False)
        if 'email' in request.GET:
            return JsonResponse(serializers.serialize('json', USER.objects.filter(user_email__exact=request.GET.get('email'))), safe=False)
    if request.method == 'POST':
        if ('email' in request.POST) and ('username' in request.POST) and ('password' in request.POST):
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('pass')
            if len(list(User.object.filter(user_email__exact=email))) > 0 or len(list(User.object.filter(user_uname__exact=username))) > 0:
                #TODO: verify username is acceptable, split username and email and return an actual error here
                return "ERROR, username or email already taken"
            user = User(user_email=email, user_uname=username, user_password=password)
            if 'address' in request.POST:
                user.user_address=request.get('address')
            if 'bio' in request.POST:
                user.user_bio=requesst.get('bio')
            user.save()
            return JsonResponse(serializers.serialize('json', user), safe=False)
        if 'id' in request.POST:
            user = User.objects.filter(user_id__exact=request.POST.get('id'))
            if 'email' in request.POST:
                # TODO: verify email isn't taken
                user.user_email = request.POST.get('email')
            if 'uname' in request.POST:
                # TODO: verify email isn't taken
                user.user_email = request.POST.get('email')

                    
