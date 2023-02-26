from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect
from django.core import serializers
from .models import *
# import datetime
# import sqlite3
import json
import requests
# import firebase_admin
# from firebase_admin import credentials, auth


# def validate_token(token):
#     decoded_token = auth.verify_id_token(token)
#     if decoded_token is None:
#         return None
#     email = decoded_token['email']
#     return email

def allergy_request(request):
    if request.method == 'POST':
        food = request.POST['food']
        url = "https://edamam-edamam-nutrition-analysis.p.rapidapi.com/api/nutrition-data"
        querystring = {"ingr":"1 " + food}
        headers = {
            "X-RapidAPI-Key": "b9d9e48884mshcd3b1e80bcbbca0p1f65fajsn2999ad0fce27",
            "X-RapidAPI-Host": "edamam-edamam-nutrition-analysis.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        health_labels = ', '.join(data['healthLabels'])
        allergy = Allergy(food_name=food, health_labels=health_labels)
        allergy.save()
        return render(request, 'homeCooked/allergy.html', {'allergy': allergy})
    else:
        return render(request, 'homeCooked/allergy.html')

def delete_post(request):
    if request.method == 'POST':
        post_id=request.POST.get('id')
        post = Post.objects.filter(pk__exact=post_id)
        data = serializers.serialize('json', post)
        post.delete()
        return JsonResponse(data, safe=False)
    
def delete_user(request):
    if request.method == 'POST':
        user_id=request.POST.get('id')
        user = User.objects.filter(pk__exact=user_id)
        data=serializers.serialize('json', user)
        user.delete()
        return JsonResponse(data, safe=False)

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
    TODO: user uses tokens, not a lot of stuff, expect structure of pages / request types / queries to change

    * = optional argument
    | = one argument or the other
    GET:
        users(token) - returns a user object coresponding to the fid provided by the token
        users() - returns all users TODO: TEMPORARY, DEBUGGING ONLY. REMOVE ONCE DEBUGGING DONE
    POST:
        users(token, uname, pass, *address, *bio, *state, *city) - creates a new user
        users(token, fid|uname|pass|address|bio|city|state) - updates one of the user settings
    """
    if request.method == 'GET':
        if 'token' in request.GET:
            return JsonResponse(serializers.serialize('json', User.objects.flter(user_email__exact=validate_token(request.GET.get('token')))), safe=False)
        return JsonResponse(serializers.serialize('json', User.objects.all()), safe=False)
    if request.method == 'POST':
        if ('token' in request.POST) and ('uname' in request.POST):
            # new user
            fid = validate_token(request.POST.get('token'))
            if fid is None:
                return None
            username = request.POST.get('uname')
            if len(list(User.object.filter(user_fid__exact=fid))) > 0 or len(list(User.object.filter(user_uname__exact=username))) > 0:
                #TODO: verify username is acceptable and return an actual error here
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
        elif ('token' in request.POST) and (('fid' in request.POST) or ('uname' in request.POST) or ('address' in request.POST) or ('bio' in request.POST) or ('state' in request.POST) or ('city' in request.POST)): # change to id email or password
            user = User.objects.get(user_fid__exact=validate_token(request.POST.get('token')))

            if 'fid' in request.POST and len(list(User.object.filter(user_fid__exact=request.POST.get('fid')))) == 0:
                user.user_fid = request.POST.get('fid')
            elif len(list(User.object.filter(user_fid__exact=request.POST.get('fid')))) > 0:
                print("ERROR, fid/email already taken")
            if 'uname' in request.POST and len(list(User.object.filter(user_uname__exact=request.POST.get('uname')))) == 0:
                user.user_uname = request.POST.get('uname') # TODO: replace with real error warning
            elif len(list(User.object.filter(user_uname__exact=request.POST.get('uname')))) > 0:
                print("ERROR, username already taken") # TODO: replace with real error warning
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