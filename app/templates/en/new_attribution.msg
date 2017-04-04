{% extends "en/service_base.msg" %}
{% block service_content %}

Your emails for the game

  {{ campaign_name }}

at

  {{ server_name }}

are now attributed to

  {{ attribution }}
{% endblock %}
