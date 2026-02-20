from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_seed_countries'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('production_year', models.PositiveIntegerField()),
                ('poster_url', models.URLField(max_length=500)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(0), MaxValueValidator(100)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('country', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='personal_movies', to='core.country')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='personal_movies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-score', '-created_at', 'title'],
            },
        ),
        migrations.CreateModel(
            name='PersonalActor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('production_year', models.PositiveIntegerField()),
                ('poster_url', models.URLField(max_length=500)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(0), MaxValueValidator(100)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('country', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='personal_actors', to='core.country')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='personal_actors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-score', '-created_at', 'full_name'],
            },
        ),
    ]