from django.test import TestCase, Client, RequestFactory
from django.core import serializers
from django.utils import timezone
from .models import *

class HomeCookedTestCases(TestCase):   
    def setUp(self):
        self.user = User(user_fid="user1", user_uname="sampleUser", 
            user_address="1060 W Addison St", user_city="Chicago", user_state="Illinois", user_zip='60613', # wrigley field
            user_bio="a fake person")
        self.user.save()

        self.recipe = Recipe.objects.create(recipe_user=self.user, recipe_name="a recipe", recipe_ingredients="stuff and things",
            recipe_img="https://imgur.com/71HOrWu", recipe_desc="a fake recipe that is deff not real.")
        self.recipe.save()

        self.post = Post.objects.create(post_producer=self.user, post_consumer=self.user, post_title="a new post", post_desc="a post description",
            post_recipe=self.recipe)
        self.post.save();
        
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

        response = self.c.get('/posts/zip', {'city':'Chicago', 'state':'Illinois'})
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

    def test_101_user_get(self):
        print("\ntest 101")
        print("fetching a user")
        print('expected response: [a user object]')

        response = self.c.get('/users/', {'fid':'user1',})

        if response.status_code != 200:
            print(" error with fetching post, test failed")
        else:
            print(" Success! got response:")

        print(response.json())

    def test_102_user_create(self):
        print("\ntest 102")
        print("creating a new user")
        print('expected response: "User created"')

        response = self.c.post('/users/', {
            'type':'Create',
            'fid':'user2',
            'uname':'user2'
            })

        if response.status_code != 200:
            print(" error with fetching post, test failed")
        else:
            print(" Success! got response:")

        print(response.json())

    def test_103_user_create_dup_fid(self):
        print("\ntest 103")
        print("creating a new user with a duplicate user fid")
        print('expected response: "Error: Account already created"')

        response = self.c.post('/users/', {
            'type':'Create',
            'fid':'user1',
            'uname':'user2'
            })

        if response.status_code != 404:
            print(" Other error encountered:")
        else:
            print(" Success! got correct response:")

        print(response.json())

    def test_103_user_create_dup_uname(self):
        print("\ntest 103")
        print("creating a new user with a duplicate username")
        print('expected response: "Error: Account already created"')

        response = self.c.post('/users/', {
            'type':'Create',
            'fid':'user2',
            'uname':'sampleUser'
            })

        if response.status_code != 404:
            print(" Other error encountered:")
        else:
            print(" Success! got correct response:")

        print(response.json())

    def test_104_user_update_uname(self):
        print("\ntest 104")
        print("updating a user's username")
        print('expected response: "Saved data"')

        response = self.c.post('/users/', {
            'type':'Change',
            'fid':'user1',
            'uname':'user1'
            })

        if response.status_code != 404:
            print(" Other error encountered:")
        else:
            print(" Success! got correct response:")

        print(response.json())

        print('\nnew user is:')
        print(self.c.get('/users/', {'fid':self.user.user_fid}).json()['user'])

    def test_105_user_update_uname(self):
        print("\ntest 105")
        print("updating a user")
        print('expected response: "Saved data"')

        
        response = self.c.post('/users/', {
            'type':'Change',
            'fid':'user1',
            'address':'a place',
            'bio':'something something',
            'city':'sanfransokio',
            'state':'constant fear',
            'zip':'58008'
            })

        if response.status_code != 404:
            print(" Other error encountered:")
        else:
            print(" Success! got correct response:")

        print(response.json())

        print('\nnew user is:')
        print(self.c.get('/users/', {'fid':self.user.user_fid}).json()['user'])

    def test_106_user_delete(self):
        print("\ntest 106")
        print("deleting a user")
        print('expected response: "Deleted User"')

        response = self.c.post('/users/delete', {'fid':'user1'})

        if response.status_code != 404:
            print(" Other error encountered:")
        else:
            print(" Success! got correct response:")

        print(response.json())

        self.user = User(user_fid="user1", user_uname="sampleUser", 
            user_address="1060 W Addison St", user_city="Chicago", user_state="Illinois", user_zip='60613', # wrigley field
            user_bio="a fake person")
        self.user.save()
    
    def test_107_user_get_by_uname(self):
        print("\ntest 107")
        print("fetching a user by uname")
        print('expected response: [a user object]')

        response = self.c.get('/users/uname', {'uname':self.user.user_uname})

        if response.status_code != 200:
            print(" error with fetching post, test failed")
        else:
            print(" Success! got response:")

        print(response.json())


    def test_201_recipe_create(self):
        print("\ntest 201")
        print("creating a recipe")
        print('expected response: "Created recipe"')

        response = self.c.post('/recipe/create', {
            'fid':'user1', 'title':'test recipe please ignore', 'desc':'a new recipe description',
            'ingredients':"{'stuff and things'}", 'tags':'gluten free', 'image':'stuff/o/images/things'})
        
        if response.status_code != 200:
            print(" Error encountered:")
        else:
            print(" Success! got response:")

        print(response.json())
    
    def test_202_recipe_get(self):
        print("\ntest 202")
        print("getting recipes by user token")
        print('expected response: "[2 recipe objects]"')

        recipe2 = Recipe.objects.create(recipe_user=self.user, recipe_name="another recipe", recipe_ingredients="more stuff and things",
            recipe_img="https://imgur.com/71HOrWu", recipe_desc="another fake recipe that is deff not real.")
        recipe2.save()

        response = self.c.get('/recipe/get', {'token':self.user.user_fid});
        
        if response.status_code != 200:
            print(" Error encountered:")
        else:
            print(" Success! got response:")

        print(response.json())

    def test_203_recipe_get_by_id(self):
        print("\ntest 203")
        print("getting recipe by user id")
        print('expected response: "[recipe object]"')

        response = self.c.get('/recipe/get/id', {'recipe_id':self.recipe.recipe_id});
        
        if response.status_code != 200:
            print(" Error encountered:")
        else:
            print(" Success! got response:")

        print(response.json())

    def test_204_recipe_delete(self):
        print("\ntest 202")
        print("deleting recipe")
        print('expected response: "Recipe deleted"')

        recipe2 = Recipe.objects.create(recipe_user=self.user, recipe_name="another recipe", recipe_ingredients="more stuff and things",
            recipe_img="https://imgur.com/71HOrWu", recipe_desc="another fake recipe that is deff not real.")
        recipe2.save()

        response = self.c.post('/recipe/delete', {'token':self.user.user_fid, 'recipe_id': recipe2.recipe_id});
        
        if response.status_code != 200:
            print(" Error encountered:")
        else:
            print(" Success! got response:")

        print(response.json())

    def test_301_review_create(self):
        print("\ntest 301")
        print("creating a review")
        print('expected response: "Saved review"')

        response = self.c.post('/review/create', {'fid':self.user.user_fid, 'post_id':self.post.post_id,
        'description':'absolutely flavorless, do not recommend', 'rating':'1'})
        
        if response.status_code != 200:
            print(" Error encountered:")
        else:
            print(" Success! got response:")

        print(response.json())
    
    def test_302_get_reviews_by_fid(self):
        print("\ntest 302")
        print("getting reviews by fid")
        print('expected response: "[review object]"')

        review = Review(review_desc="Seller didn't tip", review_giver=self.user, review_receiver=self.user,
            review_recipe=self.recipe, review_rating=1, review_post=self.post)
        review.save();

        response = self.c.get('/review/get', {'token':self.user.user_fid});
        
        if response.status_code != 200:
            print(" Error encountered:")
        else:
            print(" Success! got response:")

        print(response.json())
    
    def test_303_get_reviews_by_uname(self):
        print("\ntest 303")
        print("getting reviews by uname")
        print('expected response: "[review object]"')

        review = Review(review_desc="Seller didn't tip", review_giver=self.user, review_receiver=self.user,
            review_recipe=self.recipe, review_rating=1, review_post=self.post)
        review.save();

        response = self.c.get('/review/get', {'uname':self.user.user_uname});
        
        if response.status_code != 200:
            print(" Error encountered:")
        else:
            print(" Success! got response:")

        print(response.json())

    def test_304_get_avg_reviews(self):
        print("\ntest 304")
        print("getting avg rating of a user")
        print('expected response: [rating out of 5]')

        review = Review(review_desc="Seller didn't tip", review_giver=self.user, review_receiver=self.user,
            review_recipe=self.recipe, review_rating=1, review_post=self.post)
        review.save();

        response = self.c.get('/review/average', {'fid':self.user.user_fid});
        
        if response.status_code != 200:
            print(" Error encountered:")
        else:
            print(" Success! got response:")

        print(response.json())