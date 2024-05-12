import json
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Popular_Movies, My_Watched_Movies, My_Tier_Lists, Tier_List_Watched_Movies, Movies_Director, Movies_Cast
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from .forms import MovieForm, AddWatched, SignUpForm
import tmdbsimple as tmdb
import openai
from openai import OpenAI
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import creds

openai.api_key = creds.OpenAI_API_Key


# Create your views here.
def login_page(request):
    return render(request, 'login.html')


def sign_up_page(request):
    if request.method == 'POST':
        form =  SignUpForm(request.POST or None)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created ' + user)
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = SignUpForm() #important to do this so that either post or get you're sending form to html
    return render(request, 'signup.html', {'form':form})

@login_required
def chat_gpt_page(request):
    return render(request, 'openai.html')

@login_required
def home_page(request):
    movies = Popular_Movies.objects.all()
    p = Paginator(movies, 88)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    nums = "a" * page_obj.paginator.num_pages
    return render(request, 'home_page.html', {'movies' : movies, 'page_obj' : page_obj, 'nums' : nums}) 

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def chatgpt_response(request):
    question = request.POST.get('question', '')

    try:
        response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=question,
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0)
        answer = response.choices[0].text.strip()
        return JsonResponse({"response": answer})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page')  # Change 'home' to the desired URL after login

        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login')  # Change 'login' to the desired URL after logout

