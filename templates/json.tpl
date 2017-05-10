<html>
<head>
  <title>{{ path.name }}</title>
  %include('header.tpl', description='', keywords='', author='')

  %#<h1> <a href="/path/{{ parent }}">{{parent.name}}</a> </h1>
</head>
<body>
  <a href="/text{{ path }}">{{path.filename}}: edit raw version</a>

  %locations = items.pop('locations', [])
  %for location in locations:
  <div><a href="/path{{ location }}">{{ location }}</a></div>
  %end

  
  %for key, value in items.items():
  <div>{{ key }}: {{ value }}<br><br></div>
  %end
  

</body>
</html>
