from django.core.management.base import BaseCommand
from MovieApp.models import Popular_Movies, Movies_Director, Movies_Cast
import tmdbsimple as tmdb
import creds

class Command(BaseCommand):
    help = 'Populates the cast and director datatables with members from all popular movies'

    def handle(self, *args, **options):
        tmdb.API_KEY = creds.TMDB_API_Key
        movies = Popular_Movies.objects.all()
        # Config for URL
        config = tmdb.Configuration().info()
        base_url = config['images']['base_url']
        size = 'w500' # Edit this for a different image size
        
        # Populate Directors Table
        for movie in movies:
            response = tmdb.Movies(movie.movie_id).credits()
            crew = response['crew']
            for crew_member in crew:
                if crew_member['job'] == 'Director':
                    Movies_Director.objects.update_or_create(
                        movie_id=movie,
                        defaults={
                            'director_name': crew_member['name'],
                            'url': f"{base_url}{size}{crew_member['profile_path']}"
                        }
                    )

        # Populate Cast Table
        for movie in movies:
            response = tmdb.Movies(movie.movie_id).credits()
            cast = response['cast'][:7]
            for actor in cast:
                Movies_Cast.objects.update_or_create(
                    movie_id=movie,
                    actor_name=actor['name'],
                    character_name=actor['character'],
                    url=f"{base_url}{size}{actor['profile_path']}"
                )