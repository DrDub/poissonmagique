{% extends "es/service_base.msg" %}
{% block service_content %}
El personaje {{ full_name }} con forma abreviada {{ short_form }} no
pudo crearse, su forma abreviada ya existe.

Personajes actuales:

{% for character in all_characters %}

* {{ character.address }}: {{ character.name }} ({%- if character.is_npc %} PNJ {%- else -%} PJ {%- endif -%})

{% endfor %}

Por favor vuelva a enviar su mensaje con una forma abreviada entre
paréntesis que no duplique a ninguna de las existentes.
{% endblock %}



