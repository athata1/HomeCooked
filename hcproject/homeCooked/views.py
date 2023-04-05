from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import *
import datetime
# import sqlite3
import json
import requests
from firebase_admin import credentials, auth
import ast
from django.db.models import Sum


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
        querystring = {"ingr": "1 " + food}
        headers = {
            "X-RapidAPI-Key": "b9d9e48884mshcd3b1e80bcbbca0p1f65fajsn2999ad0fce27",
            "X-RapidAPI-Host": "edamam-edamam-nutrition-analysis.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        health_labels = ', '.join(data['healthLabels'])
        health_labels = ', '.join([x.replace('_', ' ').title() for x in health_labels.split(', ')])
        extract_strings = ['Vegan', 'Vegetarian', 'Pescatarian', 'Dairy Free', 'Gluten Free', 'Wheat Free', 'Egg Free',
                           'Milk Free', 'Peanut Free', 'Tree Nut Free', 'Soy Free']
        health_labels = ', '.join([x.strip() for x in health_labels.split(',') if x.strip() in extract_strings])
        allergy = Allergy(food_name=food, health_labels=health_labels)
        allergy.save()
        return render(request, 'homeCooked/allergy.html', {'allergy': allergy})
    else:
        return render(request, 'homeCooked/allergy.html')

    # Deletes a post upon user request


@csrf_exempt
def delete_user(request):
    if request.method != 'POST':
        return JsonResponse(status=500, data={'response': 'Error: request type must be POST'})

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    if 'fid' not in parameters:
        return JsonResponse(status=404, data={'response': 'token not in parameters'})
    uid = validate_token(parameters.get('fid'))

    if uid is None:
        return JsonResponse(status=404, data={'response': 'token not in parameters'})

    user = User.objects.get(user_fid=uid)

    if user is None:
        return JsonResponse(status=400, data={'response': 'Error: User does not exist'})
    
    user.delete()
    return JsonResponse(status=200, data={'response': 'Deleted User'})


def index(request):
    user = User.objects.all

    use = {
        "username": user
    }
    return render(request, "homeCooked\index.html", use)


def allergens(food):
    url = "https://edamam-edamam-nutrition-analysis.p.rapidapi.com/api/nutrition-data"

    query_string = {"ingr": food}
    headers = {
        "X-RapidAPI-Key": "b9d9e48884mshcd3b1e80bcbbca0p1f65fajsn2999ad0fce27",
        "X-RapidAPI-Host": "edamam-edamam-nutrition-analysis.p.rapidapi.com"
    }
    res = requests.request("GET", url, headers=headers, params=query_string)
    print(res.text);
    return res.text


@csrf_exempt
def create_recipe(request):
    if request.method != 'POST':
        return JsonResponse(status=404, data={'response': 'Not post request'})
    # return JsonResponse(serializers.serialize('json', Recipe.objects.all()), safe=False)

    if 'fid' not in request.GET:
        return JsonResponse(status=404, data={'response': 'token not in parameters'})
    fid = validate_token(request.GET.get('fid'))

    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})

    user = User.objects.get(user_fid=fid)

    recipe_desc = request.GET.get('desc')
    recipe_user = user
    recipe_name = request.GET.get('title')
    recipe_ingredients = request.GET.get('ingredients')
    ingredients = ast.literal_eval(request.GET.get('ingredients'))
    recipe_sys_tags = allergens(str(ingredients))
    recipe_tags = request.GET.get('tags')
    vals = request.GET.get('image').split('/o/images/')
    recipe_img = vals[0] + "/o/images%2F" + vals[1]
    recipe = Recipe(recipe_desc=recipe_desc, recipe_user=recipe_user,
                    recipe_name=recipe_name, recipe_ingredients=recipe_ingredients,
                    recipe_sys_tags=recipe_sys_tags, recipe_tags=recipe_tags, recipe_img=recipe_img)
    recipe.save()
    return JsonResponse(status=200, data={'response': 'Created recipe'})


