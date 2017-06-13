{% extends "es/service_base.msg" %}
{% block service_content %}
La persona que controlaba el personaje de forma abreviada
{{ short_form }} en su campaña '{{ campaign_name }}' que Ud. está
dirigiendo en el servidor {{ server_ame}} ha abandonado el juego.

El personaje ha sido convertido en un personaje no jugador.

Ud. puede enviar correos electrónicos como este personaje
incluyendo

  as-{{ short_form }}@{{ server_name }}

como una dirección extra a la que envía el correo electrónico.
{% endblock %}
