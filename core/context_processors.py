from django.db import connection
from django.db.utils import OperationalError, ProgrammingError
from django.templatetags.static import static

from .models import UserProfile


def _profile_table_exists() -> bool:
    try:
        return UserProfile._meta.db_table in connection.introspection.table_names()
    except (ProgrammingError, OperationalError):
        return False


def header_profile_context(request):
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {}

    display_name = (request.user.first_name or '').strip() or 'Profile'
    avatar_url = static('images/default-avatar.svg')

    if _profile_table_exists():
        try:
            profile = UserProfile.objects.filter(user=request.user).first()
            if profile and profile.avatar:
                avatar_url = profile.avatar.url
        except (ProgrammingError, OperationalError):
            pass

    return {
        'header_display_name': display_name,
        'header_avatar_url': avatar_url,
    }
