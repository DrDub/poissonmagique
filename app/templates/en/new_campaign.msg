{% extends "en/service_base.msg" %}
{% block service_content %}
Your new game '{{ campaign_name }}' has been created.

You can add player characters by sending an email to

  pm-new-pc@{{ server_name }}

You will then receive a special email address you can distribute to
your players for them to enroll the campaign with that character.

or you can add non-player characters by sending an email to

  pm-new-npc@{{ server_name }}

In both cases, set the subject of the email to the name of the
character. Optionally, you can specify a short form between
parenthesis. The short form will be used to generate their email
address. Short forms should be unique within the campaign.

For example, to create a character named Alice Cooper with short form
Alice set the subject to

  Alice Cooper (Alice)

You can then send emails as any of the characters (both player and
non-player) by carbon copying the special email as-<short form>, for
example, to send an email as Alice Cooper, use the special email
address

  as-alice@{{ server_name }}

By using this Poisson Magique server at {{ server_name }} you agree to
license your emails under CC-BY-SA 3.0 license.

To finish this campaign, send an email to

  end-game@${{ server_name }}

At that stage all your players will receive a copy for all the emails
exchanged during this game.

Enjoy Poisson Magique!
{% endblock %}
