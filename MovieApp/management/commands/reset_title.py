from django.core.management.base import BaseCommand
from MovieApp.models import Popular_Movies
import tmdbsimple as tmdb
import creds

class Command(BaseCommand):
    help = 'Resets the titles for all movies in the database to the most updated titles from the TMDB API.'

    def handle(self, *args, **options):
        tmdb.API_KEY = creds.TMDB_API_Key
        movies = Popular_Movies.objects.all()

        for movie in movies:
            tmdb_movie = tmdb.Movies(movie.movie_id)
            response = tmdb_movie.info()
            updated_title = response['title']
            updated_original_title = response['original_title']
            movie.title = updated_title
            movie.original_title = updated_original_title
            movie.save()