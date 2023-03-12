from django.test import TestCase, Client
from django.core import serializers


class PostTestCase(TestCase):
    def setup(self):
        #don't replace if not in systems
        user = User.objects.create(user_fid="k4zYLfDW2dROxxgRF0FvsJXWXU83", user_uname="sampleUser", 
            user_address="1060 W Addison St", user_city="Chicago", user_state="Illinois", # wrigley field
            user_bio="a fake person")
        recipe = Recipe.create(recipe_user=user, recipe_name="a recipe", recipe_ingredients="stuff and things",
            recipe_img="https://imgur.com/71HOrWu", recipe_desc="a fake recipe that is deff not real.")
        
    def test_post_get_and_post(self):
        c = Client()
        response =  c.get('/posts/sort', {'filter':'open', 'fid':"k4zYLfDW2dROxxgRF0FvsJXWXU83"})