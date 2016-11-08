{% extends "es/service_base.msg" %}
{%- import "es/macros.jinja" as macros %}
{% block service_content %}
El personaje {{ full_name }} con forma abreviada {{ short_form }} ha
conseguido crearse de manera exitosa y esta listo para registrarse.

Pídale a su jugador/a que se registre enviando un correo electrónico a

  pm-enroll-{{ enrollment_address}}@{{ server_name }}

{{ macros.character_list(all_characters) }}

Ud. puede ahora enviar correos electrónicos como este nuevo personaje
incluyendo

  as-{{ short_form }}@{{ server_name }}

como una dirección extra a la que envía el correo electrónico.
{% endblock %}
