{% extends "en/service_base.msg" %}
{% block service_content %}
The game '{{ campaign_name }}' has finished.

You can download a transcript of the game, available under CC-BY-SA
3.0 license, from

{{ report_url }}

Your email address and all your emails have been purged from this
server.

You now are free to join a new game or start a campaign as a GM.
{% endblock %}
