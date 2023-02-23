from django.urls import path

from . import views
from . import models

app_name = 'HomeCooked'
urlpatterns = [
    path('posts/', views.post_request),
    path('posts/by', views.post_produced_by),
    path('posts/all', views.post_post_has),
    path('posts/new', views.post_new_post),
    path('posts/done', views.post_complete)
]