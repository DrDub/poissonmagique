from lamson.routing import route, stateless, nolocking, Router
from lamson import queue
import game
from webapp.poissonmagique.queue_utils import queue_push

@route("(to)@(host)", to=".+", host=".+")
@stateless
@nolocking
def START(message, to=None, host=None):
    """
    @stateless and routes everything.
    Has @nolocking, but that's alright since it's just writing to a maildir.
    """
    key = Router.FULL_QUEUE.push(message)
    queue_push(Router.FULL_QUEUE, message, key)
