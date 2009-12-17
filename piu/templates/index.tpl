{% extends "base" %} -*- mode: django-html -*-

{% block content %}
<form action="." method="post">
  <div id="lexers">
    <select name="lexer" id="id-lexer">
      <option value="guess">Guess type</option>
      {%- for alias, name in lexers %}
      <option value="{{ alias }}"
              {%- if deflexer == alias %}selected{% endif %}>{{ name }}</option>
      {%- endfor %}
    </select>

    <span class="hot python">Python</span>
    <span class="hot js">JavaScript</span>
    <span class="hot ruby">Ruby</span>
    <span class="hot css">CSS</span>
    <span class="hot django">Django/Jinja</span>
  </div>

  <div><textarea name="data" rows="20" cols="120"></textarea></div>
  <input type="submit" value="Paste!">
</form>
{% endblock %}
