from django.db import models

# Create your models here.

class Post(models.Model):
    producerid = models.ForeignKey('homeCooked.User')
    recipeid = models.ForeignKey('homeCooked.Recipe')
    available = models.BooleanField(default=True)
    consumerid = models.ForeignKey('homeCooked.User')
    created = models.DateTimeField()
    compleated = models.DateTimeField()