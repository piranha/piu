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
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.0/jquery.min.js"></script>
  <script src="/static/shortcut.js"></script>
  <script src="/static/main.js"></script>
</head>
<body>
  <header>
    <h1><a href="/">paste.in.ua</a></h1>
  </header>

  <div id="content">{% block content %}{% endblock %}</div>

  <div id="footer">
    <p>
      &#169; 2009-2010 <a href="http://piranha.org.ua">Alexander Solovyov</a>,
      <a href="/about/">about</a>
    </p>
  </div>

<script type="text/javascript">
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-317760-7']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script');
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' :
        'http://www') + '.google-analytics.com/ga.js';
    ga.setAttribute('async', 'true');
    document.documentElement.firstChild.appendChild(ga);
  })();
</script>

</body>
</html>
