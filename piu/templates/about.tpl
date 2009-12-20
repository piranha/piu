{% extends "base" %} {# -*- mode: django-html -*- #}

{% block content %}
<p>That's a simple pastebin, don't hesitate to use it. ;-)</p>

<p>There is command-line <a href="/piu">utility</a>, fetch it like that:</p>

<pre><code>curl -o ~/bin/piu http://paste.in.ua/piu && chmod +x ~/bin/piu
</code></pre>
{% endblock %}
