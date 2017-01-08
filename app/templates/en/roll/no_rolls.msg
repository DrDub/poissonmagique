{% extends "en/service_base.msg" %}
{% block service_content %}

There were no rolls on your message, but {{ service_address }} was addressed.

Make sure there is a line by itself starting with ROLL:

Check for no spaces between ROLL and : and the capitalization of ROLL.

{% endblock %}
