{% extends "es/base.msg" %}
{%- block content -%}

El/la GM pidió que tirara {{ roll_str }}.

Tirada: {{ roll }}

{% if check %}
Éxito.
{% else %}
Fallo.
{% endif %}

{% endblock %}
