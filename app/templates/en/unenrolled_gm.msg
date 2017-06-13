{% extends "en/service_base.msg" %}
{% block service_content %}
The player for the character '{{ short_form }}' for the
game '{{ campaign_name }}' your are directing at {{ server_name }} has
left the game.

The chracter has been turned into a NPC.

You can send emails as this character by including

  as-{{ short_form }}@{{ server_name }}
  
as an extra email recipient.
{% endblock %}
