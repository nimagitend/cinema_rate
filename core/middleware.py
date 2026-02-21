from datetime import timedelta

from django.conf import settings
from django.contrib.auth import logout
from django.utils import timezone
from django.utils.dateparse import parse_datetime


class SessionTimeoutMiddleware:
    """Force re-login after a fixed authenticated session window."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            login_timestamp = request.session.get('auth_login_timestamp')
            max_session_age = getattr(settings, 'SESSION_COOKIE_AGE', 3600)

            if not login_timestamp:
                request.session['auth_login_timestamp'] = timezone.now().isoformat()
            else:
                login_time = parse_datetime(login_timestamp)
                if login_time and timezone.now() - login_time > timedelta(seconds=max_session_age):
                    logout(request)

        return self.get_response(request)
