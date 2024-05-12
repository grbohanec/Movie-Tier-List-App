from django.core.management.base import BaseCommand
from MovieApp.models import Popular_Movies
import tmdbsimple as tmdb
import creds

class Command(BaseCommand):
    help = 'Populates the popular movies data table with popular movies from TMDB'

    def handle(self, *args, **options):
        tmdb.API_KEY = creds.TMDB_API_Key
        # Config for URL
        config = tmdb.Configuration().info()
        base_url = config['images']['base_url']
        size = 'w500' # Edit this for a different image size
        popular_movies = get_popular_movies()
        
        for movie in popular_movies:
            release_date = movie['release_date'] if movie['release_date'] else None
            poster_path = movie['poster_path']
            poster_url = f"{base_url}{size}{poster_path}"

            if movie['adult'] == False:
                Popular_Movies.objects.update_or_create(
                    movie_id=movie['id'], 
                    defaults={
                        'adult': movie['adult'],
                        'genre_ids': movie['genre_ids'],
                        'original_language': movie['original_language'],
                        'original_title': movie['original_title'],
                        'overview': movie['overview'],
                        'popularity': movie['popularity'],
                        'poster_path': poster_url,
                        'release_date': release_date,
                        'title': movie ['title'],
                        'video': movie['video'],
                        'url': poster_url
                    }
                )

# Function for fenching movies
def get_popular_movies(page_limit=51):
    movies = []
    seen_movie_ids = set()
    for page in range(1, page_limit + 1):
        response = tmdb.Movies().popular(page=page)
        for movie in response['results']:
            if movie['id'] not in seen_movie_ids:
                movies.append(movie)
                seen_movie_ids.add(movie['id'])
    return movies


