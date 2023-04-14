from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
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
    #user_zip = models.CharField(max_length=6, verbose_name='Zipcode', default="")
    user_bio = models.CharField(max_length=200, verbose_name='Biography', default="")
    image_text = models.CharField(max_length=200, verbose_name='Image text', default="")
    user_longitude = models.DecimalField(decimal_places=5, max_digits=8, verbose_name="Longitude", default=0.0)
    user_latitude = models.DecimalField(decimal_places=5, max_digits=8, verbose_name="Latitude", default=0.0)
    user_link = models.CharField(max_length=200, verbose_name="External link", default="localhost:3000/chat")
    def __str__(self):
        return self.user_uname

class Event (models.Model):
    event_id = models.AutoField(primary_key=True, verbose_name='Event ID')
    event_name = models.CharField(max_length=200, verbose_name='Name')
    event_desc = models.CharField(max_length=200, verbose_name='Description')
    event_date = models.DateField(verbose_name='Date')
    event_time = models.TimeField(verbose_name='Time')
    event_location = models.CharField(max_length=200, verbose_name='Location')
    event_capacity = models.IntegerField(verbose_name='Capacity', null=True)
    event_host = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Host')

    def __str__(self):
        return self.event_name

class Rsvp (models.Model):
    rsvp_id = models.AutoField(primary_key=True, verbose_name='Rsvp ID')
    rsvp_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Event Guest')
    rsvp_event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Event Attending')
    
    def __str__(self):
        return self.user.user_uname + "-" + self.event.event_name

class Recipe (models.Model):
    recipe_id = models.AutoField(primary_key=True, verbose_name='Recipe ID')
    recipe_desc = models.CharField(max_length=200, verbose_name='Description')
    recipe_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    recipe_name = models.CharField(max_length=200, verbose_name='Name')
    recipe_ingredients = models.CharField(max_length=200, verbose_name='Ingredients')
    recipe_sys_tags = models.CharField(max_length=200, verbose_name='Allergens', default='')
    recipe_tags = models.CharField(max_length=200, verbose_name='Tags', default='')
    recipe_img = models.CharField(max_length=200, verbose_name='Image')

    def __str__(self):
        return self.recipe_name

class Post (models.Model):
    post_id = models.AutoField(primary_key=True, verbose_name='Post ID')
    post_title = models.CharField(max_length=100, verbose_name='Title')
    post_desc = models.CharField(max_length=200, verbose_name='Description')
    post_producer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='producer', verbose_name='Producer')
    post_consumer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='consumer', verbose_name='Consumer', null=True)
    post_created = models.DateTimeField(auto_created=True, verbose_name='Created Date/Time', default=timezone.now)
    post_completed = models.DateTimeField(auto_now=True, verbose_name='Completed Date/Time')
    post_recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE, related_name='RecipeID', verbose_name='Recipe')
    post_available = models.BooleanField(default=True)

    def __str__(self):
        return self.post_desc

class Review (models.Model):
    review_id = models.AutoField(primary_key=True, verbose_name='Review ID')
    review_desc = models.CharField(max_length=200, null=True, blank=True, verbose_name='Description')
    review_giver = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='UserGiver')
    review_receiver = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='UserReceiver')
    review_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Recipe')
    review_rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name='Rating')
    review_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')

    def __str__(self):
        return self.review_desc

class Message (models.Model):
    message_id = models.AutoField(primary_key=True, verbose_name='Message ID')
    message = models.CharField(max_length=200, verbose_name='Content')
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', verbose_name='Sender')
    message_recipient = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='recipient', verbose_name='Recipient')
    message_sent = models.DateTimeField(default=timezone.now, verbose_name='Sent Date/Time')

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

class Notification (models.Model):
    class notif_type (models.TextChoices):
        POST = 'PO', _('Post Bought')
        MESSAGE = 'ME', _('Message Recevied')
        USER = 'US', _('Profile Updated')
        EVENT = 'EV', _('RSVP Received')
        NONE = 'NO', _('error/default type') 
    
    notif_id = models.AutoField(primary_key=True, verbose_name='Notification ID')
    notif_type = models.CharField(max_length=2, choices=notif_type.choices, default=notif_type.NONE)
    notif_time = models.DateTimeField(auto_created=True, verbose_name='notification time', default=timezone.now)
    notif_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='notification receiver')
    notif_message = models.CharField(max_length=200, verbose_name='notification message')