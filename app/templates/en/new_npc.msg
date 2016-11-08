{% extends "en/service_base.msg" %}
{%- import "en/macros.jinja" as macros %}
{% block service_content %}
The character {{ full_name }} with short form {{ short_form }} has
been created.

{{ macros.character_list(all_characters) }}

You can now send an email as this new character by including as-{{
short_form }}@{{ server_name }} as an extra email recipient.
{% endblock %}
