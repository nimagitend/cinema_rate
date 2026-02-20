from django.conf import settings
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from datetime import date
from .countries import iso_to_flag

def _delete_file_from_storage(file_field) -> None:
    if not file_field:
        return
    storage = file_field.storage
    file_name = file_field.name
    if file_name and storage.exists(file_name):
        storage.delete(file_name)

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iso_code = models.CharField(max_length=2, unique=True)

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

    @property
    def flag_emoji(self) -> str:
        return iso_to_flag(self.iso_code)

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
    poster_url = models.URLField(max_length=500, blank=True, default='')
    poster_image = models.FileField(upload_to='posters/movies/', blank=True, null=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created_at', 'title']

    @property
    def poster_source(self) -> str:
        if self.poster_image:
            return self.poster_image.url
        return self.poster_url
    def delete(self, using=None, keep_parents=False):
        _delete_file_from_storage(self.poster_image)
        return super().delete(using=using, keep_parents=keep_parents)
    def __str__(self) -> str:
        return f'{self.title} ({self.user})'


class PersonalActor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal_actors')
    full_name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='personal_actors')
    production_year = models.PositiveIntegerField()
    poster_url = models.URLField(max_length=500, blank=True, default='')
    poster_image = models.FileField(upload_to='posters/actors/', blank=True, null=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created_at', 'full_name']

    @property
    def poster_source(self) -> str:
        if self.poster_image:
            return self.poster_image.url
        return self.poster_url

    @property
    def age(self) -> int:
        return max(0, date.today().year - self.production_year)
    def delete(self, using=None, keep_parents=False):
        _delete_file_from_storage(self.poster_image)
        return super().delete(using=using, keep_parents=keep_parents)
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