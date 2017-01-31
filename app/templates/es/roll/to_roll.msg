{% extends "es/base.msg" %}
{%- block content -%}

Su GM ha pedido que tire {{ roll }}.

Para completar esta tirada de dados, responda a este mensaje o
envíe un mensaje vacío a:

  {{ roll_address }}


{% endblock %}
