from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView,
    home_view,
    landing_redirect_view,
    register_view,
    profile_view,
    vote_actor_view,
    vote_movie_view,
)

urlpatterns = [
    path('', landing_redirect_view, name='landing'),
    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('vote/movie/<int:movie_id>/', vote_movie_view, name='vote_movie'),
    path('vote/actor/<int:actor_id>/', vote_actor_view, name='vote_actor'),
    path(
        'forgot-password/',
        PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url='/forgot-password/done/',
        ),
        name='password_reset',
    ),
    path(
        'forgot-password/done/',
        PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    path(
        'reset/complete/',
        PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)