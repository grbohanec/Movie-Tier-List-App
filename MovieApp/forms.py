from django import forms 
from django.forms import ModelForm
from .models import Popular_Movies, My_Watched_Movies
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#create movie form 
class MovieForm(ModelForm):
    class Meta:
        model = Popular_Movies
        fields = ('adult', 'genre_ids', 'original_language', 'original_title', 'overview', 'poster_path', 'release_date', 'title', 'url')
        labels = {
            'adult': '', 
            'genre_ids': '', 
            'original_language': '', 
            'original_title': '',
            'overview': '', 
            'poster_path': '', 
            'release_date': '', 
            'title': '', 
            'url': ''
        }
        widgets = {
            'adult': forms.TextInput(attrs={'class':'form_control', 'placeholder':'Adult'}),
            'genre_ids': forms.TextInput(attrs={'class':'form_control', 'placeholder':'Genre ID'}), 
            'original_language': forms.TextInput(attrs={'class':'form_control', 'placeholder':'Original Language'}), 
            'original_title': forms.TextInput(attrs={'class':'form_control', 'placeholder':'Original Title'}),
            'overview': forms.TextInput(attrs={'class':'form_control', 'placeholder':'Overview'}),
            'poster_path': forms.TextInput(attrs={'class':'form_control', 'placeholder':'Poster Path'}), 
            'release_date': forms.TextInput(attrs={'class':'form_control', 'placeholder':'Release Date'}), 
            'title': forms.TextInput(attrs={'class':'form_control', 'placeholder':'Title'}),
            'url': forms.TextInput(attrs={'class':'form_control', 'placeholder':'Image URL'}),

        }

class AddWatched(forms.ModelForm):
    class Meta:
        model = My_Watched_Movies
        exclude = ['user', 'movie_id', 'movie_name', 'tier', 'url']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']