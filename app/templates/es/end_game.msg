{% extends "es/service_base.msg" %}
{% block service_content %}
El juego '{{ campaign_name }}' ha terminado.

Puede usted descargar una transcripción del juego, disponible según la licencia CC-BY-SA 3.0, de la siguiente dirección:

{{ report_url }}

Su dirección de correo electrónico así como todos sus correos han sido
eliminados de este servidor.

Usted puede unirse a otro juego o comenzar un juego nuevo como GM.
{% endblock %}
