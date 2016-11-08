{% extends "es/service_base.msg" %}
{%- import "es/macros.jinja" as macros %}
{% block service_content %}
El personaje {{ full_name }} con forma abreviada {{ short_form }} no
pudo crearse, su forma abreviada ya existe.

{{ macros.character_list(all_characters) }}

Por favor vuelva a enviar su mensaje con una forma abreviada entre
paréntesis que no duplique a ninguna de las existentes.
{% endblock %}



