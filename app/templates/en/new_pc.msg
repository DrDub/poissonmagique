{% extends "en/service_base.msg" %}
{% block service_content %}
The player character {{ full_name }} with short form {{ short_form }}
has been created and it is ready to enroll.

Ask your player to enroll by sending an email to

  pm-enroll-{{ enrollment_address}}@{{ server_name }}

Known characters:

{% for character in all_characters %}

* {{ character.address }}: {{ character.name }} ({%- if character.is_npc %} NPC {%- else -%} PC {%- endif -%})

{% endfor %}

You can now send an email as this new character by including

  as-{{ short_form }}@{{ server_name }}
  
as an extra email recipient.
{% endblock %}
