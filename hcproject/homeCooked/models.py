from django.db import models

# Create your models here.

class Post(models.Model):
    producer = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, models.SET_NULL, blank=True, null=True)
    available = models.BooleanField(default=True)
    consumer = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField()
    compleated = models.DateTimeField()