from django.db import migrations


COUNTRIES = [
    'Argentina', 'Australia', 'Austria', 'Belgium', 'Brazil', 'Canada', 'Chile', 'China', 'Colombia',
    'Czech Republic', 'Denmark', 'Egypt', 'Finland', 'France', 'Germany', 'Greece', 'Hong Kong',
    'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Ireland', 'Israel', 'Italy', 'Japan',
    'Lebanon', 'Malaysia', 'Mexico', 'Morocco', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway',
    'Pakistan', 'Philippines', 'Poland', 'Portugal', 'Romania', 'Russia', 'Saudi Arabia',
    'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Thailand', 'Turkey',
    'United Kingdom', 'United States',
]


def seed_countries(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    for name in COUNTRIES:
        Country.objects.get_or_create(name=name)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_personal_entries'),
    ]

    operations = [
        migrations.RunPython(seed_countries, migrations.RunPython.noop),
    ]