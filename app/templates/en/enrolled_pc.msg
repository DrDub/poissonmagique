{% extends "service_base.msg" %}
{% block service_content %}
You are now playing the game '{{ campaign_name }}' at {{ server_name }}.

You can send an email to the person in charge of this game at any time
by emailing:

  gm@{{ server_name }}

By using this Poisson Magique server at {{ server_name }} you agree to
license your emails under CC-BY-SA 3.0 licence.

To drop from the game and stop receiving emails send an email to

  pm-end@{{ server_name }}

Or you can wait until the game finishes, when you and all the other
players will receive a copy of all the emails sent.

Enjoy Poisson Magique!
{% endblock %}
