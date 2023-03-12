from django.test import TestCase, Client
from django.core import serializers
from django.utils import timezone
from .models import *

class PostTestCase(TestCase):
    def test_post(self):
        print("\ntesting json responses searching for posts\n")
        user = User.objects.filter(user_fid="k4zYLfDW2dROxxgRF0FvsJXWXU83").first()
        if user is None:
            user = User(user_fid="k4zYLfDW2dROxxgRF0FvsJXWXU83", user_uname="sampleUser", 
            user_address="1060 W Addison St", user_city="Chicago", user_state="Illinois", # wrigley field
            user_bio="a fake person")
            user.save()
        
        recipe = Recipe.objects.filter(recipe_user=user).first()
        if recipe is None:
            recipe = Recipe.objects.create(recipe_user=user, recipe_name="a recipe", recipe_ingredients="stuff and things",
            recipe_img="https://imgur.com/71HOrWu", recipe_desc="a fake recipe that is deff not real.")
            recipe.save()

        print("setup done, user, recipe, post all found or created")
        
        #post = Post.objects.filter(post_producer=user, post_available=True).first()
        #if post is None:
        #    post = Post.objects.create(post_producer=user, post_consumer=user, post_recipe=recipe, post_title="a new available sample post", post_desc="a random description", post_available=True)
        #    post.save()
        c = Client()

        response = c.post('/posts/create', {'fid':'k4zYLfDW2dROxxgRF0FvsJXWXU83', 'recipe':recipe.recipe_id,
                                            'title':'a sample post', 'desc':'a random description'})
        if response.status_code != 200:
            print("error with fetching post, test failed")
        else:
            print("Success! got response:")

        print(response.json())
        
        print("\nfinding open posts from sampleuser:")

       
        response = c.get('/posts/sort', {'filter':'open', 'fid':"k4zYLfDW2dROxxgRF0FvsJXWXU83"})
        if response.status_code != 200:
            print("error with fetching post, test failed")
        else:
            print("Success! got response:")

        print(response.json())
        
        print("\nclosing post")
        response = c.post('/posts/close', {'fid':'k4zYLfDW2dROxxgRF0FvsJXWXU83', 'post-id':1})
        if response.status_code != 200:
            print("error with fetching post, test failed")
        else:
            print("Success! got response:")

        print(response.json())

        print("\nfinding closed posts bought by sample user")
        response = c.get('/posts/sort', {'filter':'consumer-closed', 'fid':"k4zYLfDW2dROxxgRF0FvsJXWXU83"})
        if response.status_code != 200:
            print("error with fetching post, test failed")
        else:
            print("Success! got response:")
        print(response.json())

        print("\nfinding closed posts produced by sample user")
        response = c.get('/posts/sort', {'filter':'producer-closed', 'fid':"k4zYLfDW2dROxxgRF0FvsJXWXU83"})
        if response.status_code != 200:
            print("error with fetching post, test failed")
        else:
            print("Success! got response:")
        print(response.json())
    
        new_recipe = Recipe.objects.create(recipe_user=user, recipe_name="a recipe", recipe_ingredients="stuff and things",
            recipe_img="https://imgur.com/71HOrWu", recipe_desc="a fake recipe that is deff not real.")
        new_recipe.save()
        print("\nnew recipe created: id = " + str(new_recipe.recipe_id))

        print("\nupdating post")
        response = c.post('/posts/update', {'fid':user.user_fid, 'post-id':1, 'title':'new title', 'desc':'a new description', 'recipe':new_recipe.recipe_id})
        if response.status_code != 200:
            print("error with updating post, test failed")
        else:
            print("Success! got response:")
        print(response.json())
        print('new post is:')
        print(c.get('/posts/sort', {'filter':'producer-closed', 'fid':"k4zYLfDW2dROxxgRF0FvsJXWXU83"}).json()['response'])
    
        print('\ndeleting post')
        response = c.post('/posts/delete', {'fid':"k4zYLfDW2dROxxgRF0FvsJXWXU83", 'post-id':1})
        if response.status_code != 200:
            print("error with fetching post, test failed")
        else:
            print("Success! got response:")
        print(response.json())