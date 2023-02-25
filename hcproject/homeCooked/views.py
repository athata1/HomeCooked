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
        posts(id, title|desc|producer|consumer|recipe) - updates an existing post
            if the consumer is updated and post_available is true, marks post as non avialable and sets post_completed
    Returns:
        post[]: a list of posts found
    """
    if request.method == 'GET':
        posts = None
        if 'producer' in request.GET:
            producer = request.GET.get('producer')
            posts = Post.objects.filter(post_producer__exact=producer)
        elif 'userid' in request.GET:
            user = request.GET.get('userid')
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
        users(email|uname) - returns a user object coresponding to the correct email
        users(id) - returns the user coresponding to the user id
        users(state, city) - returns the users in a specific state and city
        TODO: users(email|uname, password) - confirms if the email / password combo is valid (TODO: update to password hash)
    POST:
        users(email, uname, pass, *address, *bio, *state, *city) - creates a new user
        users(id|prev_email|prev_uname, email|uname|pass|address|bio|city|state) - updates one of the previous fields
    """
    if request.method == 'GET':
        if 'id' in request.GET:
            return JsonResponse(serializers.serialize('json', User.objects.filter(user_id__exact=request.GET.get('id'))), safe=False)
        if 'uname' in request.GET and 'pass' in request.GET:
            # TODO: find username & verify password
            return "TO Be Completed later!"
        if 'email' in request.GET and 'pass' in request.GET:
            # TODO: find email & verify password
            return "TO Be Completed later!"
        if 'uname' in request.GET:
            return JsonResponse(serializers.serialize('json', User.objects.filter(user_uname__exact=request.GET.get('username'))), safe=False)
        if 'email' in request.GET:
            return JsonResponse(serializers.serialize('json', User.objects.filter(user_email__exact=request.GET.get('email'))), safe=False)
        if ('city' in request.GET) and ('state' in request.GET):
            return JsonResponse(serializers.serialize('json', User.objects.filter(user_state__exact=request.GET.get('state')).filter(user_state__exact=request.GET.get('city'))), safe=False)
    if request.method == 'POST':
        if ('email' in request.POST) and ('uname' in request.POST) and ('pass' in request.POST):
            # new user
            email = request.POST.get('email')
            username = request.POST.get('uname')
            password = request.POST.get('pass')
            if len(list(User.object.filter(user_email__exact=email))) > 0 or len(list(User.object.filter(user_uname__exact=username))) > 0:
                #TODO: verify username is acceptable, split username and email and return an actual error here
                return "ERROR, username or email already taken"
            user = User(user_email=email, user_uname=username, user_pass=password)
            if 'address' in request.POST:
                user.user_address=request.get('address')
            if 'bio' in request.POST:
                user.user_bio=requesst.get('bio')
            if 'city' in request.POST:
                user.user_city=requesst.get('city')
            if 'state' in request.POST:
                user.user_state=request.get('state')
            user.save()
            return JsonResponse(serializers.serialize('json', user), safe=False)
        elif ('id' in request.POST) or ('email' in request.POST) or ('username' in request.POST): # change to id email or password
            # Find user TODO: send 500 if can't find user
            user = None
            if 'id' in request.POST:
                user = User.objects.filter(user_id__exact=request.POST.get('id'))
            if 'prev_uname' in request.POST:
                user = User.objects.filter(user_uname__exact=request.POST.get('prev_uname'))
            if 'prev_email' in request.POST:
                user = User.objects.filter(user_email__exact=request.POST.get('prev_email'))
            
            # updating the requested feature TODO: seperate uname and email for finding and the to update uname and email 
            if 'email' in request.POST:
                # TODO: verify email isn't taken
                user.user_email = request.POST.get('email')
            if 'uname' in request.POST:
                # TODO: verify username isn't taken
                user.user_uname = request.POST.get('uname')
            if 'pass' in request.POST:
                user.user_pass = request.POST.get('pass')
            if 'address' in request.POST:
                user.user_address = request.POST.get('address')
            if 'bio' in request.POST:
                user.user_bio = request.POST.get('bio')
            if 'city' in request.POST:
                user.user_city = request.POST.get('city')
            if 'state' in request.POST:
                user.user_state = request.POST.get('state')
            user.save()
            return JsonResponse(serializers.serialize('json', user), safe=False)