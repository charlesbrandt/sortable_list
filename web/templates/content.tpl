<html>
  <head>
    <title>{{ c['path'].name }}</title>
    %include header description='', keywords='', author=''  
    
    <script type="text/javascript">      
    </script>
    
  </head>
  <body>
    <!-- navigation / header -->
    <div style="float: right">
      <a href="/path/{{c['previous']['path']}}">previous</a>
      <input name="position" value="{{c['index']}}">
      <a href="/path/{{c['next']['path']}}">next</a>
    </div>
    <h3>
      <a href="/">*</a>/
      %parts = c['path'].relative_path_parts()
      %if len(parts):
      %for part in parts[:-1]:
      <a href="/path/{{part[1]}}">{{part[0]}}</a>/
      %end
      {{parts[-1][0]}}
      %end
    </h3>

    
    <div id="details">
      %loaded = c['path'].load()
      {{ c['path'].type() }}
      <img src="/image/{{c['path'].to_relative()}}" width="100%">
      
    </div>
    
    <p style="clear:both">&nbsp;</p>
    <p>&nbsp;</p>

    <hr />
    
    %include footer
    
    <script type="application/javascript">
     var path = "{{ c['path'] }}";
    </script>
    <script src="/js/content.js"></script>
    
  </body>
</html>
