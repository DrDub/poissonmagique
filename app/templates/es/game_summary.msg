{% extends "es/service_base.msg" %}
{% block service_content %}
Transcripción del juego hasta ahora, disponible para descarga según su
solicitud:

{{ report_url }}

{% endblock %}
