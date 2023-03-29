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
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be POST'})

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    if 'fid' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "fid" required'})
    
    try:
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = parameters.get('fid')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})
        user = User.objects.get(user_fid=fid)
        if user is None:
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})
        
        user.delete()
        return JsonResponse(status=200, data={'response': 'Deleted User'})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})


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
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be POST'})

    parameters = request.POST
    if len(request.POST) == 0:
       parameters = request.GET

    # return JsonResponse(serializers.serialize('json', Recipe.objects.all()), safe=False)
    try:
        # get user object from token
        if 'fid' not in parameters:
            return JsonResponse(status=405, data={'response': 'ParameterError: parameter "fid" required'})
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = parameters.get('fid')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})
        user = User.objects.get(user_fid=fid)
        if user is None:
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})

        recipe_desc = parameters.get('desc')
        recipe_user = user
        recipe_name = parameters.get('title')
        recipe_ingredients = parameters.get('ingredients')
        ingredients = ast.literal_eval(parameters.get('ingredients'))
        recipe_sys_tags = allergens(str(ingredients))
        recipe_tags = parameters.get('tags')
        vals = parameters.get('image').split('/o/images/')
        recipe_img = vals[0] + "/o/images%2F" + vals[1]
        recipe = Recipe(recipe_desc=recipe_desc, recipe_user=recipe_user,
                        recipe_name=recipe_name, recipe_ingredients=recipe_ingredients,
                        recipe_sys_tags=recipe_sys_tags, recipe_tags=recipe_tags, recipe_img=recipe_img)
        recipe.save()
        return JsonResponse(status=200, data={'response': 'Created recipe'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})


@csrf_exempt
def get_recipes_by_id(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be GET'})
    if 'recipe_id' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "recipe_id" required'})
    
    try:
        recipe = Recipe.objects.filter(recipe_id=int(request.GET.get('recipe_id')))
        return JsonResponse(status=200, data={'response': serializers.serialize('json', recipe)})
    except Exception as e:
        print(e)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})


@csrf_exempt
def get_recipes(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be GET'})
    if 'token' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "token" required'})

    # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
    fid = request.GET.get('token')
    if fid is None:
        return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})
    user = User.objects.get(user_fid=fid)
    if user is None:
        return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})

    recipes = Recipe.objects.filter(recipe_user=user.user_id)

    return JsonResponse(status=200, data={'response': serializers.serialize('json', recipes)})


@csrf_exempt
def delete_recipe(request):
    if request.method != 'POST':
        return JsonResponse(status=400, data={'response': 'not POST request'})

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    try:
        if 'token' not in parameters:
            return JsonResponse(status=405, data={'response': 'TokenError: invalid token'})
        if 'recipe_id' not in parameters:
            return JsonResponse(status=405, data={'response': 'recipe_id not found'})
        
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = parameters.get('token')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})


        user = User.objects.get(user_fid=fid)
        try:
            recipe = Recipe.objects.get(recipe_user=user.user_id, recipe_id=parameters.get('recipe_id'))
            recipe.delete()
        except:
            return JsonResponse(status=404, data={'response': 'Could not find recipe'})

        return JsonResponse(status=200, data={'response': 'Recipe deleted'})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})

@csrf_exempt
def create_event(request):
    if request.method != 'POST':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be POST'})
    if 'token' not in parameters:
        return JsonResponse(status=405, data={'response', 'ParameterError: parameter "token" required'})
    if 'title' not in parameters:
        return JsonResponse(status=405, data={'response', 'ParameterError: parameter "title" required'})
    if 'desc' not in parameters:
        return JsonResponse(status=405, data={'response', 'ParameterError: parameter "desc" required'})
    if 'location' not in parameters:
        return JsonResponse(status=405, data={'response', 'ParameterError: parameter "location" required'})
    if 'time' not in parameters:
        return JsonResponse(status=405, data={'response', 'ParameterError: parameter "time" required'})

    try:
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = parameters.get('token')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})
        user = User.objects.get(user_fid=fid)
        if user is None:
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})
        
        date_time = datetime.datetime.fromtimestamp(int(parameters.get('time'))/1000)
        date = date_time.date()
        time = date_time.time()

        event = Event(event_desc=parameters.get('desc'), event_location=parameters.get('location'),
                    event_host=user, event_time=time, event_date=date, event_name=parameters.get('title'))
        event.save()
        return JsonResponse(status=200, data={'response': 'Saved Event'})

    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})


