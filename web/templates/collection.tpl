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
      %for content in contents:
      %include summary content=content
      %end
    </div>
    
    <p style="clear:both">&nbsp;</p>
    <p>&nbsp;</p>

    <hr />
    
    %include footer
    
    <script type="application/javascript">
     var path = "{{ path }}";
    </script>
    %#<script src="/js/dragdrop.js"></script>
    <script src="/js/Sortable.min.js"></script>
    <script src="/js/main.js"></script>
    
  </body>
</html>
