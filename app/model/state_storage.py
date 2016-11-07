from salmon.routing import StateStorage, ROUTE_FIRST_STATE
import table as t

MAX_TTL_IN_SEC = 1 * 7 * 24 * 60 * 60L # one week

class UserStateStorage(StateStorage):

    def get(self, key, sender):
        state_key = self.key(key, sender)
        if t.has_key(state_key):
            return t.get(state_key)
        else:
            return ROUTE_FIRST_STATE

    def key(self, key, sender):
        return "salmon-state-%s-%s" % (key, sender)

    def set(self, key, sender, to_state):
        state_key = self.key(key, sender)

        if t.has_key(state_key):
            if to_state == "START":
                # don't store these, they're the default when it doesn't exist
                t.delete(state_key)
            else:
                t.set_key_ttl(state_key, to_state, MAX_TTL_IN_SEC)
        else:
            # avoid storing start states
            if to_state != "START":
                t.set_key_ttl(state_key, to_state, MAX_TTL_IN_SEC)
