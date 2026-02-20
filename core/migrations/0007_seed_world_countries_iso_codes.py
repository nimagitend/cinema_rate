from django.db import migrations, models

from core.countries import COUNTRY_DATA


def seed_world_countries(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    for iso_code, name in COUNTRY_DATA:
        by_name = Country.objects.filter(name=name).first()
        if by_name:
            by_name.iso_code = iso_code
            by_name.save(update_fields=['iso_code'])
            continue

        by_iso = Country.objects.filter(iso_code=iso_code).first()
        if by_iso:
            by_iso.name = name
            by_iso.save(update_fields=['name'])
            continue

        Country.objects.create(name=name, iso_code=iso_code)


def unseed_world_countries(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    iso_codes = [iso for iso, _ in COUNTRY_DATA]
    Country.objects.filter(iso_code__in=iso_codes).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_country_iso_code_personalactor_poster_image_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_world_countries, unseed_world_countries),
        migrations.AlterField(
            model_name='country',
            name='iso_code',
            field=models.CharField(max_length=2, unique=True),
        ),
    ]