@csrf_exempt
def get_user_id(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response': 'TypeError: request type must be GET'})

    if 'id' not in requests.GET:
        return JsonResponse(status=405, data={'response', 'ParameterError: parameter "id" required'})

    user = User.object.get(user_id=request.GET.get('id'))
    return JsonResponse(status=200, data={'response': user})

@csrf_exempt
def get_average_review(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be GET'})

    if 'fid' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "fid" required'})

    try:
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = request.GET.get('fid')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})
        user = User.objects.get(user_fid=fid)
        if user is None:
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})

        review = Review.objects.filter(review_receiver=user)
        count = len(list(review))
        sum_reviews = review.aggregate(Sum('review_rating'))
        if count == 0:
            return JsonResponse(status=200, data={'response': 5})
        avg = sum_reviews['review_rating__sum'] / count
        return JsonResponse(status=200, data={'response': avg})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})

@csrf_exempt
def get_reviews(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response', 'TypeError: request type must be POST'})
    try:
        if 'token' in request.GET:
            # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
            fid = parameters.get('token')
            if fid is None:
                return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})
            user = User.objects.get(user_fid=fid)
            if user is None:
                return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})

            reviews = Review.objects.filter(review_receiver=user)
            return JsonResponse(status=200, data={'response': serializers.serialize('json', reviews)})
        elif 'uname' in request.GET:
            user = User.objects.get(user_uname=request.GET.get('uname'))
            if user is None:
                return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})
            reviews = Review.objects.filter(review_receiver=user)
            return JsonResponse(status=200, data={'response': serializers.serialize('json', reviews)})
        else:
            return JsonResponse(status=405, data={'response', 'ParameterError: Missing parameter, "token" or "uname" expected'})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})

@csrf_exempt
def create_review(request):
    if request.method != 'POST':
        return JsonResponse(status=404, data={'response': 'TypeError: request type must be POST'})

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    if 'fid' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "fid" required'})
    if 'description' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "description" required'})
    if 'rating' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "rating" required'})
    if 'post_id' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "post_id" required'})

    try:
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = parameters.get('fid')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})
        user = User.objects.get(user_fid=fid)
        if user is None:
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})

        post = Post.objects.get(post_id=int(parameters.get('post_id')))
        if post.post_consumer.user_fid != fid:
            return JsonResponse(status=404, data={'response': 'PermissionError: User unauthorized'})

        review_receiver = Post.objects.get(post_id=int(parameters.get('post_id'))).post_recipe.recipe_user
        review = Review(review_desc=parameters.get('description'), review_giver=user,
                        review_receiver=review_receiver,
                        review_recipe=Post.objects.get(post_id=int(parameters.get('post_id'))).post_recipe,
                        review_rating=float(parameters.get('rating')), review_post=post)
        review.save()
        return JsonResponse(status=200, data={'response': 'Saved review'})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})

@csrf_exempt
def post_get_all(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be GET'})
    try:
        posts = Post.objects.all()
        return JsonResponse(status=200, data={'response': serializers.serialize('json', posts)})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response':'ServerError: an unknown error occured'})

@csrf_exempt
def post_get_by_loc(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response': 'request method must be GET'})
    if 'city' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "city" required'})
    if 'state' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "state" required'})
    try:
        posts = []
        for user in User.objects.filter(user_city=request.GET.get('city'), user_state=request.GET.get('state')):
            posts.extend(Post.objects.filter(post_producer=user))
        
        return JsonResponse(status=200, data={'response': serializers.serialize('json', posts)})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response' : 'could not create post ' + str(E)})


@csrf_exempt
def post_sort(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be GET'})
    if 'token' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "token" required'})
    if 'filter' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "filter" required'})
    try:
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = request.GET.get('token')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})
        user = User.objects.get(user_fid=fid)
        if user is None:
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})

        post_filter = request.GET.get('filter')

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
            return JsonResponse(status=404,
                data={'response': 'ParameterError: invalid filter, expected "open", "producer-closed", or "consumer-closed"'})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})


