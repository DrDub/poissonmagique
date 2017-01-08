{% extends "en/base.msg" %}
{%- block content -%}

GM asked for {{ roll_str }}.

Rolled: {{ roll }}

{% if check %}
Check.
{% else %}
Failed.
{% endif %}

{% endblock %}
