{% extends "en/service_base.msg" %}
{% block service_content %}

This dice has already been rolled.

GM asked for {{ roll_str }}.

Rolled: {{ roll }}

{% if check %}
Check.
{% else %}
Failed.
{% endif %}

{% endblock %}
