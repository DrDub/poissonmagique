# You might want to set up a posgresql DB here
# DATABASES = { 'default': { 'ENGINE':'django.db.backends.postgresql_psycopg2', 'NAME':'pm',  'USER':'pm',  'PASSWORD':'pass',  'HOST':'localhost', 'PORT':'', } }

# set the template dirs to your install and pinax install
TEMPLATE_DIRS = (
    "/path/to/poissonmagique/webapp/templates",
    "/path/to/site-packages/pinax_theme_bootstrap_account/templates",
    "/path/to/site-packages/pinax_theme_bootstrap/templates",
    "/path/to/site-packages/django_forms_bootstrap/templates",
    "/path/to/site-packages/django_forms_bootstrap/templatetags",
)

STATICFILES_DIRS = (
    "/path/to/site-packages/pinax_theme_bootstrap/static",
)

QUEUES_FOLDER= "/path/to/deployment/run/"
