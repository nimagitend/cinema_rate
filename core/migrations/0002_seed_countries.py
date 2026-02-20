from django.db import migrations


COUNTRIES = [
    'United States',
    'United Kingdom',
    'Canada',
    'France',
    'Germany',
    'Japan',
    'India',
    'South Korea',
    'Italy',
    'Spain',
]


def seed_countries(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    for name in COUNTRIES:
        Country.objects.get_or_create(name=name)


def remove_countries(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    Country.objects.filter(name__in=COUNTRIES).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_countries, remove_countries),
    ]