{% extends "es/service_base.msg" %}
{% block service_content %}
Su nuevo juego '{{ campaign_name }}' ha sido creado.

Puede añadir nuevos jugadores enviando un correo electrónico a

  pm-register-pc@{{ server_name }}

Entonces recibirá una dirección especial de correo electrónico que
puede distribuir a sus jugadores para que se registren en la campaña
para jugar a dicho personaje.

O puede también agregar personajes no jugadores enviando un correo
electrónico a

  pm-register-npc@{{ server_name }}

En ambos casos, utilice el nombre del personaje como el asunto del
correo electrónico. De manera opcional, puede especificar la forma
abreviada del nombre entre paréntesis. Esta forma abreviada será
utilizada para generar los direcciones de correo electrónico para cada
personaje. Estas formas abreviadas tienen que ser únicas para cada
campaña.

Por ejemplo, para crear un personaje llamado Alice Cooper con nombre
abreviado Alice utilice como asunto del correo electrónico:

  Alice Cooper (Alice)

Ud. puede después enviar mensajes como cualquiera de los personajes
(jugadores o no jugadores) incluyendo como destinatario la dirección
de correo electrónica especial as-<forma abreviada>, por ejemplo, para
enviar un correo electrónico como Alice Cooper, utilice la dirección
especial de correo

  as-Alice@{{ server_name }}

Al usar este servidor de Poisson Magique en {{ server_name }} Ud. está
de acuerdo con hacer disponibles sus mensajes según una licencia
CC-BY-SA 3.0.

Para terminar esta campaña, envíe un correo electrónico a

  end-game@{{ server_name }}

En ese momento todos los jugadores recibirán una copia de todos los
correos intercambiados durante el juego.

Disfrute de Poisson Magique!
{% endblock %}
