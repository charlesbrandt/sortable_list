%image = path.load()
%image_path = image.size_path("medium")
%if not image_path.exists():
%   image.make_thumbs()
%end
%small = image_path.load()
%dimensions = small.dimensions()
%width = dimensions[0] / 2

  %#<img src="/image/{{image_path.to_relative()}}" width="{{ width }}">
  <img src="/image/{{image_path.to_relative()}}" class="content">
