from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Allergy (models.Model):
    food_name = models.CharField(max_length=200)
    health_labels = models.CharField(max_length=200)

    def __str__(self):
        return self.food_name

class User (models.Model):
    user_id = models.AutoField(primary_key=True, verbose_name='User ID')
    user_fid = models.CharField(max_length=200, verbose_name='Firebase ID')
    user_uname = models.CharField(max_length=200, verbose_name='Username')
    user_address = models.CharField(max_length=200, verbose_name='Address', default="")
    user_city = models.CharField(max_length=200, verbose_name='City', default="")
    user_state = models.CharField(max_length=200, verbose_name='State', default="")
    user_bio = models.CharField(max_length=200, verbose_name='Biography', default="")

    def __str__(self):
        return self.user_uname

class Event (models.Model):
    event_id = models.AutoField(primary_key=True, verbose_name='Event ID')
    event_name = models.CharField(max_length=200, verbose_name='Name')
    event_desc = models.CharField(max_length=200, verbose_name='Description')
    event_date = models.DateField(verbose_name='Date')
    event_time = models.TimeField(verbose_name='Time')
    event_location = models.CharField(max_length=200, verbose_name='Location')
    event_capacity = models.IntegerField(verbose_name='Capacity')
    event_host = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Host')

    def __str__(self):
        return self.event_name

class Recipe (models.Model):
    recipe_id = models.AutoField(primary_key=True, verbose_name='Recipe ID')
    recipe_desc = models.CharField(max_length=200, verbose_name='Description')
    recipe_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    recipe_name = models.CharField(max_length=200, verbose_name='Name')
    recipe_ingredients = models.CharField(max_length=200, verbose_name='Ingredients')
    recipe_img = models.CharField(max_length=200, verbose_name='Image')

    def __str__(self):
        return self.recipe_name

class Post (models.Model):
    post_id = models.AutoField(primary_key=True, verbose_name='Post ID')
    post_title = models.CharField(max_length=100, verbose_name='Title')
    post_desc = models.CharField(max_length=200, verbose_name='Description')
    post_producer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='producer', verbose_name='Producer')
    post_consumer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='consumer', default=2, verbose_name='Consumer')
    post_created = models.DateTimeField(auto_created=True, verbose_name='Created Date/Time')
    post_completed = models.DateTimeField(auto_now=True, verbose_name='Completed Date/Time')
    post_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Recipe')
    post_available = models.BooleanField(default=True)

    def __str__(self):
        return self.post_desc

class Review (models.Model):
    review_id = models.AutoField(primary_key=True, verbose_name='Review ID')
    review_desc = models.CharField(max_length=200, verbose_name='Description')
    review_giver = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='User Giver')
    review_receiver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User Receiver')
    review_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Recipe')
    review_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name='Rating')
    review_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')

    def __str__(self):
        return self.review_desc

class Message (models.Model):
    message_id = models.AutoField(primary_key=True, verbose_name='Message ID')
    message = models.CharField(max_length=200, verbose_name='Content')
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', verbose_name='Sender')
    message_recipient = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='recipient', verbose_name='Recipient')
    message_sent = models.DateTimeField(default=datetime.now, verbose_name='Sent Date/Time')

    def __str__(self):
        return self.message_desc

class DiscussionBoard (models.Model):
    discussion_id = models.AutoField(primary_key=True, verbose_name='Discussion ID')
    discussion_desc = models.CharField(max_length=200, verbose_name='Description')
    discussion_sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Sender')
    discussion_event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Event')
    discussion_data = models.DateField(verbose_name='Date')

    def __str__(self):
        return self.discussion_name