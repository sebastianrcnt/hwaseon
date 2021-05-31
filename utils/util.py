def safeget(data, key):
    try:
        return data[key]
    except IndexError:
        pass
    except KeyError:
        pass

