from django.core.management.base import BaseCommand
from MovieApp.models import Popular_Movies

class Command(BaseCommand):
    help = 'Deletes adult movies from the database'

    def handle(self, *args, **options):
        Popular_Movies.objects.filter(adult=True).delete()