<!doctype html> {# -*- mode: django-html -*- #}
<html lang="en">
<head>
  <meta charset="utf-8">
  <!--[if IE]>
  <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
  <![endif]-->
  <title>paste.in.ua: {{ title }}</title>
  <link rel="stylesheet" href="/static/styles/default.css">
  <script src="/static/jquery-1.3.2.min.js"></script>
</head>
<body>
  <header>
    <h1>paste.in.ua</h1>
  </header>
  {% block content %}{% endblock %}
</body>
</html>
