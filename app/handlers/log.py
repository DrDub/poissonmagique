from lamson.routing import route, stateless, nolocking, Router
from lamson import queue
import game

@route("(to)@(host)", to=".+", host=".+")
@stateless
@nolocking
def START(message, to=None, host=None):
    """
    @stateless and routes everything.
    Has @nolocking, but that's alright since it's just writing to a maildir.
    """
    Router.FULL_QUEUE.push(message)
