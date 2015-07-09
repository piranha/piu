<!doctype html> {# -*- mode: django-html -*- #}
<html lang="en">
<head>
  <meta charset="utf-8">
  <!--[if IE]>
  <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
  <![endif]-->
  <title>paste.in.ua</title>
  <link rel="stylesheet" href="/static/main.css">
  <link rel="stylesheet" href="/static/styles/default.css">
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
  <script src="/static/main.js"></script>
</head>
<body>
  <header>
    <h1><a href="/">paste.in.ua</a></h1>
  </header>

  <div id="content">{% block content %}{% endblock %}</div>

  <div id="footer">
    <p>
      &#169; 2009-2015 <a href="http://solovyov.net/">Alexander Solovyov</a>,
      <a href="/about/">about</a>
    </p>
  </div>

<script type="text/javascript">
  var _gaq = [['_setAccount', 'UA-317760-7'], ['_trackPageview']];
  (function(d, t) {
    var g = d.createElement(t),
        s = d.getElementsByTagName(t)[0];
    g.async = g.src = '//www.google-analytics.com/ga.js';
    s.parentNode.insertBefore(g, s);
  }(document, 'script'));
</script>

</body>
</html>
