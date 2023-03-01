from .models import *

def create_review(giver, postid, rating, desc):
    if giver is None or postid is None or rating is None or desc is None or type(giver) != int or type(postid) != int or type(rating) != int or type(desc) != str or rating > 10 or rating < 1:
        raise ValueError

    post = Post.objects.get(id=postid)

    if post is None:
        raise ValueError
    
    receiver=post.post_producer
    recipe_id = post.post_recipe

    review = Review(review_desc=desc, review_giver=giver, review_receiver=receiver, review_rating=rating, review_post=post)

    if review is None:
        raise RuntimeError

def get_all_reviews():
    return Review.objects.all()