import os
from typing import Optional

from django.db import connection


def executeSql(fileName: str, sqlArgs: list, asDict:Optional[bool] = True):
    filePath = os.path.join(os.path.dirname(__file__), f'{fileName}.sql')
    sqlStatement = open(filePath).read()
    with connection.cursor() as cursor:
        cursor.execute(sqlStatement, sqlArgs)
        rows = cursor.fetchall()

        if asDict:
            columnNames = [col[0] for col in cursor.description]
            rows = [dict(zip(columnNames, row)) for row in rows]

    return rows


def getUserProfile(profileId):
    return executeSql('userProfile', [profileId])