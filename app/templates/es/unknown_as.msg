{% extends "es/service_base.msg" %}
{% block service_content %}
Ud. especificó como remitente de su mensaje a un personaje inválido
(as-{{ sender_as }}).

Personajes actuales:

{% for character in all_characters %}

* {{ character.address }}: {{ character.name }} ({%- if character.is_npc %} PNJ {%- else -%} PJ {%- endif -%})

{% endfor %}

Por favor especifique un personaje válido y vuelva a enviar el mensaje
original.

O puede también agregar un nuevo personaje no jugador enviando un
correo electrónico a

  pm-register-npc@{{ server_name }}

Utilice el nombre del personaje como el asunto del correo electrónico.
De manera opcional, puede especificar la forma abreviada del nombre
entre paréntesis. Esta forma abreviada será utilizada para generar los
direcciones de correo electrónico para cada personaje.  Estas formas
abreviadas tienen que ser únicas para cada juego.
{% endblock %}
