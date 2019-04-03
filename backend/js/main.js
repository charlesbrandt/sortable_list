// see also:
// /c/alpha/ajax/ajax.js

var ajax = {};

ajax.send = function (url, callback, method, data, async) {
  if (async === undefined) {
    async = true;
  }
  var request = new XMLHttpRequest();

  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      // Success!
      callback(request.responseText)
    } else {
      // We reached our target server, but it returned an error
      console.log(url, ": server returned an error");
    }
  };

  request.onerror = function() {
    // There was a connection error of some sort
      console.log(url, ": connection error");
  };

  request.open(method, url, async);
  if (method == 'POST') {
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  }
  request.send(data)
};

ajax.get = function (url, data, callback, async) {
  callback = typeof callback !== 'undefined' ? callback : function() {};
  var query = [];
  for (var key in data) {
      query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
    }
  ajax.send(url + (query.length ? '?' + query.join('&') : ''), callback, 'GET', null, async)
};

ajax.post = function (url, data, callback, async) {
  callback = typeof callback !== 'undefined' ? callback : function() {};
  var query = [];
  for (var key in data) {
    query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
  }
  ajax.send(url, callback, 'POST', query.join('&'), async)
};


var main_list = document.getElementById('sort');
var sortable = Sortable.create(main_list, {
  handle: ".handle",
  store: {
    /**
     * Get the order of elements. Called once during initialization.
     * @param   {Sortable}  sortable
     * @returns {Array}
     */
    get: function (sortable) {
      // var order = localStorage.getItem(sortable.options.group.name);
      // return order ? order.split('|') : [];

      // not implemented here
      return [];
    },

    /**
     * Save the order of elements. Called onEnd (when the item is dropped).
     * @param {Sortable}  sortable
     */
    set: function (sortable) {
      var order = sortable.toArray();
      //console.log(order);
      //localStorage.setItem(sortable.options.group.name, order.join('|'));
      var result = '';
      var item;
      for (var i=0; i < order.length; i++) {
        item = order[i];
        result += item + '\n';
      }

      // this does NOT WORK!!!
      // frequently bitten by this for construct... bah
      // for (var item in order) {
      //   console.log(item);
      //   result += item + '\n';
      // }

      var data = { 'content': result, 'format': 'list' };
      //do the ajax POST now
      var url = '/save' + path;
      //console.log(url);
      //console.log(data);
      //callback = function () {};
      ajax.post(url, data);
      //console.log(order);
    }
  },

  // onUpdate: function (evt) {
  //   var order = sortable.toArray();
  //   console.log(order);
  // }

});


var modals = document.getElementsByClassName('modal');

var change = function(value) {
  document.getElementById("position").value = value;
  var buttons = document.getElementsByClassName("vex-dialog-button-primary");
  buttons[0].click();
}

var modal_helper = function(evt) {
  (evt.target);
  //returns HTMLCollection
  var html_collection = document.getElementsByClassName('item');
  //convert that to a standard array to get access to indexOf
  var items = [].slice.call(html_collection);

  var cur_item = evt.target.parentElement.parentElement;
  var cur_pos = items.indexOf(cur_item);
  vex.dialog.open({
    // TODO:

    // should convert to using vue for the client side!

    input: [
      '<div class="vex-xcustom-field-wrapper">',
      '<input type="button" onclick="change(0)" value="first">',
      '<input type="text" id="position" name="position" style="width:80px" value="' + cur_pos + '" />',
      '<input type="button" onclick="change(' + items.length + ')" value="last">',
      '<input type="button" onclick="ajax.get(/image/' + evt.target.getAttribute('image-data') + ')" value="copy up">',
      '</div>',

      '<img src="/image/' + evt.target.getAttribute('image-data') + '" width="100%"><p>' + evt.target.getAttribute('image-data') + '</p>',
    ].join(''),
    callback: function (data) {
      if (!data) {
        return console.log('Cancelled');
      }
      //childNodes returns text nodes too...
      // end up with double the number
      //" #text "
      //console.log( main_list.childNodes[data.position] );
      console.log( data.position );
      console.log( main_list.children[data.position] );
      console.log (evt.target);
      //offset needed?
      var dest = parseInt(data.position) + 0;
      //main_list.insertBefore(main_list.childNodes[cur_pos], main_list.childNodes[dest]);
      main_list.insertBefore(main_list.children[cur_pos], main_list.children[dest]);
      //console.log('main_list.insertBefore(main_list.children[' + cur_pos + '], main_list.children[' + dest + ']);')
      //console.log(data);
      sortable.save();
    }

  })
}

for (var i = 0; i < modals.length; i++) {
  modals[i].addEventListener('click', modal_helper, false);
}
//console.log("Made it here!");
