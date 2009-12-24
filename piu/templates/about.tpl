{% extends "base" %} {# -*- mode: django-html -*- #}

{% block content %}
<p>That's a simple pastebin, don't hesitate to use it. ;-)</p>

<h3 id="selections"><a href="#selections">Selections</a></h3>

<p>This is neat unique feature - if you have <code>'#l-num'</code> in url,
  corresponding line will be highlighted. Of course, you can get such url just
  by clicking on line number.</p>
<p>But more than that, if you will try to select some line numbers with mouse
  (it's ok to finish selection on line itself, not on line number), you'll end
  with something like <code>'#l-num1:l-num2'</code> in url and corresponding
  lines highlighted.</p>
<p>And finally, we've got an awesome feature - you can select few such ranges
  (or supply them by hands in URL, of course ;-). Just press and hold Control or
  Shift when selecting new range and instead of replacing it will be added to
  your current ranges</p>

<h3 id="api"><a href="#api">API</a></h3>

<p>
  API is dead simple, it's just a POST request to
  a <code>'http://paste.in.ua/'</code> with single required parameter -
  <code>'data'</code>. Supply a <code>'lexer'</code> to choose a lexer, it's
  default to <code>'guess'</code>.
</p>

<h3 id="tools"><a href="#tools">Ready tools</a></h3>

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
