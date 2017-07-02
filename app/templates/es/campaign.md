Campaña de Poisson Magique: {{ campaign_name_ }}
===========================================


Autoría
-------

* GM: {{ gm_attribution }}
{% for character in print_characters %}
* {{ character.type }} {{ character.full_name }} ({{ character.short_form }}): {{ character.attribution }}
{% endfor %}

Todo este contenido está disponible bajo licencia CC-BY-SA.

Ponderaciones numéricas
-----------------------

Number of emails received: {{ all_mails }}

Correos enviados por el GM: {{ gm_emails }} (como NPCs: {{ gm_emails_as_npcs }})

Correos enviados por PCs: {{ pc_emails }}

Correos de tiradas de dados: {{ dice_rolls }}


