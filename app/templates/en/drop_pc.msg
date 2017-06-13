{% extends "en/service_base.msg" %}
{%- import "en/macros.jinja" as macros %}
{% block service_content %}
You have asked to be dropped as a player character '{{ full_name }}'
with short form {{ short_form }} from the game '{{ campaign_name }}'
at {{ server_name }}.

Confirm by replying to this email or sending an empty email to:

  pm-unenroll-{{ unenrollment_address}}@{{ server_name }}

Once confirmed, your email address will be purged from the server and
you will be attributed to have contributed to this player character.
Please note that you will not receive a copy of the emails from this
game.
{% endblock %}