@csrf_exempt
def post_create(request):
    if request.method != 'POST':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be POST'})

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET
    
    if 'token' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "token" required'})
    if 'recipe' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "recipe" required'})

    try:
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = parameters.get('token')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})
        user = User.objects.get(user_fid=fid)
        if user is None:
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})

        # seperating into diff lines so bugfixing (finding what is where) is easier

        title = parameters.get('title', 'none')
        desc = parameters.get('desc', 'none')
        created = timezone.now()
        recipe = Recipe.objects.get(recipe_id=int(parameters.get('recipe')))

        post = Post(post_title=title, post_desc=desc,
                    post_producer=user, post_created=created,
                    post_recipe=recipe, post_available=True, post_consumer=None)
        post.save()
        return JsonResponse(status=200, data={'response': 'Post created'})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})

@csrf_exempt
def post_consumer_closed(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be GET'})
    if 'token' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "token" required'})

    # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
    fid = parameters.get('token')
    if fid is None:
        return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})
    user = User.objects.get(user_fid=fid)
    if user is None:
        return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})

    posts = Post.objects.filter(post_consumer=user);
    return JsonResponse(status=200, data={'response': serializers.serialize('json', posts)})


@csrf_exempt
def post_update(request):
    if request.method != 'POST':
            return JsonResponse(status=404, data={'response': 'request method must be POST'})
    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    if 'token' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "token" required'})
    if 'post-id' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "post-id" required'})
    try:
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = parameters.get('token')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        post_id = int(parameters.get('post-id'))
        post = Post.objects.get(post_id=post_id)
        if post is None:
            return JsonResponse(status=404, data={'response': 'unable to find post with matching id'})

        if fid != post.post_producer.user_fid:
            return JsonResponse(status=404, data={'response': 'unauthorized: invalid fid'})

        title = parameters.get('title', '')
        desc = parameters.get('desc', '')
        recipe_id = parameters.get('recipe', '-1')

        if 'title' in parameters:
            post.post_title = title

        if 'desc' in parameters:
            post.post_desc = desc

        if 'recipe' in parameters:
            recipe = Recipe.objects.get(recipe_id=int(recipe_id))

            if recipe is None:
                return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})

            post.post_recipe = recipe

        post.save()
        return JsonResponse(status=200, data={'response': 'Post updated'})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})


@csrf_exempt
def post_close(request):
    if request.method != 'POST':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be POST'})

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    if 'token' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "token" required'})
    if 'post-id' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "post-id" required'})
    if "uname" not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "uname" required'})
    try:
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = parameters.get('token')

        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})

        post = Post.objects.get(pk=int(parameters.get('post-id')))

        if not post.post_available:
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})

        if post.post_producer.user_fid != fid:
            return JsonResponse(status=404, data={'response': 'AuthorizationError: user unauthorized'})

        user = User.objects.get(user_fid=fid)
        if user is None: 
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})
        
        consumer_user = User.objects.get(user_uname=parameters.get("uname"))
        if consumer_user is None:
            return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})
        
        post.post_consumer = consumer_user;
        post.post_available = False
        post.post_completed = timezone.now()
        post.save()

        return JsonResponse(status=200, data={'response': 'Post set to closed'})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})


