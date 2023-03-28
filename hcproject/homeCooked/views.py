from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect
from django.core import serializers
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import *
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
        return JsonResponse(status=404, data={'response': 'request method must be post'})

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    if 'fid' not in parameters:
        return JsonResponse(status=405, data={'response': 'token not in parameters'})

    # TESTING ONLY DO NOT ALLOW IN PROD/MAIN
    uid = parameters.get('fid')

    if uid is None:
        return JsonResponse(status=404, data={'response': 'invalid fid'})

    user = User.objects.get(user_fid=uid)

    if user is None:
        return JsonResponse(status=400, data={'response':'Error: User does not exist'})
    
    user.delete()
    
    return JsonResponse(status=200, data={'response':'Deleted User'})
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
    #print(res.text);
    return res.text


@csrf_exempt
def create_recipe(request):
    if request.method != 'POST':
        return JsonResponse(status=404, data={'response': 'Not post request'})

    parameters = request.POST
    if len(request.POST) == 0:
       parameters = request.GET

    # return JsonResponse(serializers.serialize('json', Recipe.objects.all()), safe=False)

    if 'fid' not in parameters:
        return JsonResponse(status=404, data={'response': 'token not in parameters'})
    
    #TESTING PURPOSES ONLY, VALIDATE TOKEN IN MAIN!!!!!!!!
    fid = parameters.get('fid')

    if fid is None:
        return JsonResponse(status=404, data={'response':'invalid token'})

    user = User.objects.get(user_fid=fid)

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



@csrf_exempt
def get_recipes_by_id(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response': 'not GET request'})

    if 'recipe_id' not in request.GET:
        return JsonResponse(status=404, data={'response': 'No recipe-id in parameters'})
    try:
        recipe_id = int(request.GET.get('recipe_id', '-1'))
        if recipe_id < 0:
            return JsonResponse(status=404, data={'response': 'invalid recipe id'})

        recipe = Recipe.objects.filter(recipe_id=recipe_id)
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

    # TEST PURPOSES ONLY, IF ON MAIN, VALIDATE TOKEN!!!!!!!
    fid = request.GET.get('token')

    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})

    user = User.objects.get(user_fid=fid)
    recipes = Recipe.objects.filter(recipe_user=user.user_id)

    return JsonResponse(status=200, data={'response': serializers.serialize('json', recipes)})


@csrf_exempt
def delete_recipe(request):
    if request.method != 'POST':
        return JsonResponse(status=404, data={'response': 'not POST request'})

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    if 'token' not in parameters:
        return JsonResponse(status=404, data={'response': 'token not in parameters'})
    
    # TESTING PURPOSES ONLY! VALIDATE TOKEN ON MAIN!!!!!!
    fid = parameters.get('token')
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})

    if 'recipe_id' not in parameters:
        return JsonResponse(status=404, data={'response': 'recipe_id not found'})

    user = User.objects.get(user_fid=fid)
    try:
        recipe = Recipe.objects.get(recipe_user=user.user_id, recipe_id=parameters.get('recipe_id'))
        recipe.delete()
    except:
        return JsonResponse(status=404, data={'response': 'Could not find recipe'})

    return JsonResponse(status=200, data={'response': 'Recipe deleted'})


@csrf_exempt
def get_average_review(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response': 'Expected GET request, got POST'})

    if 'fid' not in request.GET:
        return JsonResponse(status=404, data={'response': 'No fid in params'})

    #TEST PURPOSES ONLY!! VALIDATE TOKEN IN MAIN!
    fid = request.GET.get('fid')
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})
    user = User.objects.get(user_fid=fid)

    review = Review.objects.filter(review_receiver=user)
    count = len(list(review))
    sum_reviews = review.aggregate(Sum('review_rating'))
    if count == 0:
        return JsonResponse(status=200, data={'response': 5})
    avg = sum_reviews['review_rating__sum'] / count
    print(avg)
    return JsonResponse(status=200, data={'response': avg})

