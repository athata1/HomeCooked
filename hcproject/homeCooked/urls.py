from django.urls import path

from . import views
from . import models
from .views import *

app_name = 'HomeCooked'
urlpatterns = [
    path('posts/sort', post_sort),
    path('posts/create', post_create),
    path('posts/get', post_get_all),
    path('posts/zip', post_get_by_loc),
    path('posts/update', post_update),
    path('posts/close', post_close),
    path('posts/delete', post_delete),
    path('users/delete', delete_user),
    path('users/', user_manager),
    path('allergy/', allergy_request, name='allergy_request'),
    path('recipe/create', create_recipe),
    path('recipe/get', get_recipes),
    path('recipe/delete', delete_recipe),
    path('recipe/get/id', get_recipes_by_id),
    path('review/create', create_review),
    path('review/average', get_average_review),
    path('review/get', get_reviews),
]