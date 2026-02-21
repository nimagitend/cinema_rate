from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_default_superuser(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    User = apps.get_model(app_label, model_name)

    username = 'nima'
    email = 'nima@example.com'
    password = 'M123456m'

    user, _ = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        },
    )

    user.email = user.email or email
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.password = make_password(password)
    user.save(update_fields=['email', 'is_staff', 'is_superuser', 'is_active', 'password'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_seed_world_countries_iso_codes'),
    ]

    operations = [
        migrations.RunPython(create_default_superuser, migrations.RunPython.noop),
    ]