{% extends "service_base.msg" %}
{% block service_content %}
The character {{ full_name }} with short form {{ short_form }} cannot
be created, its short form collides with existing characters.

Known characters:

{% for character in all_characters %}

* {{ character.address }}: {{ character.name }} ({%- if character.is_npc %} NPC {%- else -%} PC {%- endif -%})

{% endfor %}

Please submit again with a short form between parenthesis that does
not duplicate any existing one.
{% endblock %}
