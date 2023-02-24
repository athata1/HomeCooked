from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_username', 'user_pass', 'user_email', 'user_address', 'user_bio')
    list_display_links = ('user_id', 'user_username')
    list_filter = ('user_id', 'user_username', 'user_email')
    search_fields = ('user_id', 'user_username', 'user_email')

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'event_name', 'event_desc', 'event_date', 'event_time', 'event_location', 'event_capacity', 'event_host')
    list_display_links = ('event_id', 'event_name')
    list_filter = ('event_id', 'event_name', 'event_date', 'event_time', 'event_location', 'event_capacity', 'event_host')
    search_fields = ('event_id', 'event_name', 'event_date', 'event_time', 'event_location', 'event_host')

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_id', 'recipe_desc', 'recipe_user', 'recipe_name', 'recipe_ingredients', 'recipe_img')
    list_display_links = ('recipe_id', 'recipe_name')
    list_filter = ('recipe_id', 'recipe_user', 'recipe_name')
    search_fields = ('recipe_id', 'recipe_name', 'recipe_user')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'review_desc', 'review_user', 'review_recipe', 'review_rating')
    list_display_links = ('review_id', 'review_desc')
    list_filter = ('review_id', 'review_user', 'review_recipe', 'review_rating')
    search_fields = ('review_id', 'review_user', 'review_recipe')

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'post_recipe', 'post_desc', 'post_producer', 'post_consumer', 'post_created', 'post_completed', 'post_title', 'post_available')
    list_display_links = ('post_id', 'post_desc')
    list_filter = ('post_id', 'post_producer', 'post_consumer', 'post_available')
    search_fields = ('post_id', 'post_producer', 'post_consumer', 'post_available')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'message', 'message_sender', 'message_recipient', 'message_sent')
    list_display_links = ('message_id', 'message_sender')
    list_filter = ('message_id', 'message_sender', 'message_recipient', 'message_sent')
    search_fields = ('message_id', 'message_sender', 'message_recipient')

class DiscussionBoardAdmin(admin.ModelAdmin):
    list_display = ('discussion_id', 'discussion_desc', 'discussion_sender', 'discussion_event', 'discussion_data')
    list_display_links = ('discussion_id', 'discussion_desc')
    list_filter = ('discussion_id', 'discussion_sender', 'discussion_event', 'discussion_data')
    search_fields = ('discussion_id', 'discussion_sender', 'discussion_event')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(DiscussionBoard, DiscussionBoardAdmin)