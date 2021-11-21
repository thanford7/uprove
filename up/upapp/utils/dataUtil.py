from datetime import datetime


def setObjectAttributes(obj, data: dict, keyFuncDict: dict):
    isChanged = False
    for key, propFunc in keyFuncDict.items():
        val = data.get(key)
        if propFunc:
            val = propFunc(val)
        isChanged = isChanged or val != getattr(obj, key)
        setattr(obj, key, val)

    if isChanged and hasattr(obj, 'modifiedDateTime'):
        obj.modifiedDateTime = datetime.utcnow()
