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
    if request.method == 'POST':

        if 'fid' not in request.GET:
            return JsonResponse(status=404, data={'response': 'token not in parameters'})
        uid = validate_token(request.GET.get('fid'))
        print(uid)

        user = User.objects.filter(user_fid=uid)
        if len(list(user)) == 0:
            return JsonResponse(status=400, data={'response':'Error: User does not exist'})
        user.delete()
        return JsonResponse(status=200, data={'response':'Deleted User'})
    return JsonResponse(status=500, data= {'response':'Error: request type must be POST'})


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
    #return JsonResponse(serializers.serialize('json', Recipe.objects.all()), safe=False)

    if 'fid' not in request.GET:
            return JsonResponse(status=404, data={'response':'token not in parameters'})
    fid = validate_token(request.GET.get('fid'))

    if fid is None:
        return JsonResponse(status=404, data={'response':'invalid token'})

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
    return JsonResponse(status=200, data={'response':'Created recipe'})

@csrf_exempt
def get_recipes_by_id(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response':'not GET request'})

    if 'recipe_id' not in request.GET:
        return JsonResponse(status=404, data={'response':'No recipe_ud in parameters'})
    try:
        recipe = Recipe.objects.filter(recipe_id=int(request.GET.get('recipe_id')))
        return JsonResponse(status=200, data={'response':serializers.serialize('json', recipe)})
    except Exception as e:
        print(e)
    return JsonResponse(status=404, data={'response':'Error Occured'})


@csrf_exempt
def get_recipes(request):
    if request.method != 'GET':
        return JsonResponse(status=404, data={'response':'not GET request'})
    if 'token' not in request.GET:
        return JsonResponse(status=404, data={'response':'token not in parameters'})

    fid = validate_token(request.GET.get('token'))
    if fid is None:
        return JsonResponse(status=404, data={'response':'invalid token'})

    user = User.objects.get(user_fid=fid)
    recipes = Recipe.objects.filter(recipe_user=user.user_id)

    return JsonResponse(status=200, data={'response':serializers.serialize('json', recipes)})


@csrf_exempt
def delete_recipe(request):
    if request.method != 'POST':
        return JsonResponse(status=404, data={'response':'not POST request'})

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
    avg = sum_reviews['review_rating__sum']/count
    print(avg)
    return JsonResponse(status=200, data={'response': avg})


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

    post=Post.objects.get(post_id=int(request.GET.get('post_id')))
    review_receiver = Post.objects.get(post_id=int(request.GET.get('post_id'))).post_recipe.recipe_user

    review = Review(review_desc=request.GET.get('description'), review_giver=user,
                    review_receiver=review_receiver, review_recipe=Post.objects.get(post_id=int(request.GET.get('post_id'))).post_recipe,
                    review_rating=request.GET.get('rating'), review_post=post)
    review.save()
    return JsonResponse(status=200, data={'response': 'Saved review'})


@csrf_exempt
def post_sort(request):
    try:
        if request.method != 'GET':
            return JsonResponse(status=404, data={'request':'request method is not GET'})

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
            return JsonResponse(status=404, data={'response':'invalid token'})


        if post_filter == 'open':
            posts = Post.objects.filter(post_producer=user.user_id, post_available=True)
            return JsonResponse(status=200, data={'response':serializers.serialize('json', posts)})
        elif post_filter == 'producer-closed':
            posts = Post.objects.filter(post_producer=user.user_id, post_available=False)
            return JsonResponse(status=200, data={'response':serializers.serialize('json', posts)})
        elif post_filter == 'consumer-closed':
            posts = Post.objects.filter(post_consumer=user.user_id, post_available=False)
            return JsonResponse(status=200, data={'response':serializers.serialize('json', posts)})
        else:
            return JsonResponse(status=404, data={'response': 'ValueError: filter (open, producer_closed, consumer_closed) missing or invalid'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response':'could not get post(s) ' + str(E)})


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
            return JsonResponse(status=400, data={'response':'invalid token'})

        #seperating into diff lines so bugfixing (finding what is where) is easier

        title = parameters.get('title', 'none')
        desc = parameters.get('desc', 'none')
        created = timezone.now()


        recipe = Recipe.objects.get(recipe_id=int(parameters.get('recipe', '-1')))
        
        if recipe is None:
            return JsonResponse(status=400, data={'response':'invalid recipe id'})

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

        if 'token' not in parameters:
            return JsonResponse(status=405, data={'response':'error, token required to update post'})

        fid=validate_token(parameters['token'])
        post_id = int(parameters.get('post-id', '-1'))

        if post_id < 0:
            return JsonResponse(status=404, data={'response':'missing/invalid post id'})        

        post = Post.objects.get(post_id = post_id)

        if post is None:
            return JsonResponse(status=404, data={'response':'unable to find post with matching id'})

        if fid != post.post_producer.user_fid:
            return JsonResponse(status=404, data={'response':'unauthorized: invalid fid'})

        title = parameters.get('title', '')
        desc = parameters.get('desc', '')
        recipe_id = parameters.get('recipe', '-1')

        if title != "":
            post.post_title = title

        if desc != "":
            post.post_desc = desc

        if int(recipe_id) > 0:
            recipe = Recipe.objects.get(recipe_id = int(recipe_id))

            if recipe is None:
                return JsonResponse(status=404, data={'response':'unable to find recipe with matching id'})

            post.post_recipe = recipe

        post.save()

        return JsonResponse(status=200, data={'response': 'Post updated'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response' : 'could not update post ' + str(E)})


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

        post = Post.objects.get(post_id=int(parameters.get('post-id', '-1')))
        if not post.post_available:
            return JsonResponse(status=404, data={'response': 'Error: post already closed'})
        user = User.objects.get(user_fid=fid)
        
        if post.post_producer.user_id != user.user_id:
            return JsonResponse(status=404, data={'response': 'You do not have permission to do this'})
        
        if user is None:
            return JsonResponse(status=404, data={'response': 'no user with that fid'})

        post.post_consumer = user
        post.post_available = False
        post.post_completed = timezone.now()
        post.save()
        
        return JsonResponse(status=200, data={'response': 'Post set to closed'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response' : 'could not close post ' + str(E)})


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

        user = User.objects.get(user_fid=fid)
        
        if 'post-id' not in parameters:
            return JsonResponse(status=404, data={'response': 'No post_id in parameters'})
        
        post = Post.objects.get(post_id=int(parameters.get('post-id')))
        post.delete()

        if post.post_producer.user_id != user.user_id:
            return JsonResponse(status=404, data={'response': 'You do not have permission to delete this post'})
        else:
            return JsonResponse(status=200, data={'response': 'Deleted Post'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response' : 'could not delete post: ' + str(E)})


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
def user_create(request):
    try:
        if request.method != 'POST':
            return JsonResponse(status=404, data={'response': 'request method must be POST'})
        if 'token' not in request.GET:
            return JsonResponse(status=405, data={'response': 'missing parameter: token'})

        fid = validate_token(request.GET.get('token'))

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        if User.objects.filter(user_fid=fid).exists():
            return JsonResponse(status=404, data={'response': 'fid already in use'})


        username = request.GET.get('uname')
        
        if username is None:
            return JsonResponse(status=400, data={'response':'invalid username'})
        if User.objects.filter(user_uname=username).exists():
            return JsonResponse(status=404, data={'response': 'username already in use'})

        user = User(user_fid=fid, user_uname=username)
        user.save()

        return JsonResponse(status=200, data={'response': 'User created'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response' : 'could not create user ' + str(E)})    


@csrf_exempt
def user_update(request):
    try:
        if request.method != 'POST':
            return JsonResponse(status=404, data={'response': 'request method must be POST'})
        if 'token' not in request.GET:
            return JsonResponse(status=405, data={'response': 'missing parameter: token'})

        fid = validate_token(request.GET.get('token'))

        if fid is None:
            return JsonResponse(status=404, data={'response': 'invalid token'})

        user = User.objects.get(user_fid=fid)

        if user is None:
            return JsonResponse(status=404, data={'response': 'no user with that fid'})

        #username, address, city, state, bio, image_text
        if 'uname' in request.GET:
            user.user_uname=request.GET.get('uname')
        if 'address' in request.GET:
            user.user_address=request.GET.get('address')
        if 'city' in request.GET:
            user.user_city=request.GET.get('city')
        if 'state' in request.GET:
            user.user_state=request.GET.get('state')
        if 'bio' in request.GET:
            user.user_bio=request.GET.get('bio')
        if 'image' in request.GET:
            user.image_text=request.GET.get('image')

        user.save()

        return JsonResponse(status=200, data={'response': 'User updated'})
    except Exception as E:
        print(E)
        return JsonResponse(status=500, data={'response' : 'could not create user ' + str(E)})  


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

        if len(list(user)) == 0:
            return JsonResponse(status=404, data={'response': "Error: could not find user"})

        return JsonResponse(status=200, data={'user': serializers.serialize('json', user)}, safe=False)
    if request.method == 'POST':
        if 'fid' not in request.GET or 'type' not in request.GET:
            return JsonResponse(status=404, data={'response': "Error: Missing parameters"})

        print(request.GET.get('fid'))
        fid = validate_token(request.GET.get('fid'))

        if fid is None:
            return JsonResponse(status=404, data={'response': "Error: invalid token"})

        if request.GET.get('type') == "Create":
            # new user
            if 'uname' not in request.GET:
                return JsonResponse(status=404, data={'response': "Error:username missing"})

            username = request.GET.get('uname')

            if len(list(User.objects.filter(user_fid__exact=fid))) != 0:
                return JsonResponse(status=404, data={'response': "Error: Account Already created"})

            if len(list(User.objects.filter(user_uname__exact=username))) != 0:
                return JsonResponse(status=404, data={'response': "Error: username already taken"})

            user = User(user_fid=fid, user_uname=username)
            user.save()

            return JsonResponse(status=200, data={ 'data': 'Created user'}, safe=False)
        elif request.GET.get('type') == "Change":  # change to id email or password

            uid = validate_token(request.GET.get('fid'))

            if uid is None:
                return JsonResponse(status=404, data={'response': "Error: invalid token"})

            user = User.objects.filter(user_fid__exact=uid)[0]
            if 'uname' in request.GET:
                if user.user_fid == uid and request.GET.get('uname') != user.user_uname:
                    if 'uname' in request.GET and len(
                            list(User.objects.filter(user_uname__exact=request.GET.get('uname')))) == 0:
                        user.user_uname = request.GET.get('uname')
                    elif len(list(User.objects.filter(user_uname__exact=request.GET.get('uname')))) > 0:
                        return JsonResponse(status=404, data={'response': "Error: username already taken"})

            if 'address' in request.GET:
                user.user_address = request.GET.get('address')
            if 'bio' in request.GET:
                user.user_bio = request.GET.get('bio')
            if 'city' in request.GET:
                user.user_city = request.GET.get('city')
            if 'state' in request.GET:
                user.user_state = request.GET.get('state')
            if 'image' in request.GET:
                vals = request.GET.get('image').split('/o/images/')
                user.image_text = vals[0] + "/o/images%2F" + vals[1]
            user.save()

            return JsonResponse(status=200, data={'response': 'Saved data'}, safe=False)
