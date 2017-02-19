<html>
<head>
  %if title:
  <title>{{ title }} - sortable</title>
  %else:
  <title>sortable</title>
  %end

  % description=''
  % keywords=''
  % author=''

  <!-- Meta Tags -->
  <meta http-equiv="content-type" content="application/xhtml+xml; charset=utf-8" />
  <meta name="robots" content="index, follow" />
  
  <meta name="description" content="{{description}}" />
  <meta name="keywords" content="{{keywords}}" />
  <meta name="author" content="{{author}}" />
  
  <!-- Favicon -->
  <link rel="shortcut icon" href="" />
  
  <!-- CSS -->
  <link rel="stylesheet" href="/css/style.css" media="screen" type="text/css" />
  <link rel="stylesheet" href="" media="print" type="text/css" />

  
  <!-- RSS -->
  <link rel="alternate" href="" title="RSS Feed" type="application/rss+xml" />

  <!-- JavaScript
  <script src=""></script>
  -->
  
  <script type="application/javascript">  
  </script>

</head>
<body>
  %include('navigation.tpl')

  %#this is utilized by rebase calls
  %#easier than passing in body from application.py
  
  {{!base}}

  %include('footer.tpl')

</body>
</html>
