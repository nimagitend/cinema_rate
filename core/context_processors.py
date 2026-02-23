
def header_profile_context(request):
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {}
    
    first_name = (request.user.first_name or '').strip()
    last_name = (request.user.last_name or '').strip()
    full_name = ' '.join(part for part in [first_name, last_name] if part)
    display_name = full_name or request.user.username

    return {
        'header_display_name': display_name,
    }
