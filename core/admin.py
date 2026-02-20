from django.contrib import admin

from .models import Actor, ActorVote, Country, Movie, MovieVote


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'vote_count')
    list_filter = ('country',)
    search_fields = ('title',)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'vote_count')
    list_filter = ('country',)
    search_fields = ('name',)


admin.site.register(MovieVote)
admin.site.register(ActorVote)