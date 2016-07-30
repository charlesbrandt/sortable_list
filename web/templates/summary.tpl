<div data-id="{{content['name']}}" class="content">
  %if content['image']:
  <div class="thumbnail">
    %include image_tiny path=content['image'], alt="image"
  </div>
  <div class="handle">
    <!-- handle -->
  </div>
  <div class="expand">
    <!-- expand -->
  </div>

  %if content['path'].type() == "Image":
  <a href="/image/{{content['path'].to_relative()}}">
  %else:
  <a href="/path/{{content['path'].to_relative()}}">
  %end
    <div class="follow">
      <!-- follow -->
    </div>
  </a>
  
  %else:
  <div style="clear: both">
    %if content['path'].type() == "List":
    <a href="/text/{{content['path'].to_relative()}}">
    %else:
    <a href="/path/{{content['path'].to_relative()}}">
    %end    
      [{{content['path'].filename}}]
    </a>
  </div><br>
  %end
</div>
