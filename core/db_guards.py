from django.db import connection
from django.db.utils import OperationalError, ProgrammingError


def table_has_column(table_name: str, column_name: str) -> bool:
    try:
        with connection.cursor() as cursor:
            description = connection.introspection.get_table_description(cursor, table_name)
    except (ProgrammingError, OperationalError):
        return False

    existing_columns = {col.name for col in description}
    return column_name in existing_columns