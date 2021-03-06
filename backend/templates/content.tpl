<html>
  <head>
    <title>{{ c['path'].name }}</title>
    %include('header.tpl', description='', keywords='', author='')
    
    <script type="text/javascript">      
    </script>
    
  </head>
  <body>
    <!-- navigation / header -->
    <div style="float: right" id="actions">
      <img src="/img/menu.svg" width="50">
    </div>
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
      %#{{ c['path'].type() }}, {{ c['content']['type'] }}
      %if c['path'].type() == "Movie":
      <video id="main_movie" class="video-js vjs-default-skin"
         controls preload="auto" width="100%" height="90%"
         poster="/image/{{ c['content']['image'] }}"
         data-setup='{"example_option":true}' loop>
        <source src="/file/{{c['path'].to_relative()}}" type="video/webm" />
        <p class="vjs-no-js" >Video requires javascript and HTML5 video</p>
      </video>
      %elif c['path'].type() == "Sound":
      <audio id="player" preload="auto" tabindex="0" controls="" type="audio/mpeg">
        <source type="audio/mp3" src="/file/{{c['path'].to_relative()}}">
        Sorry, your browser does not support HTML5 audio.
      </audio>
          
      %elif c['path'].type() == "Image":
        <img src="/image/{{c['path'].to_relative()}}" width="100%">      
      %else:
        Not sure how to render: {{c['path'].to_relative()}}
      %end
      
      
    </div>
    
    <p style="clear:both">&nbsp;</p>
    <p>&nbsp;</p>

    % pass # <hr />
    % pass # include footer
    
    <script type="application/javascript">
     var path = "{{ c['path'] }}";
    </script>
    <script src="/js/content.js"></script>
    
  </body>
</html>
