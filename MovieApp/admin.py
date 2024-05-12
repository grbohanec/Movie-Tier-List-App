from django.contrib import admin
from .models import Popular_Movies, My_Watched_Movies, My_Tier_Lists, Tier_List_Watched_Movies, Movies_Cast, Movies_Director

# Register your models here.
admin.site.register(Popular_Movies)
admin.site.register(My_Watched_Movies)
admin.site.register(My_Tier_Lists)
admin.site.register(Tier_List_Watched_Movies)
admin.site.register(Movies_Cast)
admin.site.register(Movies_Director)