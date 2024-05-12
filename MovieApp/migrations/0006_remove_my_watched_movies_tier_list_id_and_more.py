# Generated by Django 5.0.1 on 2024-03-09 20:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieApp', '0005_alter_my_watched_movies_tier_my_tier_lists_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='my_watched_movies',
            name='tier_list_id',
        ),
        migrations.RemoveField(
            model_name='my_watched_movies',
            name='movie_id',
        ),
        migrations.RemoveField(
            model_name='my_watched_movies',
            name='user',
        ),
        migrations.RemoveField(
            model_name='popular_movies',
            name='popularity',
        ),
        migrations.RemoveField(
            model_name='popular_movies',
            name='vote_average',
        ),
        migrations.RemoveField(
            model_name='popular_movies',
            name='vote_count',
        ),
        migrations.CreateModel(
            name='Movies_Cast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor_name', models.TextField(verbose_name='Cast Name')),
                ('character_name', models.TextField()),
                ('url', models.URLField()),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MovieApp.popular_movies')),
            ],
        ),
        migrations.CreateModel(
            name='Movies_Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director_name', models.TextField(verbose_name='Director Name')),
                ('url', models.URLField()),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MovieApp.popular_movies')),
            ],
        ),
        migrations.DeleteModel(
            name='My_Tier_Lists',
        ),
        migrations.DeleteModel(
            name='My_Watched_Movies',
        ),
    ]