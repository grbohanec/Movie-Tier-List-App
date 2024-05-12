from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

# Create your models here.
class Popular_Movies(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    adult = models.BooleanField()
    genre_ids = ArrayField(models.IntegerField(), default=list) # Delete?
    original_language = models.TextField()
    original_title = models.TextField()
    popularity = models.IntegerField(default=0)
    overview = models.TextField()
    poster_path = models.TextField()
    release_date = models.DateField(null = True) # Allowed Null since movies coming out don't have a release date
    title = models.TextField('Movie Name')
    video = models.BooleanField()
    budget = models.BigIntegerField(null = True)
    revenue = models.BigIntegerField(null = True)
    runtime = models.IntegerField(null = True)
    tagline = models.TextField(null = True)
    url = models.URLField()

class Movies_Cast(models.Model):
    movie_id = models.ForeignKey(Popular_Movies, on_delete=models.CASCADE)
    actor_name = models.TextField('Cast Name')
    character_name = models.TextField()
    url = models.URLField()

class Movies_Director(models.Model):
    movie_id = models.ForeignKey(Popular_Movies, on_delete=models.CASCADE)
    director_name = models.TextField('Director Name')
    url = models.URLField()

class My_Tier_Lists (models.Model):
    tier_list_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()

class My_Watched_Movies(models.Model):
    watched_movie_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Popular_Movies, on_delete=models.CASCADE)
    url = models.URLField()

class Tier_List_Watched_Movies(models.Model):
    tier_list_id = models.ForeignKey(My_Tier_Lists, on_delete=models.CASCADE)
    watched_movie_id = models.ForeignKey(My_Watched_Movies, on_delete=models.CASCADE)
    tier_ranking_row = models.TextField()