{% extends "base" %} -*- mode: django-html -*-

{% block content %}
{% if owner %}<a id="edit" href="/{{ id }}/edit/">edit your code</a>{% endif %}
{% for code in data %}
{{ code }}
{% endfor %}
{% endblock %}
