{% extends "en/service_base.msg" %}
{% block service_content %}
You specified at least two characters in your message:

* as-{{ send_as }}
* as-{{ other }}

Please specify only one and send again.
{% endblock %}
