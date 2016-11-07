{% extends "es/service_base.msg" %}
{% block service_content %}
Un nuevo/a jugador/a ha registrado el personaje '{{ short_form }}'
para el juego '{{ campaign_name }}' que Ud. dirige en {{ server_name }}.

Contáctese con su jugador/a enviando correos electrónicos a

  {{ short_form }}@{{ server_name }}

{% endblock %}
