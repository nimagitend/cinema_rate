from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, RegisterForm
from .models import Actor, ActorVote, Country, Movie, MovieVote


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    pass


def landing_redirect_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')


def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home_view(request: HttpRequest) -> HttpResponse:
    countries = Country.objects.all()
    movie_country = request.GET.get('movie_country', '')
    actor_country = request.GET.get('actor_country', '')
    show_all_movies = request.GET.get('show_all_movies') == '1'

    movies = Movie.objects.select_related('country').order_by('-vote_count', 'title')
    actors = Actor.objects.select_related('country').order_by('-vote_count', 'name')

    if movie_country:
        movies = movies.filter(country_id=movie_country)
    if actor_country:
        actors = actors.filter(country_id=actor_country)

    top_movie = movies.first()
    top_actor = actors.first()

    movies_ranked = list(movies[1:20])
    if show_all_movies:
        movies_ranked = list(movies[1:])

    actors_ranked = list(actors[1:20])

    context = {
        'countries': countries,
        'movie_country': movie_country,
        'actor_country': actor_country,
        'top_movie': top_movie,
        'top_actor': top_actor,
        'movies_ranked': movies_ranked,
        'actors_ranked': actors_ranked,
        'show_all_movies': show_all_movies,
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