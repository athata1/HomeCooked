from django.urls import path

from . import views
from . import models

app_name = 'HomeCooked'
urlpatterns = [
    path('posts/', views.post_request),
    path('posts/db', views.post_manager),
    path('users/', views.user_manager),
]