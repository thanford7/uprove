import re

import inflect
from django.utils import timezone

inflectEngine = inflect.engine()

def getFileNameFromUrl(url):
    if not url:
        return None

    groups = re.split(r'\\|/', url)
    return groups[-1]


def setObjectAttributes(obj, data: dict, keyFuncDict: dict):
    isChanged = False
    for key, propHelpers in keyFuncDict.items():
        formName = None
        propFunc = None
        isProtectExisting = False
        isIgnoreExcluded = False
        if propHelpers:
            formName = propHelpers.get('formName')
            propFunc = propHelpers.get('propFunc')
            isProtectExisting = propHelpers.get('isProtectExisting')
            isIgnoreExcluded = propHelpers.get('isIgnoreExcluded')

        if isIgnoreExcluded and (formName or key) not in data:
            continue

        val = data.get(formName or key)
        if propFunc:
            val = propFunc(val)
        if val is None and isProtectExisting:
            continue
        isChanged = isChanged or val != getattr(obj, key)
        setattr(obj, key, val)

    if isChanged and hasattr(obj, 'modifiedDateTime'):
        obj.modifiedDateTime = timezone.now()

    return isChanged


def capitalizeAllWords(str):
    words = str.split(' ')
    return ' '. join([w.capitalize() for w in words])


def pluralize(word, count):
    return f'{count} {inflectEngine.plural(word, count)}'


def intOrNone(val):
    try:
        return int(val)
    except ValueError:
        return None