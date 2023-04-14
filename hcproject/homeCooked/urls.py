from django.urls import path

from . import views
from . import models
from .views import *

app_name = 'HomeCooked'
urlpatterns = [
    path('event/create', create_event),
    path('event/get', get_events),
    path('event/rsvp', rsvp_for_event),
    path('event/get/attended', get_attended_events),
    path('event/get/unattended', get_unattended_events),
    path('posts/sort', post_sort),
    path('posts/create', post_create),
    path('posts/get', post_get_all),
    path('posts/loc', post_get_by_loc),
    path('posts/update', post_update),
    path('posts/close', post_close),
    path('posts/delete', post_delete),
    path('posts/all', post_get_all),
    path('posts/zip', post_get_by_zip),
    path('users/delete', delete_user),
    path('users/', user_manager),
    path('users/uname', user_by_uname),
    path('users/uname/contains', user_by_uname_contains),
    path('allergy/', allergy_request, name='allergy_request'),
    path('recipe/create', create_recipe),
    path('recipe/get', get_recipes),
    path('recipe/delete', delete_recipe),
    path('recipe/get/id', get_recipes_by_id),
    path('review/create', create_review),
    path('review/average', get_average_review),
    path('review/get', get_reviews),
    path('search', search_for),
    path('notifs', get_notifs),
]