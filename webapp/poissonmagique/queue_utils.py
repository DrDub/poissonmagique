from lamson import queue
from models import MessageID, Queue
from django.db import IntegrityError, connection

def sanity_check(queue):
    """
    Check whether all the messages in the maildir are accounted for.
    Returns the corresponding instance for the Queue ORM.
    """
    try:
        name = queue.dir.split('/')[-1]
        db_queue = Queue.objects.get(name=name)
    except Queue.DoesNotExist:
        db_queue = Queue(name=name, maildir=queue.dir)
        db_queue.save()
    mails_in_folder = len(queue.keys())
    mails_in_db = len(MessageID.objects.filter(queue=db_queue))
    if mails_in_folder != mails_in_db:
        for key in queue.keys():
            if len(MessageID.objects.filter(key=key, queue=db_queue)) == 0:
                msg = queue.get(key)
                try:
                    message_id = MessageID(message_id = msg['Message-ID'][1:-1], key=key, queue=db_queue)
                    message_id.save()
                except IntegrityError:
                    connection._rollback()
                    # race condition with upload queue, all it's good
    return db_queue

def queue_push(queue, msg, key):
    """
    Keep track a new message as it is added to a maildir.
    Returns the newly saved MessageID ORM instance.
    """
    db_queue = sanity_check(queue)
    try:
        message_id = MessageID(message_id = msg['Message-ID'][1:-1], key=key, queue=db_queue)
        message_id.save()
    except IntegrityError:
        connection._rollback()
        message_id = MessageID.objects.get(key=key, queue=db_queue)
        
    return message_id
