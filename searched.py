from MovieApp.models import Popular_Movies
import tmdbsimple as tmdb
import creds

tmdb.API_KEY = creds.TMDB_API_Key

def search_movie():
    movies = []
    inp = input("Search a movie: ")
    response = tmdb.Search().movie(query=inp,page=1,include_adult=False)
    movies = response
    print(movies)
    return movies

config = tmdb.Configuration().info()
base_url = config['images']['base_url']
size = 'w500' # Edit this for a different image size
search_movies = search_movie()
        
for movie in search_movies:
    movie_info = tmdb.Movies(movie['id']).info()
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
                'poster_path': poster_url,
                'release_date': release_date,
                'title': movie ['title'],
                'video': movie['video'],
                'budget': movie_info['budget'],
                'revenue': movie_info['revenue'],
                'runtime':movie_info['runtime'],
                'tagline': movie_info['tagline'],
                'url': poster_url
            }
        )