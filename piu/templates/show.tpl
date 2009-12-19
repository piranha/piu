{% extends "base" %} -*- mode: django-html -*-

{% block content %}
<div class="meta">
{% if owner %}<a id="edit" href="/{{ id }}/edit/">edit your code</a>{% endif %}
<span>Pasted at <time datetime="">{{ date }}</time></span> |
<span>Highlighted as {{ lexer }}</span>
</div>
{% for code in data %}
{{ code }}
{% endfor %}
{% endblock %}
