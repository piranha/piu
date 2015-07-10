{% extends "base" %} -*- mode: django-html -*-

{% block content %}
<form action="." method="post">
  <div class="meta">
    <select name="lexer" id="lexers">
      <option value="guess">Guess type</option>
      {%- for alias, name in lexers %}
      <option value="{{ alias }}"
              {%- if deflexer == alias %} selected{% endif %}>{{ name }}</option>
      {%- endfor %}
    </select>

    <a class="hot" href="#" rel="guess">Guess</a> |
    <a class="hot" href="#" rel="text">Text</a> |
    <a class="hot" href="#" rel="python">Python</a> |
    <a class="hot" href="#" rel="js">JavaScript</a> |
    <a class="hot" href="#" rel="rb">Ruby</a> |
    <a class="hot" href="#" rel="css">CSS</a> |
    <a class="hot" href="#" rel="html">HTML</a> |
    <a class="hot" href="#" rel="django">Django/Jinja</a>
    <span class="note">(press Ctrl-J to put focus on selectbox)</span>
  </div>

  <div>
    <textarea id="text" name="data" rows="20" cols="120" autofocus>{{ data }}</textarea>
  </div>
  <input type="submit" value="Paste!">
  <span class="note">(or press Ctrl-Enter)</span>
</form>
<script type="text/javascript">
  document.addEventListener('DOMContentLoaded', function() {
      if (!("autofocus" in document.createElement("input"))) {
          document.getElementById("text").focus();
      }
  });
</script>
{% endblock %}
