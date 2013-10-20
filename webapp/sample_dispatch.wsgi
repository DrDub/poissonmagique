import os
import sys
sys.stdout = sys.stderr

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages
import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp/mod_wsgi/egg-cache'

os.system("mkdir -p '/tmp/mod_wsgi/egg-cache'")

sys.path.append('/path/to/webapp')
sys.path.append('/path/to/pm')

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
