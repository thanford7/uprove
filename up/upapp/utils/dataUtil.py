

def setObjectAttributes(obj, data: dict, keyFuncDict: dict):
    for key, propFunc in keyFuncDict.items():
        val = data.get(key)
        if propFunc:
            val = propFunc(val)
        setattr(obj, key, val)
