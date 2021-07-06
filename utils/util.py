def safeget(data, key):
    try:
        return data[key]
    except IndexError:
        pass
    except KeyError:
        pass

def hasattrs(d: dict, keys: list):
    return set(keys).issubset(d.keys())
