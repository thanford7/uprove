import re
from datetime import datetime


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
        if propHelpers:
            formName = propHelpers.get('formName')
            propFunc = propHelpers.get('propFunc')

        val = data.get(formName or key)
        if propFunc:
            val = propFunc(val)
        isChanged = isChanged or val != getattr(obj, key)
        setattr(obj, key, val)

    if isChanged and hasattr(obj, 'modifiedDateTime'):
        obj.modifiedDateTime = datetime.utcnow()
