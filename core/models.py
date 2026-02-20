from django.conf import settings
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=120)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='actors')
    vote_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-vote_count', 'name']

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='movies')
    vote_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-vote_count', 'title']

    def __str__(self) -> str:
        return self.title


class MovieVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'movie'], name='unique_movie_vote')]


class ActorVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'actor'], name='unique_actor_vote')]