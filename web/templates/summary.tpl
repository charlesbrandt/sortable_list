<div data-id="{{content['name']}}" class="content item">
  <div class="thumbnail">
    %if content['image']:
    %include image_tiny path=content['image'], alt="image"
    %else:
    [{{content['path'].filename}}]
    %end
  </div>

  <div class="guide">
    <img src="/img/guide.png" class="content">

    <div class="handle">
      <!-- handle -->
    </div>

    %if content['image']:
    %#  path = content['image'].load()
    %  image_data = content['image'].to_relative()
    %else:
    %  image_data = ''
    %end

    <div class="modal" image-data="{{ image_data }}">
      <!-- modal -->
    </div>

    %if content['path'].type() == "Image":
    <a href="/image/{{content['path'].to_relative()}}">
    %elif content['path'].type() == "List":
    <a href="/text/{{content['path'].to_relative()}}">
    %else:
    <a href="/path/{{content['path'].to_relative()}}">
    %end
      <div class="follow">
        <!-- follow -->
      </div>
    </a>

  </div>  
  
</div>
