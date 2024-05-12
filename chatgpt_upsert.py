from MovieApp.models import Popular_Movies
import tmdbsimple as tmdb
import creds

rec_string = ['Treasure Island', 'Pirates of the Caribbean: The Curse of the Black Pearl', 'Master and Commander: The Far Side of the World']
recommended_movies = []
for rec in rec_string:
    try:
        rec_movies = Popular_Movies.objects.filter(title__icontains=rec)    
        recommended_movies.extend(rec_movies)
        
    except Popular_Movies.DoesNotExist:
        tmdb.API_KEY = creds.TMDB_API_Key
        config = tmdb.Configuration().info()
        base_url = config['images']['base_url']
        size = 'w500' # Edit this for a different image size
        
        response = tmdb.Search().movie(query=rec,page=1,include_adult=False)
        search_movie = response['result'][0]
        print(search_movie)
        #for movie in response['results']:
            #search_movies_list.append(movie)
        
        #list_of_primarykeys = []
        #for movie in search_movies_list:
            #release_date = movie['release_date'] if movie['release_date'] else None
            #poster_path = movie['poster_path']
            #poster_url = f"{base_url}{size}{poster_path}"
        release_date = search_movie['release_date'] if search_movie['release_date'] else None
        poster_path = search_movie['poster_path']
        poster_url = f"{base_url}{size}{poster_path}"
        
        if search_movie['adult'] == False:
            rec_movies = Popular_Movies.objects.update_or_create(
            movie_id=search_movie['id'], 
            defaults={
            'adult': search_movie['adult'],
            'genre_ids': search_movie['genre_ids'],
            'original_language': search_movie['original_language'],
            'original_title': search_movie['original_title'],
            'overview': search_movie['overview'],
            'popularity': search_movie['popularity'],
            'poster_path': poster_url,
            'release_date': release_date,
            'title': search_movie ['title'],
            'video': search_movie['video'],
            'vote_average': search_movie['vote_average'],
            'vote_count': search_movie['vote_count'],
            'url': poster_url})
            recommended_movies.extend(rec_movies)
     