@csrf_exempt
def get_recipes_by_id(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response': 'not GET request'})

    if 'recipe_id' not in request.GET:
        return JsonResponse(status=404, data={'response': 'No recipe_ud in parameters'})
    try:
        recipe = Recipe.objects.filter(recipe_id=int(request.GET.get('recipe_id')))
        return JsonResponse(status=200, data={'response': serializers.serialize('json', recipe)})
    except Exception as e:
        print(e)
    return JsonResponse(status=404, data={'response': 'Error Occured'})


@csrf_exempt
def get_recipes(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response': 'not GET request'})
    if 'token' not in request.GET:
        return JsonResponse(status=404, data={'response': 'token not in parameters'})

    fid = validate_token(request.GET.get('token'))
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})

    user = User.objects.get(user_fid=fid)
    recipes = Recipe.objects.filter(recipe_user=user.user_id)

    return JsonResponse(status=200, data={'response': serializers.serialize('json', recipes)})


@csrf_exempt
def delete_recipe(request):
    if request.method != 'POST':
        return JsonResponse(status=404, data={'response': 'not POST request'})

    if 'token' not in request.GET:
        return JsonResponse(status=404, data={'response': 'token not in parameters'})
    fid = validate_token(request.GET.get('token'))
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})

    if 'recipe_id' not in request.GET:
        return JsonResponse(status=404, data={'response': 'recipe_id not found'})

    user = User.objects.get(user_fid=fid)
    try:
        recipe = Recipe.objects.get(recipe_user=user.user_id, recipe_id=request.GET.get('recipe_id'))
        recipe.delete()
    except:
        return JsonResponse(status=404, data={'response': 'Could not find recipe'})

    return JsonResponse(status=200, data={'response': 'Recipe deleted'})

@csrf_exempt
def change_event(request):
    if request.method != 'POST':
        return JsonResponse(status=404, data={'response': 'Not POST request'})

    if 'token' not in request.GET:
        return JsonResponse(status=404, data={'response', 'No token given'})

    fid = validate_token(request.GET.get('token'))
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})
    user = User.objects.get(user_fid=fid)

    if 'event-id' not in request.GET:
        return JsonResponse(status=404, data={'response', 'No event-id given'})

    event = Event.objects.get(pk=int(request.GET.get('event-id')))
    if event.event_host != user:
        return JsonResponse(status=404, data={'response', 'You do not have permission to change this'})

    if 'title' in request.GET:
        event.event_name = request.GET.get('title')
    if 'desc' in request.GET:
        event.event_desc = request.GET.get('desc')
    if 'location' in request.GET:
        event.event_location = request.GET.get('location')
    if 'time' in request.GET:
        date_time = datetime.datetime.fromtimestamp(int(request.GET.get('time')) / 1000)
        date = date_time.date()
        time = date_time.time()
        event.event_date = date
        event.event_time = time
    event.save()
    return JsonResponse(status=200, data={'response': 'Updated Event'})

@csrf_exempt
def create_event(request):
    if request.method != 'POST':
        return JsonResponse(status=404, data={'response': 'Not POST request'})

    if 'title' not in request.GET:
        return JsonResponse(status=404, data={'response', 'No title given'})

    if 'desc' not in request.GET:
        return JsonResponse(status=404, data={'response', 'No description given'})

    if 'location' not in request.GET:
        return JsonResponse(status=404, data={'response', 'No location given'})

    if 'time' not in request.GET:
        return JsonResponse(status=404, data={'response', 'No time given'})

    date_time = datetime.datetime.fromtimestamp(int(request.GET.get('time'))/1000)
    date = date_time.date()
    time = date_time.time()

    if 'token' not in request.GET:
        return JsonResponse(status=404, data={'response', 'No token given'})

    fid = validate_token(request.GET.get('token'))
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})
    user = User.objects.get(user_fid=fid)

    event = Event(event_desc=request.GET.get('desc'), event_location=request.GET.get('location'),
                  event_host=user, event_time=time, event_date=date, event_name=request.GET.get('title'))
    event.save()
    return JsonResponse(status=200, data={'response': 'Saved Event'})




