{% extends "es/service_base.msg" %}
{%- import "es/macros.jinja" as macros %}
{% block service_content %}

Ha pedido que se le dé de baja como jugador del personaje '{{
full_name }}' con forma abreviada {{ short_form }} en el servidor '{{
server_name }}'.

Puede confirmar respondiendo a este correo electrónico o enviando un
correo electrónico vacío a:

  pm-unenroll-{{ unenrollment_address}}@{{ server_name }}

Una vez confirmada, su dirección de correo electrónica será borrada
completamente del servidor y se le atribuirá haber colaborado con su
personaje jugador. Sin embargo, usted no recibirá una copia de los
correos electrónicos al final del juego.
{% endblock %}
