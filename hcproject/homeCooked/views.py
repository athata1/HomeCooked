from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import *
# import datetime
# import sqlite3
import json
import requests
from firebase_admin import credentials, auth


def validate_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
    except:
        return None;
    uid = decoded_token["uid"]
    return uid

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
        health_labels = ', '.join([x.replace('_', ' ').title() for x in health_labels.split(', ')])
        extract_strings = ['Vegan', 'Vegetarian', 'Pescatarian', 'Dairy Free', 'Gluten Free', 'Wheat Free', 'Egg Free', 'Milk Free', 'Peanut Free', 'Tree Nut Free', 'Soy Free']
        health_labels = ', '.join([x.strip() for x in health_labels.split(',') if x.strip() in extract_strings])
        allergy = Allergy(food_name=food, health_labels=health_labels)
        allergy.save()
        return render(request, 'homeCooked/allergy.html', {'allergy': allergy})
    else:
        return render(request, 'homeCooked/allergy.html')


    #Deletes a post upon user request

def delete_post(request):
    if request.method == 'POST':
        post_id=request.POST.get('id')
        post = Post.objects.filter(pk__exact=post_id)
        data = serializers.serialize('json', post)
        post.delete()
        return JsonResponse(data, safe=False)

    # Deletes a user and all associated data, 
    # i.e. any data with references to user will be deleted

@csrf_exempt
def delete_user(request):
    if request.method == 'POST':

        uid = validate_token(request.GET.get('fid'))

        if uid is None:
            return JsonResponse(data={'status': '400', 'message': 'Error invalid token'})

        user = User.objects.filter(user_fid=uid)
        if len(list(user)) == 0:
            return JsonResponse(data={'status': '400', 'message': 'Error: User does not exist'})
        user.delete()
        return JsonResponse(data={'status':'200','message':'Deleted User'})
    return JsonResponse(data={'status':'400','message':'Error not POST request'})

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


@csrf_exempt
def post_manager(request):
    if request.method == 'GET':
        posts = None
        if 'key' not in request.GET:
            return JsonResponse(data={'status':'400', 'message':'Error: no user/post id provided'})
        if 'type' not in request.GET:
            return JsonResponse(data={'status':'400', 'message':'Error: no type provided'})

        search_key = request.GET['user']
        request_type = request.GET['type']

        if search_key is NONE:
            return JsonResponse(data={'status':'400', 'message':'Error: search key invalid'})
        if request_type == 'producer':
            posts = Post.objects.filter(post_producer__exact=search_key)
            return JsonResponse({'status' : '200', 'posts' : serializers.serialize('json', posts)})
        elif request_type == 'transactions':
            posts = Post.objects.filter(post_producer__exact=search_key) | Post.objects.filter(post_consumer__exact=search_key)
            return JsonResponse({'status' : '200', 'posts' : serializers.serialize('json', posts)})
        elif request_type == 'single':
            posts = Post.objects.filter(post_id__exact=search_key)
            return JsonResponse({'status' : '200', 'posts' : serializers.serialize('json', posts)})
        else:
            return JsonResponse(data={'status':'400', 'message':'request type invalid'})
    elif request.method == 'POST':
        if 'type' not in request.POST:
            return JsonResponse(data={'status':'400', 'message':'Error: no type provided'})
        
        request_type = request.POST['type']
        
        if request_type == 'new':
            producer = request.POST['producer']
            recipe = request.POST['recipe']
            title = request.POST['title']
            desc = requests.POST['desc']

            if producer is None or recipe is None or title is None or desc is None:
                return JsonResponse(data={'status':'400', 'message':'Error: missing arguments.'})

            post = Post(post_producer=producer, post_recipe=recipe, post_created=datetime.datetime.now(), post_title=title, post_desc=desc)
            post.save()
            return JsonResponse(data={'status' : '200', 'post' : serializers.serialize('json', post)})
        elif request_type == 'update':
            if 'id' not in request.POST:
                return JsonResponse(data={'status':'400', 'message':'Error: no post id provided'})
            
            post = Post.objects.get(post_id=request.POST['id'])

            if post is None:
                return JsonResponse(data={'status':'400', 'message':'Error: no post with that id'})
            if 'title' in request.POST:
                post.post_title = request.POST['title']
            if 'desc' in request.POST:
                post.post_desc = request.POST['desc']
            if 'producer' in request.POST:
                post.post_producer = request.POST['producer']
            if 'consumer' in request.POST:
                if not post.post_available:
                    post.post_available = False
                    post.post_completed = datetime.datetime.now()
                post.post_consumer = request.POST['consumer']
            if 'recipe' in request.POST:
                post.post_recipe = request.POST['recipe']

            post.save()
            return JsonResponse(data={'status' : '200', 'post' : serializers.serialize('json', post)})