@csrf_exempt
def get_user_id(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response': 'Not GET request'})

    if 'id' not in requests.GET:
        return JsonResponse(status=404, data={'response', 'Not id'})

    user = User.object.get(user_id=request.GET.get('id'))
    return JsonResponse(status=200, data={'response': user})

@csrf_exempt
def get_average_review(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response': 'Not POST request'})

    if 'fid' not in request.GET:
        return JsonResponse(status=404, data={'response': 'No fid in params'})

    fid = validate_token(request.GET.get('fid'))
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})
    user = User.objects.get(user_fid=fid)

    review = Review.objects.filter(review_receiver=user)
    count = len(list(review))
    sum_reviews = review.aggregate(Sum('review_rating'))
    if count == 0:
        return JsonResponse(status=200, data={'response': 5})
    avg = sum_reviews['review_rating__sum'] / count
    return JsonResponse(status=200, data={'response': avg})

@csrf_exempt
def get_reviews(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response', "Not a GET request"})

    if 'token' in request.GET:
        fid = validate_token(request.GET.get('token'))
        if fid is None:
            return JsonResponse(status=404, data={'response', "Could not find user"})
        user = User.objects.get(user_fid=fid)

        reviews = Review.objects.filter(review_receiver=user)
        return JsonResponse(status=200, data={'response': serializers.serialize('json', reviews)}, safe=False)

    elif 'uname' in request.GET:
        user = User.objects.get(user_uname=request.GET.get('uname'))
        reviews = Review.objects.filter(review_receiver=user)
        return JsonResponse(status=200, data={'response': serializers.serialize('json', reviews)}, safe=False)
    else:
        return JsonResponse(status=404, data={'response', 'Not valid method type'})

@csrf_exempt
def create_review(request):
    if request.method != 'POST':
        return JsonResponse(status=404, data={'response': 'Not POST request'})
    if 'fid' not in request.GET:
        return JsonResponse(status=404, data={'response': 'No fid in params'})

    fid = validate_token(request.GET.get('fid'))
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})
    user = User.objects.get(user_fid=fid)

    if 'description' not in request.GET:
        return JsonResponse(status=404, data={'response': 'No description in params'})

    if 'rating' not in request.GET:
        return JsonResponse(status=404, data={'response': 'No rating in params'})

    if 'post_id' not in request.GET:
        return JsonResponse(status=404, data={'response': 'No rating in params'})

    post = Post.objects.get(post_id=int(request.GET.get('post_id')))
    if post.post_consumer.user_fid != fid:
        return JsonResponse(status=404, data={'response': 'Do not have permission to create review'})

    review_receiver = Post.objects.get(post_id=int(request.GET.get('post_id'))).post_recipe.recipe_user
    review = Review(review_desc=request.GET.get('description'), review_giver=user,
                    review_receiver=review_receiver,
                    review_recipe=Post.objects.get(post_id=int(request.GET.get('post_id'))).post_recipe,
                    review_rating=float(request.GET.get('rating')), review_post=post)
    review.save()
    return JsonResponse(status=200, data={'response': 'Saved review'})

@csrf_exempt
def post_get_all(request):
    try:
        if request.method != 'GET':
            return JsonResponse(status=404, data={'response':'request method is not GET'})
        
        posts = Post.objects.all()
        return JsonResponse(status=200, data={'response': serializers.serialize('json', posts)})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response':'could not get post(s) ' + str(E)})

@csrf_exempt
def post_get_by_loc(request):
    try:
        if request.method != 'GET':
            return JsonResponse(status=404, data={'response': 'request method must be POST'})
        if 'city' not in request.GET:
            return JsonResponse(status=405, data={'response': 'missing parameter city'})
        if 'state' not in request.GET:
            return JsonResponse(status=405, data={'response': 'missing parameter state'})
    
        posts = []

        for user in User.objects.filter(user_city=request.GET.get('city'), user_state=request.GET.get('state')):
            posts.extend(Post.objects.filter(post_producer=user))
        
        return JsonResponse(status=200, data={'response': serializers.serialize('json', posts)})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response' : 'could not create post ' + str(E)})


