#!/usr/bin/env python
"""
Help handle backend processes for storing sortable list results

separate tab:
cd /c/public/sortable_list/web
python application.py 
"""

import sys, os, re

from bottle import static_file, redirect
from bottle import get, post, request
from bottle import route, run
from bottle import template


#DO NOT USE THIS IN PRODUCTION!!
import bottle
bottle.debug(True)

server_root = os.path.dirname(os.path.realpath(__file__))
#print "Server root: %s" % server_root

#for importing sortable_list
sys.path.append(os.path.dirname(server_root))
from gaze import gaze

#default is "./views/" directory
template_path = os.path.join(server_root, 'templates')
#bottle.TEMPLATE_PATH.append('./templates/')
bottle.TEMPLATE_PATH.append(template_path)

try:
    import simplejson as json
except:
    try:
        import json
    except:
        print "No json module found"
        exit()
        
from moments.path import Path
from moments.launch import edit, file_browse

server = bottle.Bottle()


# GLOBALS:
#this is equivalent to main() function in template_script.py

#requires that at least one argument is passed in to the script itself
#(through sys.argv)
ignores = []

port = 8888
path_root = "/path/to/some/safe/location/"
#this is not a safe path, but it's convenient
path_root = "/"


# ROUTES

#Be careful when specifying a relative root-path such as root='./static/files'.
#The working directory (./) and the project directory are not always the same.
#@route('/css/:filename')
@server.route('/css/:filename#.+#')
#@route('/css/style.css')

def css_static(filename):
    css_path = os.path.join(server_root, 'css')
    print css_path
    #return static_file(filename, root='./css')
    return static_file(filename, root=css_path)

@server.route('/js/:filename#.+#')
def js_static(filename):
    js_path = os.path.join(server_root, 'js')
    return static_file(filename, root=js_path)

@server.route('/img/:filename#.+#')
def images_static(filename):
    image_path = os.path.join(server_root, 'img')
    return static_file(filename, root=image_path)
  
 
@server.route('/path/launch/:source#.+#')
def launch_path(source=''):
    global path_root
    path = Path(path_root + source, relative_prefix=path_root)

    #just assume the whole thing has been sent
    #path = Path(source)

    response = ''
    if path.type() == "Log":
        edit(path)
        response += "editing: %s<br>" % path
    elif path.type() == "Directory":
        file_browse(path)
        response += "browsing: %s<br>" % path
    else:
        response += "unknown type: %s for: %s<br>" % (path.type(), path)

    response += "LAUNCH PATH: %s<br>" % source
    return response


#to force a download, use the following:
#    return static_file(filename, root='/path/to/static/files', download=filename)


@server.post('/save/:relative#.+#')
@server.post('/save/')
@server.post('/save')
def save(relative=''):
    """
    
    """
    global path_root

    if re.match('~', relative):
        relative = os.path.expanduser(relative)

    if not relative:
        #could set a default here if it is desireable
        print "NO DESTINATION SENT!"
    elif not re.match('/', relative):
        relative = path_root + relative

    
    #destination = Path(relative, relative_prefix=path_root)
    #now check if the destination is a directory...
    #in that case, create a sortable.list name in the directory
    if os.path.isdir(relative):
        path = Path(relative)
        name = path.name + ".list"
        destination = os.path.join(relative, name)
    else:
        destination = relative

    #print destination
    
    #debug:
    #print dir(request.forms)
    #print "Keys: %s" % (request.forms.keys())
    #print "Values: %s" % (request.forms.values())
    
    #gets a string
    #could be json or text / list
    content = request.forms.get('content')

    save_as = request.forms.get('format')

    if save_as in ["list"]:
        dest_file = open(destination, 'w')
        #print "opened: ", destination
        #print "writing (raw): ", content
        dest_file.write(content)
        dest_file.close()
        print "saved content to: ", destination
    ## elif save_as == "json":
    ##     #could also do something like:
    ##     ordered_list = json.loads(content)
    ##     save_json(destination, ordered_list)
    ##     #but that seems like the same thing as above

    #return "Success!"
    #redirect("/text" + relative)
    redirect("/path" + relative)



