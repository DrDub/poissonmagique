{% extends "service_base.msg" %}
{% block service_content %}
A player has enrolled for the character '{{ short_form }}' for the
game '{{ campaign_name }}' your are directing at {{ server_name }}.

Contact your player by sending emails to

  {{ short_form }}@{{ server_name }}

{% endblock %}
