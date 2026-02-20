from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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


class PersonalMovie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal_movies')
    title = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='personal_movies')
    production_year = models.PositiveIntegerField()
    poster_url = models.URLField(max_length=500)
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created_at', 'title']

    def __str__(self) -> str:
        return f'{self.title} ({self.user})'


class PersonalActor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal_actors')
    full_name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='personal_actors')
    production_year = models.PositiveIntegerField()
    poster_url = models.URLField(max_length=500)
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created_at', 'full_name']

    def __str__(self) -> str:
        return f'{self.full_name} ({self.user})'


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