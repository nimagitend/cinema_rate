from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView,
    home_view,
    register_view,
    vote_actor_view,
    vote_movie_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('vote/movie/<int:movie_id>/', vote_movie_view, name='vote_movie'),
    path('vote/actor/<int:actor_id>/', vote_actor_view, name='vote_actor'),
]