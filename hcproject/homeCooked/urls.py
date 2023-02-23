from django.urls import path

from . import views
from . import models

app_name = 'HomeCooked'
urlpatterns = [
    path('posts/', views.post_request),
    path('posts/getPostedBy/<int:pk>/', views.post_byUser_request),
]