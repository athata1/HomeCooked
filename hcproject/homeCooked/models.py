from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User (models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    biography = models.CharField(max_length=200)

    def __str__(self):
        return self.user_name

class Event (models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=200)
    event_desc = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=200)
    event_capacity = models.IntegerField()
    event_host = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name

class Recipe (models.Model):
    recipe_id = models.AutoField(primary_key=True)
    recipe_desc = models.CharField(max_length=200)
    recipe_user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=200)
    recipe_ingredients = models.CharField(max_length=200)
    recipe_img = models.ImageField(upload_to='images')

    def __str__(self):
        return self.recipe_name

class Review (models.Model):
    review_id = models.AutoField(primary_key=True)
    review_desc = models.CharField(max_length=200)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    review_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return self.review_desc

class Post (models.Model):
    post_id = models.AutoField(primary_key=True)
    post_desc = models.CharField(max_length=200)
    post_producer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='producer')
    post_consumer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consumer')
    post_review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_desc

class Message (models.Model):
    message_id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=200)
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    message_recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')

    def __str__(self):
        return self.message_desc

class DiscussionBoard (models.Model):
    discussion_id = models.AutoField(primary_key=True)
    discussion_desc = models.CharField(max_length=200)
    discussion_sender = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    discussion_data = models.DateField()

    def __str__(self):
        return self.discussion_name