@csrf_exempt
def post_sort(request):
    try:
        if request.method != 'GET':
            return JsonResponse(status=404, data={'response':'request method is not GET'})

        if 'token' not in request.GET:
            return JsonResponse(status=404, data={'response': 'token/fid not in parameters'})

        fid = validate_token(request.GET.get('token'))

        post_filter = request.GET.get('filter', 'none')

        if post_filter is None:
            return JsonResponse(status=405, data={'response': 'missing filter'})

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        user = User.objects.get(user_fid=fid)

        if user is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        if post_filter == 'open':
            posts = Post.objects.filter(post_producer=user.user_id, post_available=True)
            return JsonResponse(status=200, data={'response': serializers.serialize('json', posts)})
        elif post_filter == 'producer-closed':
            posts = Post.objects.filter(post_producer=user.user_id, post_available=False)
            return JsonResponse(status=200, data={'response': serializers.serialize('json', posts)})
        elif post_filter == 'consumer-closed':
            posts = Post.objects.filter(post_consumer=user.user_id, post_available=False)
            return JsonResponse(status=200, data={'response': serializers.serialize('json', posts)})
        else:
            return JsonResponse(status=404, data={
                'response': 'ValueError: filter (open, producer_closed, consumer_closed) missing or invalid'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response': 'could not get post(s) ' + str(E)})


@csrf_exempt
def post_create(request):
    try:
        if request.method != 'POST':
            return JsonResponse(status=404, data={'response': 'request method must be POST'})
        if 'token' not in request.GET:
            return JsonResponse(status=405, data={'response': 'token not in parameters'})

        parameters = request.POST
        if len(request.POST) == 0:
            parameters = request.GET

        fid = validate_token(parameters.get('token'))

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        user = User.objects.get(user_fid=fid)

        if user is None:
            return JsonResponse(status=400, data={'response': 'invalid token'})

        # seperating into diff lines so bugfixing (finding what is where) is easier

        title = parameters.get('title', 'none')
        desc = parameters.get('desc', 'none')
        created = timezone.now()

        recipe = Recipe.objects.get(recipe_id=int(parameters.get('recipe', '-1')))

        if recipe is None:
            return JsonResponse(status=400, data={'response': 'invalid recipe id'})

        post = Post(post_title=title, post_desc=desc,
                    post_producer=user, post_created=created,
                    post_recipe=recipe, post_available=True, post_consumer=None)
        post.save()
        return JsonResponse(status=200, data={'response': 'Post created'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response': 'could not create post ' + str(E)})

@csrf_exempt
def post_consumer_closed(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response': 'request method must be GET'})

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    fid = validate_token(parameters.get('token'))
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})
    user = User.objects.get(user_fid=fid)

    posts = Post.objects.filter(post_consumer=user);
    return JsonResponse(status=200, data={'response': serializers.serialize('json', posts)})


@csrf_exempt
def post_update(request):
    try:
        if request.method != 'POST':
            return JsonResponse(status=404, data={'response': 'request method must be POST'})

        parameters = request.POST
        if len(request.POST) == 0:
            parameters = request.GET

        if 'post-id' not in parameters:
            return JsonResponse(status=405, data={'response': 'request parameter "post-id" is missing'})

        post_id = int(parameters.get('post-id', '-1'))

        if post_id < 0:
            return JsonResponse(status=404, data={'response': 'missing/invalid post id'})

        post = Post.objects.get(post_id=post_id)

        if post is None:
            return JsonResponse(status=404, data={'response': 'unable to find post with matching id'})

        if 'token' not in parameters:
            return JsonResponse(status=405, data={'response': 'error, token required to update post'})

        fid = validate_token(parameters['token'])

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        if fid != post.post_producer.user_fid:
            return JsonResponse(status=404, data={'response': 'unauthorized: invalid fid'})

        title = parameters.get('title', '')
        desc = parameters.get('desc', '')
        recipe_id = parameters.get('recipe', '-1')

        if title != "":
            post.post_title = title

        if desc != "":
            post.post_desc = desc

        if int(recipe_id) > 0:
            recipe = Recipe.objects.get(recipe_id=int(recipe_id))

            if recipe is None:
                return JsonResponse(status=404, data={'response': 'unable to find recipe with matching id'})

            post.post_recipe = recipe

        post.save()

        return JsonResponse(status=200, data={'response': 'Post updated'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response': 'could not update post ' + str(E)})

@csrf_exempt
def get_events(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response': 'request method must be GET'})

    if 'token' not in request.GET:
        return JsonResponse(status=405, data={'response': 'error, token required to update post'})
    fid = validate_token(request.GET['token'])
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})

    user = User.objects.get(user_fid=fid)
    events = Event.objects.filter(event_host=user)
    return JsonResponse(status=200, data={'response': serializers.serialize('json', events)}, safe=False)



@csrf_exempt
def get_post_close(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response': 'request method must be GET'})

    if 'token' not in request.GET:
        return JsonResponse(status=405, data={'response': 'error, token required to update post'})

    fid = validate_token(request.GET['token'])

    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})

    user = User.objects.get(user_fid=fid)
    lng = user.user_longitude
    lat = user.user_latitude
    lng_min = lng - 2
    lng_max = lng + 2
    lat_min = lat - 2
    lat_max = lat + 2

    posts = Post.objects.select_related('post_producer').filter(post_producer__user_longitude__lt=lng_max,
                                                                post_producer__user_longitude__gt=lng_min,
                                                                post_producer__user_latitude__lt=lat_max,
                                                                post_producer__user_latitude__gt=lat_min)
    return JsonResponse(status=200, data={'response': serializers.serialize('json', posts)}, safe=False)


@csrf_exempt
def post_close(request):
    try:
        if request.method != 'POST':
            return JsonResponse(status=404, data={'response': 'request method must be POST'})

        parameters = request.POST
        if len(request.POST) == 0:
            parameters = request.GET

        if 'token' not in parameters:
            return JsonResponse(status=404, data={'response': 'No token'})

        fid = validate_token(request.GET.get('token'))

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        if 'post-id' not in parameters:
            return JsonResponse(status=404, data={'response': 'No post id'})
        print(parameters.get('post-id'))
        post = Post.objects.get(pk=int(parameters.get('post-id')))

        if not post.post_available:
            return JsonResponse(status=404, data={'response': 'Error: post already closed'})


        if post.post_producer.user_fid != fid:
            return JsonResponse(status=404, data={'response': 'You do not have permission to do this'})

        user = User.objects.get(user_fid=fid)

        if "uname" not in parameters:
            return JsonResponse(status=404, data={'response': 'No consumer username'})

        consumer_user = User.objects.get(user_uname=parameters.get("uname"))

        post.post_consumer = consumer_user;
        post.post_available = False
        post.post_completed = timezone.now()
        post.save()

        return JsonResponse(status=200, data={'response': 'Post set to closed'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response': 'could not close post ' + str(E)})


@csrf_exempt
def post_delete(request):
    try:
        if request.method != 'POST':
            return JsonResponse(status=404, data={'response': 'request method must be POST'})

        parameters = request.POST
        if len(request.POST) == 0:
            parameters = request.GET

        if 'token' not in parameters:
            return JsonResponse(status=404, data={'response': 'token not in parameters'})

        fid = validate_token(request.GET.get('token'))

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        if 'post-id' not in parameters:
            return JsonResponse(status=404, data={'response': 'No post_id in parameters'})

        post = Post.objects.get(post_id=int(parameters.get('post-id')))

        if post.post_producer.user_fid != fid:
            return JsonResponse(status=404, data={'response': 'You do not have permission to delete this post'})
        else:
            post.delete()
            return JsonResponse(status=200, data={'response': 'Deleted Post'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response': 'could not delete post: ' + str(E)})


@csrf_exempt
def user_by_uname(request):
    if request.method == 'GET':
        if 'uname' not in request.GET:
            return JsonResponse(status=405, data={'response': 'missing uname in parameter'})

        user = User.objects.filter(user_uname__exact=request.GET.get('uname'))
        if len(list(user)) != 0:
            return JsonResponse(status=405, data={'data': serializers.serialize('json', user)}, safe=False)
        return JsonResponse(status=404, data={'response': 'uname does not exist'})
    return JsonResponse(status=405, data={'response': 'Not Get request'})


@csrf_exempt
def user_by_id(request):
    if request.method == 'GET':
        if 'id' not in request.GET:
            return JsonResponse(status=405, data={'response': 'missing uname in parameter'})

        user = User.objects.filter(user_id=request.GET.get('id'))
        if len(list(user)) != 0:
            return JsonResponse(status=200, data={'data': serializers.serialize('json', user)}, safe=False)
        return JsonResponse(status=404, data={'response': 'id does not exist'})
    return JsonResponse(status=405, data={'response': 'Not Get request'})

@csrf_exempt
def user_manager(request):
    if request.method == 'GET':
        # return JsonResponse(data={'status': '200', 'user': serializers.serialize('json', User.objects.all())}, safe=False)
        if 'fid' not in request.GET:
            return JsonResponse(status=404, data={'response': "Error: token not valid"})

        fid = validate_token(request.GET.get('fid'))

        if fid is None:
            return JsonResponse(status=404, data={'response': "Error: token not valid"})

        user = User.objects.filter(user_fid__exact=fid).only('user_uname', 'user_city', 'user_state', 'user_bio')

        if user is None:
            return JsonResponse(status=404, data={'response': "Error: could not find user"})

        return JsonResponse(status=200, data={'user': serializers.serialize('json', user)}, safe=False)
    
    if request.method == 'POST':
        
        parameters = request.POST
        if len(request.POST) == 0:
            parameters = request.GET

        if 'fid' not in parameters:
            return JsonResponse(status=405, data={'response': "Error: Missing fid"})
        if 'type' not in parameters:
            return JsonResponse(status=405, data={'response': "Error: Missing request type"})

        print(request.GET.get('fid'))
        fid = validate_token(parameters.get('fid'))

        if fid is None:
            return JsonResponse(status=404, data={'response': "Error: invalid token"})

        if parameters.get('type') == "Create":
            # new user
            if 'uname' not in parameters:
                return JsonResponse(status=405, data={'response': "Error: Username missing"})

            username = parameters.get('uname')

            if len(list(User.objects.filter(user_fid=fid))) != 0:
                return JsonResponse(status=404, data={'response': "Error: Account already created"})

            if len(list(User.objects.filter(user_uname=username))) != 0:
                return JsonResponse(status=404, data={'response': "Error: Account already created"})

            user = User(user_fid=fid, user_uname=username)
            user.save()

            return JsonResponse(status=200, data={ 'data': 'Created user'}, safe=False)
        elif parameters.get('type') == "Change":  # change to id email or password

            uid = validate_token(parameters.get('fid'))

            if uid is None:
                return JsonResponse(status=404, data={'response': "Error: invalid token"})

            user = User.objects.get(user_fid=uid)

            if user is None:
                return JsonResponse(status=404, data={'response': "Error: no user matching that fid"})
            
            if 'uname' in parameters:
                if len(list(User.objects.filter(user_uname=parameters.get('uname')))) == 0:
                    user.user_uname = parameters.get('uname')
                else:
                    if (User.objects.get(user_uname=parameters.get('uname')) != user):
                        return JsonResponse(status=404, data={'response': "Error: username already taken"})

            if 'address' in parameters:
                user.user_address = parameters.get('address')
            if 'bio' in parameters:
                user.user_bio = parameters.get('bio')
            if 'city' in parameters:
                user.user_city = parameters.get('city')
            if 'state' in parameters:
                user.user_state = parameters.get('state')
            if 'zip' in parameters:
                user.user_zip = parameters.get('zip')
            if 'image' in parameters:
                vals = parameters.get('image').split('/o/images/')
                user.image_text = vals[0] + "/o/images%2F" + vals[1]
            if 'lng' in parameters:
                val = float(parameters.get('lng'))
                user.user_longitude = val
            if 'lat' in parameters:
                val = float(parameters.get('lat'))
                user.user_latitude = val
            user.save()

            return JsonResponse(status=200, data={'response': 'Saved data'}, safe=False)


@csrf_exempt
def search_for(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response': 'request method must be GET'})
    if 'query' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "query" required'})
    try:
        query=request.GET.get('query')
        results = []
        if 'filter_posts' not in request.GET:
            results.extend(Post.objects.filter(post_title__icontains=query))
        if 'filter_city' not in request.GET:
            for users in Users.objects.filter(user_city=request.GET.get('city'), user_state=request.GET.get('state')):
                results.extend(Post.objects.filter(post_producer=user))
        if 'filter_users' not in request.GET:
            results.extend(User.objects.filter(user_uname__icontains=query))

        for user in list(User.objects.filter(user_uname__icontains=query)):    
            if 'filter_producer' not in request.GET:
                results.extend(Post.objects.filter(post_producer=user))
            if 'filter_consumer' not in request.GET:
                results.extend(Post.objects.filter(post_consumer=user))
        
        return JsonResponse(status=200, data={'response': serializers.serialize('json', list(set(results)))})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response' : 'could not create post ' + str(E)})