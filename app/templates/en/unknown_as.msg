{% extends "en/service_base.msg" %}
{% block service_content %}
You specified an unknown character to be the sender of your message
(as-{{ sender_as }}).

Known characters:

{% for character in all_characters %}

* {{ character.address }}: {{ character.name }} ({%- if character.is_npc %} NPC {%- else -%} PC {%- endif -%})

{% endfor %}

Please specify a valid sender and send again.

Alternatively, you can add non-player characters by sending an email
to

  pm-register-npc@{{ server_name }}

And set the subject of the email to the name of the
character. Optionally, you can specify a short form between
parenthesis. The short form will be used to generate their email
address. Short forms should be unique within the campaign.
{% endblock %}
