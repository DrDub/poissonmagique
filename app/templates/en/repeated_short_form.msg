{% extends "en/service_base.msg" %}
{%- import "en/macros.jinja" as macros %}
{% block service_content %}
The character {{ full_name }} with short form {{ short_form }} cannot
be created, its short form collides with existing characters.

{{ macros.character_list(all_characters) }}

Please submit again with a short form between parenthesis that does
not duplicate any existing one.
{% endblock %}
