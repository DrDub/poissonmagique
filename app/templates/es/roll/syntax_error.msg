{% extends "es/service_base.msg" %}
{% block service_content %}

Hay un error de sintaxis en su cadena de tirada

{{ roll }}

y no pudo ser entendida.

La sintaxis para las tiradas de dados es

dígitos 'D'/nada dígitos +/- (más dígitos 'D' dígitos)  < / > dígitos

el signo de mayor o menor y el límite que le sigue son requeridos.

{% endblock %}
