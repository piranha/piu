{% extends "base" %} -*- mode: django-html -*-

{% block content %}
<div class="meta">
  <span class="right">
    <select name="lexer" id="lexers">
      <option value="">View as</option>
      {%- for alias, name in lexers %}
      <option value="{{ alias }}"
              {%- if alias in lexer.aliases %} selected{% endif %}>{{ name }}</option>
      {%- endfor %}
    </select> |

    {% if owner -%}
    <a id="edit" href="/{{ item.id }}/edit/">edit your code</a> |
    {%- endif %}
    {% if lexer.name == "JSON" -%}
    <a href="?pretty">pretty-format JSON</a> |
    {%- endif %}
    <a id="wrap" href="#">toggle wrap</a> |
    <a href="/{{ item.id }}/raw/">raw</a>
  </span>
<span>Pasted at <time datetime="{{ date.isoformat() }}">{{ date }}</time></span> |
<span>Highlighted as {{ lexer.name }}</span>
</div>

{{ item['html'] }}

<span class="note">&uarr; Click line number to highlight;
  drag to highlight range; hold shift to select few</span>

<script type="text/javascript">
  var lexers = $id('lexers');
  var currentLexer = lexers.value;
  lexers.addEventListener('change', function(e) {
    if (currentLexer != lexers.value)
      window.location.search = "?as=" + selected.value;
  });
</script>
{% endblock %}