@csrf_exempt
def post_delete(request):
    if request.method != 'POST':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be POST'})

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    if 'token' not in parameters:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "token" required'})
    if 'post-id' not in parameters:
            return JsonResponse(status=405, data={'response': 'ParameterError: parameter "post-id" required'})
    try:
        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = parameters.get('token')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})

        post = Post.objects.get(post_id=int(parameters.get('post-id')))

        if post.post_producer.user_fid != fid:
            return JsonResponse(status=404, data={'response': 'AuthorizationError: user unauthorized'})

        post.delete()
        return JsonResponse(status=200, data={'response': 'Deleted Post'})
    except Exception as E:
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})


@csrf_exempt
def user_by_uname(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be GET'})
    if 'uname' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "uname" required'})

    user = User.objects.filter(user_uname__exact=request.GET.get('uname'))
    if len(list(user)) != 0:
        return JsonResponse(status=200, data={'data': serializers.serialize('json', user)})
    return JsonResponse(status=404, data={'response': 'uname does not exist'})


@csrf_exempt
def user_by_id(request):
    if request.method != 'GET':
        return JsonResponse(status=400, data={'response': 'TypeError: request type must be GET'})
    if 'id' not in request.GET:
        return JsonResponse(status=405, data={'response': 'ParameterError: parameter "id" required'})

    try:
        user = User.objects.filter(user_id=int(request.GET.get('id')))
        if len(list(user)) != 0:
            return JsonResponse(status=200, data={'data': serializers.serialize('json', user)})
        return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid'})
    except: 
        print(E)
    return JsonResponse(status=500, data={'response': 'ServerError: an unknown error occured'})

@csrf_exempt
def user_manager(request):
    if request.method == 'GET':
        # return JsonResponse(data={'status': '200', 'user': serializers.serialize('json', User.objects.all())}, safe=False)
        if 'fid' not in request.GET:
            return JsonResponse(status=404, data={'response': 'TypeError: request type must be GET'})

        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = request.GET.get('fid')

        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})

        user = User.objects.filter(user_fid__exact=fid).only('user_uname', 'user_city', 'user_state', 'user_bio')

        if user is None:
            return JsonResponse(status=404, data={'response': "Error: could not find user"})

        return JsonResponse(status=200, data={'user': serializers.serialize('json', user)}, safe=False)
    if request.method == 'POST':
        
        parameters = request.POST
        if len(request.POST) == 0:
            parameters = request.GET

        if 'fid' not in parameters:
            return JsonResponse(status=405, data={'response': 'ParameterError: parameter "fid" required'})
        if 'type' not in parameters:
            return JsonResponse(status=405, data={'response': 'ParameterError: parameter "type" required'})

        # TEST ONLY! VALIDATE TOKEN FOR OFFICIAL USE
        fid = parameters.get('fid')
        if fid is None:
            return JsonResponse(status=404, data={'response': 'TokenError: invalid token'})

        if parameters.get('type') == "Create":
            # new user
            if 'uname' not in parameters:
                return JsonResponse(status=405, data={'response': 'ParameterError: parameter "uname" required'})
            
            username = parameters.get('uname')

            if len(list(User.objects.filter(user_fid=fid))) != 0:
                return JsonResponse(status=404, data={'response': 'DatabaseError: fid already in use'})

            if len(list(User.objects.filter(user_uname=username))) != 0:
                return JsonResponse(status=404, data={'response': 'DatabaseError: username already in use'})

            user = User(user_fid=fid, user_uname=username)
            user.save()
            return JsonResponse(status=200, data={ 'data': 'Created user'})

        elif parameters.get('type') == "Change":  # change to id email or password
            uid = validate_token(parameters.get('fid'))

            if uid is None:
                return JsonResponse(status=404, data={'response': "TokenError: invalid token"})

            user = User.objects.get(user_fid=uid)

            if user is None:
                return JsonResponse(status=404, data={'response': 'DatabaseError: no user matching that fid' })
            
            if 'uname' in parameters:
                if len(list(User.objects.filter(user_uname=parameters.get('uname')))) == 0:
                    user.user_uname = parameters.get('uname')
                else:
                    if (User.objects.get(user_uname=parameters.get('uname')) != user):
                        return JsonResponse(status=404, data={'response': 'DatabaseError: username already in use'})

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