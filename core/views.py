from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .db_guards import table_has_column
from .forms import LoginForm, PersonalActorForm, PersonalMovieForm, RegisterForm
from .models import Actor, ActorVote, Country, Movie, MovieVote, PersonalActor, PersonalMovie


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = False

class UserLogoutView(LogoutView):
    next_page = 'login'

def landing_redirect_view(request: HttpRequest) -> HttpResponse:
    return redirect('login')


def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            messages.success(request, 'Your account has been created successfully. Please log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home_view(request: HttpRequest) -> HttpResponse:
    def _table_exists(table_name: str) -> bool:
        try:
            return table_name in connection.introspection.table_names()
        except (ProgrammingError, OperationalError):
            return False

    countries = Country.objects.none()
    movie_country = request.GET.get('movie_country', '')
    actor_country = request.GET.get('actor_country', '')
    country_schema_ready = table_has_column(Country._meta.db_table, 'iso_code')

    if country_schema_ready:
        countries = Country.objects.all()
    else:
        messages.error(request, 'Country data is unavailable until database migrations are applied.')

    personal_movie_table_exists = _table_exists(PersonalMovie._meta.db_table)
    personal_actor_table_exists = _table_exists(PersonalActor._meta.db_table)

    movie_form = PersonalMovieForm(prefix='movie')
    actor_form = PersonalActorForm(prefix='actor')

    if request.method == 'POST':
        if 'add_movie' in request.POST:
            if personal_movie_table_exists:
                movie_form = PersonalMovieForm(request.POST, request.FILES, prefix='movie')
                if movie_form.is_valid():
                    movie = movie_form.save(commit=False)
                    movie.user = request.user
                    movie.save()
                    messages.success(request, 'Movie saved to your personal list.')
                    return redirect('home')
            else:
                messages.error(request, 'Movie list is temporarily unavailable. Please run migrations.')
        elif 'add_actor' in request.POST:
            if personal_actor_table_exists:
                actor_form = PersonalActorForm(request.POST, request.FILES, prefix='actor')
                if actor_form.is_valid():
                    actor = actor_form.save(commit=False)
                    actor.user = request.user
                    actor.save()
                    messages.success(request, 'Actor saved to your personal list.')
                    return redirect('home')
            else:
                messages.error(request, 'Actor list is temporarily unavailable. Please run migrations.')
        elif 'delete_movie' in request.POST and personal_movie_table_exists:
            movie = get_object_or_404(PersonalMovie, id=request.POST.get('delete_movie'), user=request.user)
            movie.delete()
            messages.success(request, 'Movie removed from your list.')
            return redirect('home')
        elif 'delete_actor' in request.POST and personal_actor_table_exists:
            actor = get_object_or_404(PersonalActor, id=request.POST.get('delete_actor'), user=request.user)
            actor.delete()
            messages.success(request, 'Actor removed from your list.')
            return redirect('home')

    movies = []
    actors = []

    try:

        if personal_movie_table_exists:
            movie_queryset = PersonalMovie.objects.filter(user=request.user).select_related('country')
            if movie_country:
                movie_queryset = movie_queryset.filter(country__name__iexact=movie_country)
            movies = list(movie_queryset)
        
        if personal_actor_table_exists:
            actor_queryset = PersonalActor.objects.filter(user=request.user).select_related('country')
            if actor_country:
                actor_queryset = actor_queryset.filter(country__name__iexact=actor_country)
            actors = list(actor_queryset)

    except (ProgrammingError, OperationalError):
        movies = []
        actors = []
        messages.error(request, 'Your personal lists are unavailable until database migrations are applied.')

    top_movie = movies[0] if movies else None
    top_actor = actors[0] if actors else None

    context = {
        'countries': countries,
        'movie_country': movie_country,
        'actor_country': actor_country,
        'top_movie': top_movie,
        'top_actor': top_actor,
        'movies_ranked': movies,
        'actors_ranked': actors,
        'movie_form': movie_form,
        'actor_form': actor_form,
    }
    return render(request, 'core/home.html', context)


@login_required
def vote_movie_view(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = get_object_or_404(Movie, id=movie_id)
    _, created = MovieVote.objects.get_or_create(user=request.user, movie=movie)
    if created:
        Movie.objects.filter(id=movie.id).update(vote_count=F('vote_count') + 1)
        messages.success(request, f'You voted for {movie.title}.')
    else:
        messages.info(request, f'You already voted for {movie.title}.')
    return redirect('home')


@login_required
def vote_actor_view(request: HttpRequest, actor_id: int) -> HttpResponse:
    actor = get_object_or_404(Actor, id=actor_id)
    _, created = ActorVote.objects.get_or_create(user=request.user, actor=actor)
    if created:
        Actor.objects.filter(id=actor.id).update(vote_count=F('vote_count') + 1)
        messages.success(request, f'You voted for {actor.name}.')
    else:
        messages.info(request, f'You already voted for {actor.name}.')
    return redirect('home')