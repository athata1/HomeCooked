from django.apps import AppConfig


class HomecookedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homeCooked'

class Post(producerID, recipeID):
    postid = 0;
    producerID = producerID;
    recipeID = recipeID;
    available = True;
    consumerID = 0;