@login_required
@csrf_exempt
def edit_user_tierlist(request, tierlist_id):
    watched_movies = My_Watched_Movies.objects.all()
    tierlist = My_Tier_Lists.objects.get(tier_list_id=tierlist_id)
    ranked_movie_ids = Tier_List_Watched_Movies.objects.filter(tier_list_id=tierlist)
    ids = [movie.watched_movie_id.watched_movie_id for movie in ranked_movie_ids]
    unranked_movies = watched_movies.exclude(watched_movie_id__in=ids)

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            watched_movie = data['movieId']
            new_tier = data['newTier']

            if int(watched_movie) in ids:
                ranked_movie = ranked_movie_ids.get(watched_movie_id=watched_movies.get(watched_movie_id=watched_movie))
                ranked_movie.tier_ranking_row = new_tier
                ranked_movie.save()
            else:
                Tier_List_Watched_Movies.objects.create(tier_list_id=tierlist,watched_movie_id=watched_movies.get(watched_movie_id=watched_movie), tier_ranking_row=new_tier)
            
            if new_tier == "movies_window":
                obj_to_delete = Tier_List_Watched_Movies.objects.get(tier_ranking_row="movies_window")
                obj_to_delete.delete()
            
            unranked_movies = unranked_movies.exclude(watched_movie_id=watched_movie)

            return JsonResponse({'message': 'Movie tier updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return render(request, 'edit_user_tierlist.html', {'watched_movies': watched_movies, 'tierlist': tierlist, 'ranked_movie_ids': ranked_movie_ids, 'unranked_movies': unranked_movies})

@login_required
def search_movies(request):
    if request.method == "POST":
        searched = request.POST['searched']
        #add the search feature here
        tmdb.API_KEY = creds.TMDB_API_Key
        config = tmdb.Configuration().info()
        base_url = config['images']['base_url']
        size = 'w500' # Edit this for a different image size
        search_movies_list = []
        response = tmdb.Search().movie(query=searched,page=1,include_adult=False)

        for movie in response['results']:
            search_movies_list.append(movie)
        search_movies_list = search_movies_list[:10] #limit the search
         
        list_of_primarykeys = []
        for movie in search_movies_list:
            release_date = movie['release_date'] if movie['release_date'] else None
            poster_path = movie['poster_path']
            poster_url = f"{base_url}{size}{poster_path}"
        
            if movie['adult'] == False:
                list_of_primarykeys.append(movie['id'])
                Popular_Movies.objects.update_or_create(
                movie_id=movie['id'], 
                defaults={
                'adult': movie['adult'],
                'genre_ids': movie['genre_ids'],
                'original_language': movie['original_language'],
                'original_title': movie['original_title'],
                'popularity': movie['popularity'],
                'overview': movie['overview'],
                'poster_path': poster_url,
                'release_date': release_date,
                'title': movie ['title'],
                'video': movie['video'],
                'url': poster_url}
                )
                response = tmdb.Movies(movie['id']).credits() #adding Director
                crew = response['crew']
                for crew_member in crew:
                    if crew_member['job'] == 'Director':
                        director_object = Popular_Movies.objects.get(movie_id=movie['id'])
                        Movies_Director.objects.update_or_create(movie_id=director_object,
                        defaults={'director_name': crew_member['name'],
                        'url': f"{base_url}{size}{crew_member['profile_path']}"
                        })
                response = tmdb.Movies(movie['id']).credits() #adding cast members
                cast = response['cast'][:7]
                for actor in cast:
                    actor_object = Popular_Movies.objects.get(movie_id=movie['id'])
                    Movies_Cast.objects.update_or_create(movie_id=actor_object,actor_name=actor['name'],
                    character_name=actor['character'],url=f"{base_url}{size}{actor['profile_path']}")

        movies = Popular_Movies.objects.filter(pk__in=list_of_primarykeys)
        #SELECT *
        #FROM public."MovieApp_popular_movies"
        #WHERE title ILIKE '%scooby%'
        #ORDER BY movie_id ASC;
        return render(request, 'search_movies.html', {'searched' : searched, 'movies' : movies})
    else:
        return render(request, 'search_movies.html', {})

@login_required    
def all_movies(request):
    movie_list = Popular_Movies.objects.all()
    return render(request, 'movies_list.html', {'movie_list' : movie_list})

@login_required
def list_movies(request):
    movie_list = Popular_Movies.objects.all()
    return render(request, 'movies.html', {'movie_list' : movie_list})

@login_required
def show_movies(request, movie_id):
    movie = Popular_Movies.objects.get(pk=movie_id)
    recommended_movies = []
    try:
        # prompt = f"Give me three movie titles in the same genre as this movie:{movie.title}. Put each movie title on a new line with no numbering, no bullet points, no punctuation, no dashes, and no special characters. When recommending the original 'Star Wars: Episode IV - A New Hope' just return Star Wars as the movie title. Do this for similar long titled movies too."
        # response = openai.completions.create(
        #     model="gpt-4-0125-preview",
        #     prompt=prompt,
        #     temperature=0.5,
        #     max_tokens=150,
        #     top_p=0.5,
        #     frequency_penalty=0.0,
        #     presence_penalty=0.0
        # )
        client = OpenAI(api_key=creds.TMDB_API_Key)

        response = client.chat.completions.create(
            model = "gpt-4-1106-preview",
            response_format = { "type" : "json_object" },
            messages = [
                {"role": "system", "content": "You are a huge movie fan with a wide array of movie knowledge tasked with quickly recommending movies to people and outputting it in a JSON with recommendations as the key in the response."},
                {"role": "user", "content": f"Give me three movie titles quickly in the same genre as this movie: {movie.title}. Put each movie title on the same line seperated by a | with no numbering, no bullet points, no punctuation, no dashes and no special characters."}
            ]
        )
        recommendations = response.choices[0].message.content
        data = json.loads(recommendations)
        rec_string = data["recommendations"]
        rec_string = rec_string.split(" | ")
        print(f"Received recommendations from ChatGPT: {rec_string}")

        recommended_movies = []
        for rec in rec_string:
            movie_object = Popular_Movies.objects.filter(title__iexact=rec)
            movie_object2 = Popular_Movies.objects.filter(title__istartswith=rec)
            movie_object = movie_object.union(movie_object2)
            if movie_object.first() != None: 
                print("rec movie already added to database")
                movie_object = movie_object.first()
                recommended_movies.append(movie_object) #add movie object to list
        
            else:
                tmdb.API_KEY = creds.TMDB_API_Key
                config = tmdb.Configuration().info()
                base_url = config['images']['base_url']
                size = 'w500' # Edit this for a different image size

                response = tmdb.Search().movie(query=rec,page=1,include_adult=False)
                search_movie = response['results'][0]
                print(search_movie)
                release_date = search_movie['release_date'] if search_movie['release_date'] else None
                poster_path = search_movie['poster_path']
                poster_url = f"{base_url}{size}{poster_path}"
        
                if search_movie['adult'] == False:
                    rec_movies = Popular_Movies.objects.create(
                    movie_id=search_movie['id'], 
                    adult= search_movie['adult'],
                    genre_ids=search_movie['genre_ids'],
                    original_language=search_movie['original_language'],
                    original_title=search_movie['original_title'],
                    popularity=search_movie['popularity'],
                    overview=search_movie['overview'],
                    poster_path=poster_url,
                    release_date=release_date,
                    title=search_movie ['title'],
                    video=search_movie['video'],
                    url=poster_url)
                    recommended_movies.append(rec_movies) #add movie object to list

                    response = tmdb.Movies(search_movie['id']).credits() #adding Director
                    crew = response['crew']
                    for crew_member in crew:
                        if crew_member['job'] == 'Director':
                            director_object = Popular_Movies.objects.get(movie_id=search_movie['id'])
                            Movies_Director.objects.update_or_create(movie_id=director_object,
                                defaults={'director_name': crew_member['name'],
                                        'url': f"{base_url}{size}{crew_member['profile_path']}"
                                        })
                            
                            
                    response = tmdb.Movies(search_movie['id']).credits() #adding cast members
                    cast = response['cast'][:7]
                    for actor in cast:
                        actor_object = Popular_Movies.objects.get(movie_id=search_movie['id'])
                        Movies_Cast.objects.update_or_create(movie_id=actor_object,actor_name=actor['name'],
                            character_name=actor['character'],url=f"{base_url}{size}{actor['profile_path']}")
            
    except Exception as e:
        print(f"Error fetching recommendations: {e}")

    print("The recommend movies list is: ")
    print(recommended_movies)
    #check to see if User has watched movie
    id_exists = My_Watched_Movies.objects.filter(movie_id_id=movie.movie_id, user_id=request.user.id).exists()

    movie_watched = My_Watched_Movies(movie_id=movie)
    directors = Movies_Director.objects.filter(movie_id_id=movie.movie_id)
    cast = Movies_Cast.objects.filter(movie_id_id=movie.movie_id)
    
    if request.POST:
        form = AddWatched(request.POST or None, instance=movie_watched)
        if form.is_valid():
            watched_object = form.save(commit=False)
            watched_object.user_id = request.user.id
            watched_object.movie_id_id = movie.movie_id
            watched_object.movie_name = movie.title
            watched_object.tier = "N"
            watched_object.url = movie.url
            watched_object.save()
        return redirect('home_page')
    
    return render(request, 'show_movies.html', {'movie' : movie, 'exists':id_exists, 'form' : My_Watched_Movies, 'recommended_movies' : recommended_movies[:3],
                                                'directors':directors, 'cast': cast})

@login_required
def update_movies(request, movie_id):
    movie = Popular_Movies.objects.get(pk=movie_id)
    form = MovieForm(request.POST or None, instance=movie)
    if form.is_valid():
        form.save()
        return redirect('list-movies')

    return render(request, 'update_movie.html', {'movie' : movie, 'form' : form})

@login_required
def add_movie(request):
    submitted = False
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_movie?submitted=True')
    else:
        form = MovieForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_movie.html', {'form' : form, 'submitted' : submitted})


@login_required
def user_tierlists(request):
    tierlists = My_Tier_Lists.objects.filter(user=request.user)  # Assuming you want to show per user
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            name = request.POST.get('name')
            if name:
                My_Tier_Lists.objects.create(name=name, user=request.user)
                return redirect('user_tierlists')  
            
        if action == 'delete':
            tierlist_id = request.POST.get('tierlist_id')
            if tierlist_id:
                My_Tier_Lists.objects.get(tier_list_id=tierlist_id).delete()
                return redirect('user_tierlists')
            
        if action == 'rename':
            tierlist_id = request.POST.get('tierlist_id')
            name = request.POST.get('name')
            if tierlist_id and name:
                tierlist = My_Tier_Lists.objects.get(tier_list_id=tierlist_id)
                tierlist.name = name
                tierlist.save()
                return redirect('user_tierlists')
        
    return render(request, 'user_tierlists.html', {'tierlists': tierlists})