@csrf_exempt
def get_reviews(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response', "Not a GET request"})

    if 'token' in request.GET:
        #test purposes only! VALIDATE TOKEN IN MAIN!!!!!!!!!!
        fid = request.GET.get('token')
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

    parameters = request.POST
    if len(request.POST) == 0:
        parameters = request.GET

    if 'fid' not in parameters:
        return JsonResponse(status=404, data={'response': 'No fid in params'})

    # TESTING PURPOSES ONLY!! VALIDATE TOKEN ON MAIN!!!!!!!!!!!!
    fid = parameters.get('fid')
    if fid is None:
        return JsonResponse(status=404, data={'response': 'invalid token'})
    user = User.objects.get(user_fid=fid)

    if 'description' not in parameters:
        return JsonResponse(status=404, data={'response': 'No description in params'})

    if 'rating' not in parameters:
        return JsonResponse(status=404, data={'response': 'No rating in params'})

    if 'post_id' not in parameters:
        return JsonResponse(status=404, data={'response': 'No rating in params'})

    post = Post.objects.get(post_id=int(parameters.get('post_id')))
    if post.post_consumer.user_fid != fid:
        return JsonResponse(status=404, data={'response': 'Do not have permission to create review'})

    review_receiver = Post.objects.get(post_id=int(parameters.get('post_id'))).post_recipe.recipe_user

    review = Review(review_desc=parameters.get('description'), review_giver=user,
                    review_receiver=review_receiver,
                    review_recipe=Post.objects.get(post_id=int(parameters.get('post_id'))).post_recipe,
                    review_rating=int(parameters.get('rating')), review_post=post)
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
        if 'zip' not in request.GET:
            return JsonResponse(status=405, data={'response': 'missing parameter zipcode'})
    
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

        fid = request.GET.get('fid')
        if 'token' not in request.GET:
            if fid is None:
                return JsonResponse(status=404, data={'response': 'token/fid not in parameters'})
        else:
            fid = validate_token(request.GET.get('token'))

        post_filter = request.GET.get('filter', 'none')

        if post_filter is None:
            return JsonResponse(status=405, data={'response': 'missing filter'})

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        user = User.objects.get(user_fid=fid)

        if user is None:
            return JsonResponse(status=404, data={'response':'invalid token'})

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

        parameters = request.POST
        if len(request.POST) == 0:
            parameters = request.GET

        # TODO: THIS IS TEST CODE!! 
        # TODO: IT IS NOT TO MAKE IT TO THE MAIN BRANCH!
        # TODO: IF THIS IS IN MAIN, DELETE ANY MENTION OF fid BEFORE fid=validate_token... (and the else statment that's in)
        
        fid = parameters.get('fid')
        if 'token' not in parameters:
            if fid is None:
                return JsonResponse(status=404, data={'response': 'token/fid not in parameters'})
        else:
            fid = validate_token(parameters.get('token'))

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        user = User.objects.get(user_fid=fid)

        if user is None:
            return JsonResponse(status=400, data={'response': 'invalid token'})


        #seperating into diff lines so bugfixing (finding what is where) is easier
        title = parameters.get('title', 'untitled')
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
        return JsonResponse(status=500, data={'response' : 'could not create post ' + str(E)})


@csrf_exempt
def post_update(request):
    try:
        if request.method != 'POST':
            return JsonResponse(status=404, data={'response': 'request method must be POST'})

        parameters = request.POST
        if len(request.POST) == 0:
            parameters = request.GET

        if 'post-id' not in parameters:
            return JsonResponse(status=405, data={'response':'request parameter "post-id" is missing'})

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

        fid = parameters.get('fid')
        if 'token' not in parameters:
            if fid is None:
                return JsonResponse(status=405, data={'response':'request parameter "token" is missing'})
        else:
            fid = validate_token(token);

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        if fid != post.post_producer.user_fid:
            return JsonResponse(status=404, data={'response': 'unauthorized: invalid fid'})

        title = parameters.get('title', '')
        desc = parameters.get('desc', '')
        recipe_id = int(parameters.get('recipe', '-1'))

        if title != "":
            post.post_title = title

        if desc != "":
            post.post_desc = desc

        if recipe_id > 0:
            recipe = Recipe.objects.get(recipe_id = recipe_id)

            if recipe is None:
                return JsonResponse(status=404, data={'response': 'unable to find recipe with matching id'})

            post.post_recipe = recipe

        post.save()

        return JsonResponse(status=200, data={'response': 'Post updated'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response': 'could not update post ' + str(E)})


@csrf_exempt
def post_close(request):
    try:
        if request.method != 'POST':
            return JsonResponse(status=404, data={'response': 'request method must be POST'})
        
        parameters = request.POST
        if len(request.POST) == 0:
            parameters = request.GET

        fid = parameters.get('fid')
        if 'token' not in parameters:
            if fid is None:
                return JsonResponse(status=404, data={'response': 'No token'})
        else:
            fid = validate_token(parameters.get('token'))

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        if 'post-id' not in parameters:
            return JsonResponse(status=404, data={'response': 'No post id'})
        print(parameters.get('post-id'))
        post = Post.objects.get(pk=int(parameters.get('post-id')))

        if not post.post_available:
            return JsonResponse(status=404, data={'response': 'Error: post already closed'})
        
        user = User.objects.get(user_fid=fid)
        if post.post_producer.user_id == user.user_id:
            return JsonResponse(status=404, data={'response': "You can't buy an item you sold"})
        
        if user is None:
            return JsonResponse(status=404, data={'response': 'no user with that fid'})

        post.post_consumer = user;
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
        
        fid = parameters.get('fid')
        if 'token' not in parameters:
            if fid is None:
                return JsonResponse(status=404, data={'response': 'token not in parameters'})
        else:
            fid = validate_token(request.GET.get('token'))
        
        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        user = User.objects.get(user_fid=fid)
        
        if 'post-id' not in parameters:
            return JsonResponse(status=404, data={'response': 'No post_id in parameters'})

        if post.post_producer.user_fid != fid:
            return JsonResponse(status=404, data={'response': 'You do not have permission to delete this post'})
        else:
            post = Post.objects.get(post_id=int(parameters.get('post-id')))
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

        # TEST ONLY!! VALIDATE TOKEN OTHERWISE!!!!!!!
        fid = request.GET.get('fid')

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
        parameters = request.POST
        if len(request.POST) == 0:
            parameters = request.GET


        if 'fid' not in parameters:
            return JsonResponse(status=405, data={'response': "Error: Missing fid"})
        if 'type' not in parameters:
            return JsonResponse(status=405, data={'response': "Error: Missing request type"})

        # TESTING ONLY!! VALIDATE FID OTHERWISE AND USE TOKEN!!!!!!!!!!
        fid = parameters.get('fid')

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

            # testing purposes only!! DO NOT ALLOW IN MAIN/PROD
            uid = parameters.get('fid')

            if uid is None:
                return JsonResponse(status=404, data={'response': "Error: invalid token"})

            user = User.objects.get(user_fid=uid)

            if user is None:
                return JsonResponse(status=404, data={'response': "Error: no user matching that fid"})
            
            if 'uname' in parameters:
                if len(list(User.objects.filter(user_uname=parameters.get('uname')))) == 0:
                    user.user_uname = parameters.get('uname')
                else:
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