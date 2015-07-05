{% extends "base" %} {# -*- mode: django-html -*- #}

{% block content %}
<p>That's a simple pastebin, don't hesitate to use it. ;-) In case you want your
  own, sources are on <a href="https://github.com/piranha/piu">Github</a>.</p>

<h2 id="selections"><a href="#selections">Selections</a></h2>

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

<h2 id="shortcuts"><a href="#shortcuts">Shortcuts</a></h2>

<p>There are few shortcuts for convenience:</p>

<dl>
  <dt>Ctrl-Enter</dt>
  <dd>Create a paste (but only if textarea is not empty)</dd>

  <dt>Ctrl-J</dt>
  <dd>Jump to a lexer selection</dd>

  <dt>Ctrl-N</dt>
  <dd>Create new paste</dd>
</dl>

<h2 id="pretty"><a href="#pretty">Prettification</a></h2>

<p>If you have pasted JSON, you'll have option to prettify it (look at top-right
  corner). Just in case you have some ugly one.</p>

<h2 id="api"><a href="#api">API</a></h2>

<p>
  API is dead simple, it's just a POST request to
  a <code>'http://paste.in.ua/'</code> with single required parameter -
  <code>'data'</code>. Supply a <code>'lexer'</code> to choose a lexer; it's
  default to <code>'guess'</code>.
</p>

<h2 id="tools"><a href="#tools">Tools</a></h2>

<h3 id="piu"><a href="#piu">Command line</a></h3>

<p>You can fetch command-line <a href="/piu">utility</a> like that:</p>

<pre><code>curl -o ~/bin/piu http://paste.in.ua/piu && chmod +x ~/bin/piu</code></pre>

<p>Features:</p>
<ul>
  <li>determine file type by extension</li>
  <li>determine file type by analyzing input data</li>
  <li>automatically copy url to clipboard using either xclip or pbcopy
    (whichever is available on your system).</li>
</ul>

<p>Usage:</p>

<pre><code>&gt; piu somefile.py
&gt; cat file | piu
&gt; hg export tip | piu
</code></pre>

<h3 id="piu-el"><a href="#piu-el">Emacs</a></h3>

<p>Also we have small nice <a href="/piu.el">piece of code</a> for Emacs;
download and put it somewhere in your Emacs' <code>'load-path'</code>. Comments
about usage are inside the file itself.</p>

{% endblock %}
