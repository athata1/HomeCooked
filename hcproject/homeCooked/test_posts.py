from django.test import TestCase, Client, RequestFactory
from django.core import serializers
from django.utils import timezone
from .models import *

class PostTestCase(TestCase):   
    def setUp(self):
        self.user = User(user_fid="user1", user_uname="sampleUser", 
            user_address="1060 W Addison St", user_city="Chicago", user_state="Illinois", user_zip='60613', # wrigley field
            user_bio="a fake person")
        self.user.save()

        self.recipe = Recipe.objects.create(recipe_user=self.user, recipe_name="a recipe", recipe_ingredients="stuff and things",
            recipe_img="https://imgur.com/71HOrWu", recipe_desc="a fake recipe that is deff not real.")
        self.recipe.save()
        
        self.c = Client()
        self.factory = RequestFactory()

    def test_001_post_a_create_post(self):
        print("\ntest 001")
        print("creating a new post")
        print('expected response: "Post created"')

        response = self.c.post('/posts/create', {
            'fid':self.user.user_fid,
            'recipe':self.recipe.recipe_id,
            'title':'a sample post',
            'desc':'a random description'
            })

        if response.status_code != 200:
            print(" error with fetching post, test failed")
        else:
            print(" Success! got response:")

        print(response.json())


    def test_002_post_sort_open(self):
        print("\ntest 002")
        print("finding open posts from the user:")
        print("expected response: [a post object]")

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title")
        post.save()

        response = self.c.get('/posts/sort', {'filter':'open', 'fid':self.user.user_fid})
        if response.status_code != 200:
            print(" error with fetching post, test failed")
        else:
            print(" Success! got response:")

        print(response.json())

  
    def test_003_post_close_post(self):
        print('\ntest 003')
        print('closing post')
        print('expected response: "Post set to closed"')

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title")
        post.save()

        user2 = User(user_fid="user2", user_uname='sampleUser2',
        user_address="1060 W Addison St", user_city="Chicago", user_state="Illinois", # wrigley field
        user_bio="a fake person")
        user2.save()

        response = self.c.post('/posts/close', {'fid':user2.user_fid, 'post-id':1})
        if response.status_code != 200:
            print(" error with fetching post, test failed")
        else:
            print(" Success! got response:")

        print(response.json())

    def test_004_post_sort_closed_consumer(self):
        print('\ntest 004')
        print("finding closed posts bought by the user:")
        print('expected response: [a post object]')

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title", post_consumer=self.user, post_available=False)
        post.save()

        response = self.c.get('/posts/sort', {'filter':'consumer-closed', 'fid':self.user.user_fid})
        if response.status_code != 200:
            print(" error with fetching post, test failed")
        else:
            print(" Success! Got response:")
        print(response.json())
    
    def test_005_post_sort_closed_producer(self):
        print('\ntest 005')
        print("finding closed posts")
        print('expected response: [a post object]')

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title", post_consumer=self.user, post_available=False)
        post.save()

        response = self.c.get('/posts/sort', {'filter':'producer-closed', 'fid':self.user.user_fid})
        if response.status_code != 200:
            print(" error with fetching post, test failed")
        else:
            print(" Success! got response:")
        print(response.json())


    def test_006_post_update(self):
        print('\ntest 006')
        print("updating post:")
        print('expected response: "Post updated\nnew post is [a post object]"')

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title")
        post.save()

        new_recipe = Recipe.objects.create(recipe_user=self.user, recipe_name="a recipe", recipe_ingredients="stuff and things",
            recipe_img="https://imgur.com/71HOrWu", recipe_desc="a fake recipe that is deff not real.")
        new_recipe.save()

        print("\nnew recipe created: id = " + str(new_recipe.recipe_id))

        response = self.c.post('/posts/update', {'fid':self.user.user_fid, 'post-id':str(post.post_id), 'title':'new title', 'desc':'a new description', 'recipe':new_recipe.recipe_id})
        if response.status_code != 200:
            print("error with updating post, test failed")
        else:
            print("Success! Got response:")
        print(response.json())

        print('new post is:')
        print(self.c.get('/posts/sort', {'filter':'open', 'fid':self.user.user_fid}).json()['response'])
    

    def test_007_post_delete(self):
        print('\ntest 007')
        print('deleting post')
        print('expected response: "Deleted post"')

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title")
        post.save()

        response = self.c.post('/posts/delete', {'fid':self.user.user_fid, 'post-id':1})
        if response.status_code != 200:
            print(" error with fetching post, test failed")
        else:
            print(" Success! Got response:")
        print(response.json())


    def test_008_post_create_empty_fields(self):
        print('\ntest 008')
        print('creating post with empty title and description fields')
        print('expected response: "Post created"')

        response = self.c.post('/posts/create', {
            'fid':self.user.user_fid,
            'recipe':self.recipe.recipe_id,
        })

        if response.status_code != 200:
            print(" error with creating post with empty title and description")
        else:
            print(" Success! You should be able to leave these fields empty")

        print(response.json())
    
    def test_009_post_close_post_as_producer(self):
        print('\ntest 009')
        print("Attempting to close post as producer")
        print('''expected result: "You can't buy an item you sold"''')

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title")
        post.save()

        response = self.c.post('/posts/close', {'fid':self.user.user_fid, 'post-id':1})
        if response.status_code != 404:
            print("Fail! you should not be able to do this!")
        else:
            print(" Success! You can't buy an item you sold!")

        print(response.json())
    
    def test_010_post_delete_post_unauthorized(self):
        print('\ntest 010')
        print("Attempting to delete post as unauthorized user")
        print('''expected response: "You do not have permission to delete this post"''')

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title")
        post.save()

        user2 = User(user_fid="user2", user_uname='sampleUser2',
        user_address="1060 W Addison St", user_city="Chicago", user_state="Illinois", # wrigley field
        user_bio="a fake person")
        user2.save()

        response = self.c.post('/posts/delete', {'fid':user2.user_fid, 'post-id':1})
        if response.status_code != 404:
            print(" error: only the producer should be able to delete posts!")
        else:
            print(" Success! You must be the producer to delete this post!")

        print(response.json())


    def test_011_post_get_all(self):
        print('\ntest 011')
        print("Getting all posts")
        print('''expected response: [a post object]''')

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title")
        post.save()

        response = self.c.get('/posts/get')
        if response.status_code != 200:
            print(" error with retrieving posts")
        else:
            print(" Success! Got response")

        print(response.json())


    def test_012_post_get_by_location(self):
        print('\ntest 012')
        print("Getting all posts in zipcode 60613")
        print('''expected response: [a post object][a post object from a different user]''')

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title")
        post.save()

        user2 = User(user_fid="user2", user_uname="sampleUser1", 
            user_address="1060 W Addison St", user_city="Chicago", user_state="Illinois", user_zip='60613', # wrigley field
            user_bio="a fake sibling of a fake person")
        user2.save()

        post2 = Post(post_producer=user2, post_recipe=self.recipe, post_title="some random title")
        post2.save()        

        response = self.c.get('/posts/zip', {'zip':'60613'})
        if response.status_code != 200:
            print(" error with retrieving posts")
        else:
            print(" Success! Got response")

        print(response.json())
    
    def test_013_post_get_wrong_post_by_location(self):
        print('\ntest 013')
        print("Getting all posts in zipcode 0 (only post is of zip code 60613)")
        print('''expected response: [nothing]''')

        post = Post(post_producer=self.user, post_recipe=self.recipe, post_title="some random title")
        post.save()      

        response = self.c.get('/posts/zip', {'zip':'0'})
        if response.status_code != 200:
            print(" error with retrieving posts")
        else:
            print(" Success! Got response")

        print(response.json())