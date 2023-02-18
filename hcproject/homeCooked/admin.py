from django.contrib import admin
from .models import *

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Sending Review', {'fields': ['review_user']}),
        ('Recipe Receiving Review', {'fields': ['review_recipe', 'review_rating', 'review_desc']})
    ]

class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name, Description, Host?', {'fields': ['event_name', 'event_desc', 'event_host']}),
        ('When, Where, Who?', {'fields': ['event_date', 'event_time', 'event_location', 'event_capacity']})
    ]

class MessageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sender', {'fields': ['message_sender']}),
        ('Recipient', {'fields': ['message_recipient', 'message']})
    ]


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Producer Side', {'fields': ['post_producer', 'post_desc', 'post_created']}),
        ('Consumer Side', {'fields': ['post_consumer', 'post_review', 'post_compleated']})
    ]

class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Author and Name', {'fields': ['recipe_user', 'recipe_name']}),
        ('Recipe Info', {'fields': ['recipe_desc', 'recipe_ingredients', 'recipe_img']})
    ]

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Login Credentials', {'fields': ['username', 'password']}),
        ('User Info', {'fields': ['email', 'address', 'biography']})
    ]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Message, MessageAdmin)