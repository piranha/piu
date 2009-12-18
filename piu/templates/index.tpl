{% extends "base" %} -*- mode: django-html -*-

{% set deflexer = request.COOKIES.get("lexer", "guess") %} 

{% block content %}
<form action="." method="post">
  <div id="selector">
    <select name="lexer" id="lexers">
      <option value="guess">Guess type</option>
      {%- for alias, name in lexers %}
      <option value="{{ alias }}"
              {%- if deflexer == alias %}selected{% endif %}>{{ name }}</option>
      {%- endfor %}
    </select>

    <span class="hot" rel="guess">Guess</span> |
    <span class="hot" rel="python">Python</span> |
    <span class="hot" rel="js">JavaScript</span> |
    <span class="hot" rel="rb">Ruby</span> |
    <span class="hot" rel="css">CSS</span> |
    <span class="hot" rel="html">HTML</span> |
    <span class="hot" rel="django">Django/Jinja</span>
    <span class="note">(press Ctrl-J to select from keyboard)</span>
  </div>

  <div>
    <textarea id="text" name="data" rows="20" cols="120">{{ data }}</textarea>
  </div>
  <input type="submit" value="Paste!">
  <span class="note">(or press Ctrl-Enter)</span>
</form>
<script>document.getElementById("text").focus();</script>
{% endblock %}
