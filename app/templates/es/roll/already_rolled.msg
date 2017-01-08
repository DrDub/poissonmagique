{% extends "es/service_base.msg" %}
{% block service_content %}

Esta tirada ya ha sido ejecutada.

El GM pidió {{ roll_str }}.

Resultado de la tirada: {{ roll }}

{% if check %}
Éxito.
{% else %}
Fallo.
{% endif %}

{% endblock %}
