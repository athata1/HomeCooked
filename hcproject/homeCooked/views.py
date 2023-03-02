from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .reviews import *
# import datetime
# import sqlite3
import json
import requests
from firebase_admin import credentials, auth
import ast


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

        uid = validate_token(request.GET.get('fid'))

        if uid is None:
            return JsonResponse(data={'status': '400', 'message': 'Error invalid token'})

        user = User.objects.filter(user_fid=uid)
        if len(list(user)) == 0:
            return JsonResponse(data={'status': '400', 'message': 'Error: User does not exist'})
        user.delete()
        return JsonResponse(data={'status': '200', 'message': 'Deleted User'})
    return JsonResponse(data={'status': '400', 'message': 'Error not POST request'})


def index(request):
    user = User.objects.all

    use = {
        "username": user
    }
    return render(request, "homeCooked\index.html", use)


def post_request(request):
    posts = Post.objects.all()

    context = {
        "post_list": posts
    }
    return render(request, "homeCooked\posts.html", context)

@csrf_exempt
def review_manager(request):
    if request.method == 'GET':
        return JsonResponse({'status':'200', 'reviews':serializers.serialize('json', get_all_reviews())})
    if request.method == 'POST':
        user_id = request.GET['userid']
        post_id = request.GET['postid']
        rating = request.GET['rating']
        desc = request.GET['desc']

        review = None
        try:
            review = create_review(giver=user_id, post_id=post_id, rating=rating, desc=desc)
            review.save()
            return JsonResponse(data={'status': '200', 'response': 'Created review'})
        except ValueError:
            return JsonResponse(data={'status':'400', 'message':'Error: missing/invalid parameters'})
        except RuntimeError:
            return JsonResponse(data={'status':'500', 'message':'Error: review creation failed for unknown reason'})

@csrf_exempt
def create_review(request):
    user_id = request.GET.get('userid')
    post_id = request.GET.get('postid')
    rating = request.GET.get('rating')
    desc = request.GET.get('desc')

    review = None
    try:
        review = Review(review_giver=user_id, review_post=post_id, review_rating=rating, review_desc=desc)
        review.save()
        return JsonResponse(data={'status': '200', 'response': 'Created review'})
    except ValueError:
        return JsonResponse(data={'status':'400', 'message':'Error: missing/invalid parameters'})
    except RuntimeError:
        return JsonResponse(data={'status':'500', 'message':'Error: review creation failed for unknown reason'})

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
        return JsonResponse(data={'status': '404', 'response': 'Not post request'})
    #return JsonResponse(serializers.serialize('json', Recipe.objects.all()), safe=False)

    if 'token' not in request.GET:
            return JsonResponse(data={'status': '404', 'response': 'token not in parameters'})
    fid = validate_token(request.GET.get('token'))
    if fid is None:
        return JsonResponse(data={'status': '404', 'response': 'invalid token'})

    user = User.objects.get(user_fid=fid)

    recipe_desc = request.GET.get('desc')
    recipe_user = user
    recipe_name = request.GET.get('title')
    recipe_ingredients = request.GET.get('ingredients')
    ingredients = ast.literal_eval(request.GET.get('ingredients'))
    recipe_sys_tags = allergens(str(ingredients))
    recipe_tags = request.GET.get('tags')
    recipe_img = request.GET.get('image')
    recipe = Recipe(recipe_desc=recipe_desc, recipe_user=recipe_user,
                    recipe_name=recipe_name, recipe_ingredients=recipe_ingredients,
                    recipe_sys_tags=recipe_sys_tags, recipe_tags=recipe_tags, recipe_img=recipe_img)
    recipe.save()
    return JsonResponse(data={'status': '200', 'response': 'Created recipe'})

@csrf_exempt
def get_recipes_by_id(request):
    if request.method != 'GET':
        return JsonResponse(data={'status': '404', 'response': 'not GET request'})

    if 'recipe_id' not in request.GET:
        return JsonResponse(data={'status': '404', 'response': 'No recipe_ud in parameters'})

    try:
        recipe = Recipe.objects.filter(recipe_id=int(request.GET.get('recipe_id')))
        if (len(list(recipe)) != 1):
            return JsonResponse(data={'status': '404', 'response': 'Could not find recipe'})
        return JsonResponse(data={'status':200, 'response':serializers.serialize('json', recipe)}, safe=False)
    except Exception as e:
        print(e)




@csrf_exempt
def get_recipes(request):
    if request.method != 'GET':
        return JsonResponse(data={'status': '404', 'response': 'not GET request'})
    if 'token' not in request.GET:
        return JsonResponse(data={'status': '404', 'response': 'token not in parameters'})
    fid = validate_token(request.GET.get('token'))
    if fid is None:
        return JsonResponse(data={'status': '404', 'response': 'invalid token'})

    user = User.objects.get(user_fid=fid)
    recipes = Recipe.objects.filter(recipe_user=user.user_id)
    return JsonResponse(serializers.serialize('json', recipes), safe=False)

