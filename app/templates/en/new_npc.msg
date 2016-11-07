{% extends "service_base.msg" %}
{% block service_content %}
The character {{ full_name }} with short form {{ short_form }} has
been created.

Known characters:

{% for character in all_characters %}

* {{ character.address }}: {{ character.name }} ({%- if character.is_npc %} NPC {%- else -%} PC {%- endif -%})

{% endfor %}

You can now send an email as this new character by including as-{{
short_form }}@{{ server_name }} as an extra email recipient.
{% endblock %}
