{% extends "base" %} -*- mode: django-html -*-

{% block content %}
{% for code in data %}
{{ code }}
{% endfor %}
{% endblock %}
