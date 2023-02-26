from django.urls import path

from . import views
from . import models

app_name = 'HomeCooked'
urlpatterns = [
    path('posts/', views.post_manager),
    path('users/', views.user_manager),
    path('posts/delete', views.delete_post),
    path('users/delete', views.delete_post),
]