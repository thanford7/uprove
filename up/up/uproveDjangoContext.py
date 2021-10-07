from datetime import date

from up.up import settings

COPYRIGHT_START_YEAR = 2021
currentYear = date.today().year

def uproveDjangoContext(request):
    return {
        'DEBUG': settings.DEBUG,
        'copyrightYearRange': f'{COPYRIGHT_START_YEAR}{"-" + str(currentYear) if currentYear != COPYRIGHT_START_YEAR else ""}',
        'baseJSUrl': '',  # TODO
        'version': '',  # TODO
        'versionDateTime': ''  # TODO
    }