@server.route('/image/:relative#.+#')
def image(relative=''):
    """
    """
    global path_root

    #if not re.match('/', relative):
    #    relative = os.path.join(path_root, relative)

    #print "SHOWING IMAGE: %s" % relative
    path = Path(relative, relative_prefix=path_root)
    if path.type() == "Image":
        return static_file(relative, root=path_root)
    else:
        #TODO: raise 404
        pass


def expand_relative(relative):
    global path_root

    if re.match('~', relative):
        relative = os.path.expanduser(relative)
    ## else:
    ##     relative = os.path.join('/', relative)
    ##     full = os.path.abspath(relative)
    ## print full

    full_path = os.path.join(path_root, relative)

    return full_path

@server.route('/text/:relative#.+#')
def text(relative=''):
    """
    load a text editor
    start with just a simple form

    this is a low level way of sorting a text based list...
    just edit the order and save the results
    """
    global path_root

    #if not re.match('/', relative):
    #    relative = os.path.join(path_root, relative)

    full_path = expand_relative(relative)

    print "Editing Text: %s" % relative
    path = Path(full_path, relative_prefix=path_root)
    contents = file(full_path).read()
    if path.type() in [ "Text", "List", "JSON" ]:
        return template('editor', path=path, contents=contents)

    else:
        #TODO: raise 404
        pass

@server.route('/path/:relative#.+#')
@server.route('/path/')
@server.route('/path')
def path(relative=''):
    """
    serve a path ... either a directory or a file

    !!! WARNING !!!
    this allows the app to function as a customizable file system browser
    be careful with what you set path_root to.
    If the machine you run this on has sensitive information
    and is connected to a public network, it's available
    """
    global path_root

    if re.match('~', relative):
        relative = os.path.expanduser(relative)
    ## else:
    ##     relative = os.path.join('/', relative)
    ##     full = os.path.abspath(relative)
    ## print full

    full_path = os.path.join(path_root, relative)
    path = Path(full_path, relative_prefix=path_root)

    (sl, collection, current) = gaze(full_path)
    if current:
        #might be able to figure these details out in javascript
        #but for now:
        index = collection.index(current)
        if index != 0:
            previous_item = collection[index-1]
        else:
            previous_item = collection[-1]

        if index != len(collection)-1:
            next_item = collection[index+1]
        else:
            next_item = collection[0]

        context = { "path": path,
                    "collection": collection,
                    "content": current,
                    "index": index,
                    "previous": previous_item,
                    "next": next_item,
                    }
            
        return template('content', c=context)
    else:
        return template('collection', path=path, collection=collection)

@server.route('/now')
def now(relative=''):
    return template('now')

@server.route('/')
def index():
    global path_root
    return template('home', path_root=path_root)

if __name__ == '__main__':
    #default host:
    host = "localhost"
    
    if len(sys.argv) > 1:
        helps = ['--help', 'help', '-h']
        for i in helps:
            if i in sys.argv:
                print "python application.py --context [directory to load] [address]"
                exit()

        proots = ['--root', '-r', '-c', '--context']
        for p in proots:
            if p in sys.argv:
                i = sys.argv.index(p)
                sys.argv.pop(i)
                path_root = sys.argv.pop(i)
                sys.argv.pop(i)

        ports = ['--port', '-p']
        for p in ports:
            if p in sys.argv:
                i = sys.argv.index(p)
                sys.argv.pop(i)
                port = sys.argv.pop(i)
                sys.argv.pop(i)

        hosts = ['--host', '-h', '--address', '-a']
        for h in hosts:
            if h in sys.argv:
                i = sys.argv.index(h)
                sys.argv.pop(i)
                host = sys.argv.pop(i)
                sys.argv.pop(i)

        # if we still have something left, assume it's an address
        if len(sys.argv) > 1:
            host = sys.argv[1]

    print "Path root: %s" % path_root
    
    #start the server loop
    #reloader=True enables Auto Reloading
    #run(app=server, host='localhost', port=port, reloader=True)
    run(app=server, host=host, port=port, reloader=True)
