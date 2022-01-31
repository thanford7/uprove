import os

from django.db import connection


def executeSqlMigration(sqlFileName):
    filePath = os.path.join(os.path.dirname(__file__), sqlFileName)
    with open(filePath) as sqlFile:
        sqlStatement = sqlFile.read()
        with connection.cursor() as c:
            c.execute(sqlStatement)
