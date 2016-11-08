{% extends "es/service_base.msg" %}
{%- import "es/macros.jinja" as macros %}
{% block service_content %}
Ud. especificó como remitente de su mensaje a un personaje inválido
(as-{{ sender_as }}).

{{ macros.character_list(all_characters) }}

Por favor especifique un personaje válido y vuelva a enviar el mensaje
original.

O puede también agregar un nuevo personaje no jugador enviando un
correo electrónico a

  pm-new-npc@{{ server_name }}

Utilice el nombre del personaje como el asunto del correo electrónico.
De manera opcional, puede especificar la forma abreviada del nombre
entre paréntesis. Esta forma abreviada será utilizada para generar los
direcciones de correo electrónico para cada personaje.  Estas formas
abreviadas tienen que ser únicas para cada juego.
{% endblock %}
