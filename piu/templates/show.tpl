{% extends "base" %} -*- mode: django-html -*-

{% block content %}
<div class="meta">
  <span class="right">
    {% if owner -%}
    <a id="edit" href="/{{ id }}/edit/">edit your code</a> |
    {%- endif %}
    <a href="/{{ id }}/raw/">raw</a>
  </span>
<span>Pasted at <time datetime="{{ date.isoformat }}">{{ date }}</time></span> |
<span>Highlighted as {{ lexer }}</span>
</div>
{% for code in data %}
{{ code }}
{% endfor %}
{% endblock %}
