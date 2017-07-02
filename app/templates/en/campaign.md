Poisson Magique Campaign: {{ campaign_name_ }}
===========================================


Attributions
------------

GM: {{ gm_attribution }}

{% for character in print_characters %}
{{ character.type }} {{ character.full_name }} ({{ character.short_form }}): {{ character.attirbution }}
{%- endfor -%}

All content under license CC-BY-SA

Numbers
-------

Number of emails received: {{ all_mails }}

GM emails: {{ gm_emails }} (as NPCs {{ gm_emails_as_npcs }})

PC emails: {{ pc_emails }}

Dice roll emails: {{ dice_rolls }}

