

class _object(object):
    pass

def asobj(d):
    ret = _object()
    ret.__dict__.update(d)
    return ret
