from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Post)
admin.site.register(Message)