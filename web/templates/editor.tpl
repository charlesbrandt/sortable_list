<html>
<head>
  <title>{{ path.name }}</title>
  %include header description='', keywords='', author=''

  %#<h1> <a href="/path/{{ parent }}">{{parent.name}}</a> </h1>
</head>
<body>

  <form action="/save/{{ path }}" method="POST">
    <textarea name="content" cols="80" rows="45">{{ contents }}</textarea>
    <input type="hidden" name="format" value="list">
    <input type="submit" value="Save">
  </form>
</body>
</html>
