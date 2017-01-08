{% extends "es/service_base.msg" %}
{% block service_content %}

No había tiradas en su mensaje, sin embargo la dirección {{ service_address }} 
fue incluida entres los destinatarios del mensaje.

Asegúrese de que exista una línea en el mensaje que comience con ROLL:

Chequee que no hayan espacios entre ROLL y : y que ROLL esté en mayúsculas.

{% endblock %}
