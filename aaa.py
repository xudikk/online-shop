import sqlite3
from base.helper import dictfetchall, dictfetchone
connect = sqlite3.connect("db.sqlite3")
cursor = connect.cursor()

sql = """
    select * from core_category
"""

cursor.execute(sql)

natija = dictfetchone(cursor)

print(natija)

