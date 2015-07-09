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
  <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
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

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-317760-7', 'auto');
  ga('send', 'pageview');
</script>

</body>
</html>
