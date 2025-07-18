from contextlib import closing
from methodism import dictfetchone, dictfetchall
from django.db import connection


def get_category(pk=None):
    sql = f"select * from core_category {f'where id={pk}' if pk else ''}"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        if pk: data = dictfetchone(cursor)
        else: data = dictfetchall(cursor)

    return data





