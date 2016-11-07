{% extends "service_base.msg" %}
{% block service_content %}

El personaje {{ full_name }} con forma abreviada {{ short_form }} ha conseguido crearse de manera exitosa.

Personajes actuales:

{% for character in all_characters %}

* {{ character.address }}: {{ character.name }} ({%- if character.is_npc %} NPC {%- else -%} PC {%- endif -%})

{% endfor %}

Ud. puede ahora enviar correos electrónicos como este nuevo personaje
incluyendo as-{{ short_form }}@{{ server_name }} como una dirección
extra a la que envía el correo electrónico.
{% endblock %}
