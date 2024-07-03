def serialise(obj: object):
    if hasattr(obj, "__obj__"):
        return obj.__obj__()
    else:
        return dict()
