
def safe_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
        return obj
    return unicode(obj.__repr__())
#    return obj.__repr__() #unicode(obj).encode('ascii','ignore')
