from django.urls import path
from . import views
from .views import chatgpt_response
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_view, name='login_page'),
    path('chatgpt-page/', views.chat_gpt_page, name='chatgpt_page'),
    path('chatgpt-response/', chatgpt_response, name='chatgpt_response'),
    path('home/',views.home_page, name='home_page'),
    path('sign_up/', views.sign_up_page, name='sign_up'),
    path('login/',views.login_view, name='login'),
    path('login/',views.logout_view, name='logout'),
    path('show_movie/<movie_id>', views.show_movies, name='show-movies'),
    path('edit_user_tierlist/<tierlist_id>', views.edit_user_tierlist, name='edit_user_tierlist'),
    path('search_movies', views.search_movies, name='search-movies'),
    path('movies', views.all_movies, name='list-movies'),
    path('list_movies', views.list_movies, name='movies' ),
    path('show_movie/<movie_id>', views.show_movies, name='show-movies'),
    path('update_movie/<movie_id>', views.update_movies, name='update-movies'),
    path('add_movie', views.add_movie, name='add-movie'),
    path('user_tierlists/', views.user_tierlists, name='user_tierlists'),
    # Default Django Logout View
    path('logout/', LogoutView.as_view(next_page='login_page'), name='logout'),
]
