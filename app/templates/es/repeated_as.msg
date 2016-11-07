{% extends "es/service_base.msg" %}
{% block service_content %}
Ud. incluyó dos personajes como remitentes de su mensaje:

* as-{{ send_as }}
* as-{{ other }}

Por favor especifique sólo uno y vuelva a enviar el mensaje original.
{% endblock %}
