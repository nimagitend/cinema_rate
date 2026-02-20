from django.db import migrations


def recreate_missing_personal_tables(apps, schema_editor):
    existing_tables = set(schema_editor.connection.introspection.table_names())

    personal_movie = apps.get_model('core', 'PersonalMovie')
    personal_actor = apps.get_model('core', 'PersonalActor')

    if personal_movie._meta.db_table not in existing_tables:
        schema_editor.create_model(personal_movie)
        existing_tables.add(personal_movie._meta.db_table)

    if personal_actor._meta.db_table not in existing_tables:
        schema_editor.create_model(personal_actor)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_expand_countries'),
    ]

    operations = [
        migrations.RunPython(recreate_missing_personal_tables, migrations.RunPython.noop),
    ]