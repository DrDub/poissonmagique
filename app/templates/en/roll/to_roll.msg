{% extends "en/base.msg" %}
{%- block content -%}

Your GM asked for {{ roll }}.

To complete this dice roll, reply to this message
or send an empty message to:

  {{ roll_address }}

{% endblock %}
