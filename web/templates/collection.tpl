<html>
  <head>
    <title>{{ path.name }}</title>
    %include header description='', keywords='', author=''  
    
    <script type="text/javascript">      
    </script>
    
  </head>
  <body>
    <h3>
      <a href="/">*</a>/
      %parts = path.relative_path_parts()
      %if len(parts):
      %for part in parts[:-1]:
      <a href="/path/{{part[1]}}">{{part[0]}}</a>/
      %end
      {{parts[-1][0]}}
      %end
    </h3>

    <div id="sort">
      %for content in collection:
      %include summary content=content
      %end
    </div>
    
    <p style="clear:both">&nbsp;</p>
    <p>&nbsp;</p>

    % pass # <hr />
    % pass # include footer
    
    
    <script type="application/javascript">
     var path = "{{ path }}";
    </script>
    <script src="/js/vex.combined.min.js"></script>
    <script>vex.defaultOptions.className = 'vex-theme-wireframe'</script>
    <link rel="stylesheet" href="/css/vex.css" />
    <link rel="stylesheet" href="/css/vex-theme-wireframe.css" />

    <script src="/js/Sortable.min.js"></script>
    <script src="/js/main.js"></script>
    
  </body>
</html>