@csrf_exempt
def delete_recipe(request):
    if request.method != 'POST':
        return JsonResponse(data={'status': '404', 'response': 'not POST request'})

    if 'token' not in request.GET:
        return JsonResponse(data={'status': '404', 'response': 'token not in parameters'})
    fid = validate_token(request.GET.get('token'))
    if fid is None:
        return JsonResponse(data={'status': '404', 'response': 'invalid token'})

    if 'recipe_id' not in request.GET:
        return JsonResponse(data={'status': '404', 'response': 'recipe_id not found'})

    user = User.objects.get(user_fid=fid)
    try:
        recipe = Recipe.objects.get(recipe_user=user.user_id, recipe_id=request.GET.get('recipe_id'))
        recipe.delete()
    except:
        return JsonResponse(data={'status': '404', 'response': 'Could not find recipe'})

    return JsonResponse(data={'status': '200', 'response': 'Recipe deleted'})


@csrf_exempt
def delete_post(request):
    if request.method != 'POST':
        return JsonResponse(data={'status': '404', 'response': 'Not Post request'})

    if 'token' not in request.GET:
        return JsonResponse(data={'status': '404', 'response': 'token not in parameters'})
    fid = validate_token(request.GET.get('token'))
    if fid is None:
        return JsonResponse(data={'status': '404', 'response': 'invalid token'})

    user = User.objects.get(user_fid=fid)
    if 'post_id' not in request.GET:
        return JsonResponse(data={'status': '404', 'response': 'No post_id in parameters'})
    try:
        post = Post.objects.get(post_id=request.GET.get('post_id'))
        post.delete()
        if post.post_producer != user.user_id:
            return JsonResponse(data={'status': '404', 'response': 'You do not have permission to delete this post'})
    except Exception as e:
        print(e)
        return JsonResponse(data={'status': '404', 'response': 'Could not delete post'})

@csrf_exempt
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
        if 'token' not in request.GET:
            return JsonResponse(data={'status': '404', 'response': 'token not in parameters'})
        fid = validate_token(request.GET.get('token'))
        if fid is None:
            return JsonResponse(data={'status': '404', 'response': 'invalid token'})

        if 'type' not in request.GET:
            return JsonResponse(data={'status': '404', 'response': 'type not in parameters'})

        user = User.objects.get(user_fid=fid)

        if request.GET.get('type') == 'open':
            posts = Post.objects.filter(post_producer=user.user_id, post_available=True)
            return JsonResponse(serializers.serialize('json', posts), safe=False)
        elif request.GET.get('type') == 'producer_closed':
            posts = Post.objects.filter(post_producer=user.user_id, post_available=False)
            return JsonResponse(serializers.serialize('json', posts), safe=False)
        elif request.GET.get('type') == 'consumer_closed':
            posts = Post.objects.filter(post_consumer=user.user_id, post_available=False)
            return JsonResponse(serializers.serialize('json', posts), safe=False)
        else:
            return JsonResponse({'status': '404', 'message': 'Error: Invalid type'}, safe=False)

    elif request.method == 'POST':
        post = None

        if 'token' not in request.GET:
            return JsonResponse(data={'status': '404', 'response': 'token not in parameters'})
        fid = validate_token(request.GET.get('token'))
        if fid is None:
            return JsonResponse(data={'status': '404', 'response': 'invalid token'})

        if 'type' not in request.GET:
            return JsonResponse(data={'status': '404', 'response': 'type not in parameters'})

        user = User.objects.get(user_fid=fid)

        if request.GET.get('type') == 'Create':
            post_title = ''
            post_desc = ''
            post_producer = user
            post_created = datetime.now()
            recipe = Recipe.objects.get(recipe_id=request.GET.get('recipe'))
            post_recipe = recipe
            post_available = True
            post = Post(post_title=post_title, post_desc=post_desc,
                        post_producer=post_producer, post_created=post_created,
                        post_recipe=post_recipe, post_available=post_available, post_consumer=None)
            post.save()
            return JsonResponse(data={'status': '200', 'response': 'Post created for user'})
        return JsonResponse(data={'status': '404', 'response': 'type does not exist'})


@csrf_exempt
def user_by_uname(request):
    if request.method == 'GET':
        if 'uname' not in request.GET:
            return JsonResponse(data={'status': '405', 'response': 'missing uname in parameter'})

        user = User.objects.filter(user_uname__exact=request.GET.get('uname'))
        if len(list(user)) != 0:
            return JsonResponse({'status': '200', 'data': serializers.serialize('json', user)}, safe=False)
        return JsonResponse(data={'status': '404', 'response': 'uname does not exist'})
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
        # return JsonResponse(data={'status': '200', 'user': serializers.serialize('json', User.objects.all())}, safe=False)
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

            return JsonResponse({'status': 200, 'data': 'Created user'}, safe=False)
        elif request.GET.get('type') == "Change":  # change to id email or password

            uid = validate_token(request.GET.get('fid'))

            if uid is None:
                return JsonResponse(data={'status': '404', 'message': "Error: invalid token"})

            user = User.objects.filter(user_fid__exact=uid)[0]
            if 'uname' in request.GET:
                if user.user_fid == uid and request.GET.get('uname') != user.user_uname:
                    if 'uname' in request.GET and len(
                            list(User.objects.filter(user_uname__exact=request.GET.get('uname')))) == 0:
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
            if 'image' in request.GET:
                user.image_text = request.GET.get('image')
            user.save()

            return JsonResponse(data={'status': '200', 'message': 'Saved data'}, safe=False)
