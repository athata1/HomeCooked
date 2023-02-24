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


def post_produced_by(request):
    """
    TODO: combine with all other get methods to get any post that patches any parameter
    GET METHOD
    returns a list of post produced by a specific user
    
    Parameters:
        "user" (int): the userid of the person to search posts from

    Returns:
        post[]: a list of posts created by "user"

    """
    if request.method == 'GET':
        pk = request.GET.get('user', None)
        return JsonResponse(serializers.serialize('json', Post.objects.filter(post_producer__exact=pk)), safe=False)

def post_new_post(request):
    """
    POST method
    creates a new post based off of the producer, the recipe, title, and desc

    Parameters:
        producer (int): the producer id of the person creating the post
        recipe (int): the recipe id of the recipe used by the post
        title (string): the title of the post
        desc (string): the description of the post
    
    Returns:
        post: the new post created by "producer" using recipe "recipe", with title "title" and description "desc"
    """
    if request.method == 'POST':
        producer = request.POST.get('producer', None)
        recipe = request.POST.get('recipe', None)
        title = request.POST.get('title', None)
        desc = reqeusts.POST.get('desc', None)
        post = Post(post_producer=producer, post_recipe=recipe, post_created=datetime.datetime.now(), post_title=title, post_desc=desc)
        post.save()
        return JsonResponse(serializers.serialize('json', post), safe=False)

def post_post_has(request):
    """
    TODO: combine with all other get methods to get any post that patches any parameter
    GET method
    finds posts created by or bought by "user"

    Parameters:
        user (int): the userid of the person buying the meal

    Returns:
        post[]: a list of posts either created by or bought by "user"

    """
    if request.method == 'GET':
        user=request.GET.get('user', None)
        print(user)
        createdBy = Post.objects.filter(post_producer__exact=user)
        boughtFrom = Post.objects.filter(post_consumer__exact=user)
        data = createdBy.union(boughtFrom)
        return JsonResponse(serializers.serialize('json', data), safe=False)

def post_complete(request):
    """
    POST method
    completes a transaction in a post. (sets the consumer, completed time and marks it as no longer available)

    Parameters:
        id (int): the id of the post to complete
        consumer (int): the id of the user buying the food

    Returns:
        post: the updated post
    """
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
    """
    TODO: combine with all other get methods to get any post that patches any parameter
    GET method
    fetches a post with a specific id

    Parameters:
        id (int): the id of the post to fetch

    Returns:
        post: the post with the id "id"
    """

    if request.method == 'GET':
        post = request.GET.get('id', None)
        return JsonResponse(serializers.serialize('json', Post.objects.filter(post_id__exact=post)), safe=False)

def post_update(request):
    """
    POST method
    updates a post to fix either the title, description, producer, consumer, or recipe used

    Parameters:
        id (int, required): the id of the post to be updated
        title (string, optional): the updated title of the post
        desc (string, optional): the updated description of the post
        producer (int, optional): the updated producer id
        consumer (int, optional): the updated consumer id
        recipe (int, optional): the updated recipe id

    Returns:
        post: the updated post
    """

    if request.method == 'POST':
        postid = request.POST.get('id', None)
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
        