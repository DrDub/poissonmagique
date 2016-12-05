import redis
from config.settings import redis_host, redis_port, redis_db
from unicode_helper import safe_unicode

r = None

# Data model, currently using redis, but can be moved to SQL or text
# files

def start_table():
    r = redis.StrictRedis(host=redis_host,
                              port=redis_port,
                              db=redis_db)
    assert r.time()
    return r

def _key(key):
    return "pm-" + key

def has_key(key):
    return r.exists(_key(key))

def get(key):
    return safe_unicode(r.get(_key(key)))

def delete_key(key):
    return r.delete(_key(key))

def set_key(key, value):
    return r.set(_key(key), value)

def set_key_ttl(key, value, ttl):
    k = _key(key)
    r.set(k, value)
    r.expire(k, ttl)

def increment(key):
    return r.incr(_key(key))

def create_object(key, **values):
    for k in values:
        r.hset(_key(key), k, values[k])

def get_object(key):
    k = _key(key)
    keys = r.hkeys(k)
    result = {}
    for hk in keys:
        result[hk] = safe_unicode(r.hget(k, hk))
    return result

def set_field(key, field, value):
    r.hset(_key(key), field, value)

def get_field(key, field):
    return safe_unicode(r.hget(_key(key), field))

def add_to_list(key, elem):
    r.rpush(_key(key), elem)

def list_elems(key):
    length = r.llen(_key(key))
    result = []
    for idx in xrange(0,length):
        result.append(safe_unicode(r.lindex(_key(key), idx)))
    return result

def list_len(key):
    return r.llen(_key(key))

def list_append(key, elem):
    r.rpush(_key(key), elem)

def list_append_all(key, elems):
    for elem in elems:
        r.rpush(_key(key), elem)

    
