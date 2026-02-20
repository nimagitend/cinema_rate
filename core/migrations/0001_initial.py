from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('vote_count', models.PositiveIntegerField(default=0)),
                ('country', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='actors', to='core.country')),
            ],
            options={'ordering': ['-vote_count', 'name']},
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('vote_count', models.PositiveIntegerField(default=0)),
                ('country', models.ForeignKey(on_delete=models.deletion.PROTECT, related_name='movies', to='core.country')),
            ],
            options={'ordering': ['-vote_count', 'title']},
        ),
        migrations.CreateModel(
            name='MovieVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=models.deletion.CASCADE, to='core.movie')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ActorVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(on_delete=models.deletion.CASCADE, to='core.actor')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='movievote',
            constraint=models.UniqueConstraint(fields=('user', 'movie'), name='unique_movie_vote'),
        ),
        migrations.AddConstraint(
            model_name='actorvote',
            constraint=models.UniqueConstraint(fields=('user', 'actor'), name='unique_actor_vote'),
        ),
    ]