@csrf_exempt
def user_by_uname(request):
    if request.method == 'GET':
        if 'uname' not in request.GET:
            return JsonResponse(data={'status': '405', 'response': 'missing uname in parameter'})

        user = User.objects.filter(user_uname__exact=request.GET.get('uname'))
        if len(list(user)) != 0:
            return JsonResponse({'status':'200', 'data': serializers.serialize('json', user)}, safe=False)
        return JsonResponse(data={'status':'404', 'response':'uname does not exist'})
    return JsonResponse(data={'status': '405', 'response': 'Not Get request'})

@csrf_exempt
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
        #return JsonResponse(data={'status': '200', 'user': serializers.serialize('json', User.objects.all())}, safe=False)
        if 'fid' not in request.GET:
            return JsonResponse(data={'status': '404', 'message': "Error: token not valid"})

        fid = validate_token(request.GET.get('fid'))

        if fid is None:
            return JsonResponse(data={'status': '404', 'message': "Error: token not valid"})

        user = User.objects.filter(user_fid__exact=fid).only('user_uname', 'user_city', 'user_state', 'user_bio')

        if len(list(user)) == 0:
            return JsonResponse(data={'status': '404', 'message': "Error: could not find user"})

        return JsonResponse(data={'status': "200", 'user': serializers.serialize('json', user)}, safe=False)
    if request.method == 'POST':
        if 'fid' not in request.GET or 'type' not in request.GET:
            return JsonResponse(data={'status': '404', 'message': "Error: Missing parameters"})

        print(request.GET.get('fid'))
        fid = validate_token(request.GET.get('fid'))

        if fid is None:
            return JsonResponse(data={'status': '404', 'message': "Error: invalid token"})

        if request.GET.get('type') == "Create":
            # new user
            if 'uname' not in request.GET:
                return JsonResponse(data={'status': '404', 'message': "Error:username missing"})

            username = request.GET.get('uname')

            if len(list(User.objects.filter(user_fid__exact=fid))) != 0:
                return JsonResponse(data={'status': '404', 'message': "Error: Account Already created"})

            if len(list(User.objects.filter(user_uname__exact=username))) != 0:
                return JsonResponse(data={'status': '404', 'message': "Error: username already taken"})

            user = User(user_fid=fid, user_uname=username)
            user.save()

            return JsonResponse({'status': 200, 'data':'Created user'}, safe=False)
        elif request.GET.get('type') == "Change": # change to id email or password

            uid = validate_token(request.GET.get('fid'))

            if uid is None:
                return JsonResponse(data={'status': '404', 'message': "Error: invalid token"})

            user = User.objects.filter(user_fid__exact=uid)[0]
            if 'uname' in request.GET:
                if user.user_fid == uid and request.GET.get('uname') != user.user_uname:
                    if 'uname' in request.GET and len(list(User.objects.filter(user_uname__exact=request.GET.get('uname')))) == 0:
                        user.user_uname = request.GET.get('uname')
                    elif len(list(User.objects.filter(user_uname__exact=request.GET.get('uname')))) > 0:
                        return JsonResponse(data={'status': '404', 'message': "Error: username already taken"})
            if 'address' in request.GET:
                user.user_address = request.GET.get('address')
            if 'bio' in request.GET:
                user.user_bio = request.GET.get('bio')
            if 'city' in request.GET:
                user.user_city = request.GET.get('city')
            if 'state' in request.GET:
                user.user_state = request.GET.get('state')
            user.save()

            return JsonResponse(data={'status':'200', 'message':'Saved data'}, safe=False)