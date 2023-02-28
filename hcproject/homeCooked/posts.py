from .models import *

def get_posts_by(user_id):
    if type(user_id) != int:
        raise TypeError('user_id must be an integer')
    return Post.objects.filter(post_producer__exact=user_id)

def get_posts_including(user_id):
    if type(user_id) != int:
        raise TypeError('user_id must be an integer')

    return get_posts_by(user_id) | get_posts_to(user_id)

def get_posts_to(user_id):
    if type(user_id) != int:
        raise TypeError('user_id must be an integer')

    return Post.objects.filter(post_consumer__exact=user_id)

def get_post(post_id):
    if type(post_id) != int:
        raise TypeError('post_id must be an integer')

    return Post.objects.filter(post_id__exact=post_id)