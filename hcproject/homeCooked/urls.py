from django.urls import path

from . import views
from . import models
from .views import *

app_name = 'HomeCooked'
urlpatterns = [
    path('posts/', post_manager),
    path('users/', user_manager),
    path('posts/delete', delete_post),
    path('users/delete', delete_user),
    path('allergy/', allergy_request, name='allergy_request'),
]