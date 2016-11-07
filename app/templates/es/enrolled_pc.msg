{% extends "service_base.msg" %}
{% block service_content %}
Ud. está ahora jugando el juego '{{ campaign_name }}' en {{ server_name }}.

Ud. puede enviar correos electrónicos a la persona a cargo del juego
en todo momento mediante la dirección:

  gm@{{ server_name }}

Al usar este servidor de Poisson Magique en {{ server_name }} Ud. está
de acuerdo con hacer disponibles sus mensajes según una licencia
CC-BY-SA 3.0.

Para salir del juego y dejar de recibir correos electrónicos envíe un correo a

  pm-end@{{ server_name }}

O puede simplemente esperar a que termine el juego, momento en el cual
Ud. y los otros jugadores recibirán una copia de todos los correos
intercambiados durante el juego.

Disfrute de Poisson Magique!
{% endblock %}
