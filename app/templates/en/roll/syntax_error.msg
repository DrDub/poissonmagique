{% extends "en/service_base.msg" %}
{% block service_content %}

There was a syntax error in your roll string

{{ roll }}

and it cannot be parsed.

The syntax for dice rolls is

digits 'D'/nothing digits +/- (more digits 'D' digits)  < / > digits

the more or less sign and the limit afterward are mandatory.

{% endblock %}
