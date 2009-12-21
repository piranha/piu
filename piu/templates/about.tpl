{% extends "base" %} {# -*- mode: django-html -*- #}

{% block content %}
<p>That's a simple pastebin, don't hesitate to use it. ;-)</p>

<p>There is command-line <a href="/piu">utility</a>, fetch it like that:</p>

<pre><code>curl -o ~/bin/piu http://paste.in.ua/piu && chmod +x ~/bin/piu</code></pre>

<p>Features:</p>
<ul>
  <li>determine file type by extension</li>
  <li>determine file type by analyzing input data</li>
  <li>automatically copy url to clipboard using either xclip or pbcopy
    (whichever is available on your system).</li>
</p>
{% endblock %}
