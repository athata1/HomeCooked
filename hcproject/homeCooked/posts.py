from .models import *
import datetime

def get_posts_by(user_id):
    if type(user_id) != int:
        raise TypeError('user_id must be an integer')
    
    return Post.objects.filter(post_producer__exact=user_id)

def get_posts_to(user_id):
    if type(user_id) != int:
        raise TypeError('user_id must be an integer')
    
    return Post.objects.filter(post_consumer__exact=user_id)

def get_posts_with(user_id):
    if type(user_id) != int:
        raise TypeError('user_id must be an integer')
    
    return get_posts_by(user_id) | get_posts_to(user_id)

def get_post(post_id):
    if type(post_id) != int:
        raise TypeError('post_id must be an integer')
    
    return Post.objects.get(pk=post_id)


def create_post(user_id, recipe_id, title, desc):
    if type(user_id) != int or type(recipe_id) != int or type(title) != str or type(desc) != str:
        raise TypeError('invalid parameter types')

    producer= User.objects.get(pk=user_id)
    recipe = Recipe.objects.get(pk=user_id)

    if producer is None:
        raise ValueError('unable to find user with that id')
    if recipe is None:
        raise ValueError('unable to find recipe with that id')

    post = Post(post_producer_id=producer.pk, post_recipe_id=recipe.pk, post_title=title, post_desc=desc, post_created=datetime.datetime.now())
    
    post.save()

    return post.post_id

def update_post(postid, title="", desc="", consumer_id=-1, recipe_id=-1):
    
    if postid is None:
        raise ValueError("invalid Post")

    if title != "":
        post.post_title = title

    if desc != "":
        post.post_desc = desc
    
    if consumer_id > 0:
        consumer = User.objects.get(user_id=consuemr_id)

        if consumer is None:
            raise ValueError('unable to find user with that id')

        if not post.post_available:
            post.post_available = False
            post.post_completed = datetime.datetime.now()
        post.post_consumer = consumer
    
    if recipe_id > 0:
        recipe = Recipe.objects.get(recipe_id = recipe_id)

        if recipe is None:
            raise ValueError('unable to find recipe with that id')

        post.post_recipe = recipe
    
    post.save()

    return post.pk
