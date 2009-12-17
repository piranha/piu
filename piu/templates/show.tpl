{% extends "base.html" %} -*- mode: django-html -*-

{% block content %}
{% for code in data %}
{{ code }}
<hr>
{% endfor %}
{% endblock %}
