from django.core.management.base import BaseCommand
from MovieApp.models import Popular_Movies
import tmdbsimple as tmdb
import creds

class Command(BaseCommand):
    help = 'Populates the Popular_Movies table with the budget, revenue, runtime, and tagline of the movie'

    def handle(self, *args, **options):
        tmdb.API_KEY = creds.TMDB_API_Key
        movies = Popular_Movies.objects.all()

        for movie in movies:
            response = tmdb.Movies(movie.movie_id).info()
            Popular_Movies.objects.filter(movie_id=movie.movie_id).update(
                popularity = response['popularity'],
                budget=response['budget'],
                revenue=response['revenue'],
                runtime=response['runtime'],
                tagline=response['tagline']
            )
