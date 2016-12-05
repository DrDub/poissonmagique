from salmon.routing import route, stateless, nolocking, Router
from salmon import queue

@route("(to)@(host)", to=".+", host=".+")
@stateless
@nolocking
def START(message, to=None, host=None):
    """
    @stateless and routes everything.
    Has @nolocking, but that's alright since it's just writing to a maildir.
    """
    Router.FULL_QUEUE.push(message)
