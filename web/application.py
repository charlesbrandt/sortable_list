#!/usr/bin/env python
"""
Pose server that uses a separate server to access journal data
that way journal data does not need to be reloaded every time server restarts

does make startup more complex:

separate tab:
cd /c/moments/moments
python journal_server.py /c/journal

python application-split.py
"""

import sys, os, re, codecs
import urllib, urllib2

#redefine standard python range:
pyrange = range

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
        
from moments.log import Log
from moments.path import Path
from moments.tag import Tags
from moments.association import Association
from moments.journal import Journal
from moments.timestamp import Timerange

from moments.journal import RemoteJournal

from moments.launch import edit, file_browse

from mindstream.cloud import Cloud
#from moments.mindstream import Mindstream


server = bottle.Bottle()


# GLOBALS:
#this is equivalent to main() function in template_script.py

#requires that at least one argument is passed in to the script itself
#(through sys.argv)
ignores = []

port = 8888
path_root = '/c/moments/tests/'
path_root = "/c/binaries/journal/2010/"
path_root = "/c/"
path_root = "/"

if len(sys.argv) > 1:
    helps = ['--help', 'help', '-h']
    for i in helps:
        if i in sys.argv:
            print "python application.py [directory to load]"
            exit()

    ports = ['--port', '-p']
    for p in ports:
        if p in sys.argv:
            i = sys.argv.index(p)
            sys.argv.pop(i)
            port = sys.argv.pop(i)

    proots = ['--root', '-r', '-c', '--context']
    for p in proots:
        if p in sys.argv:
            i = sys.argv.index(p)
            sys.argv.pop(i)
            path_root = sys.argv.pop(i)


print "Path root: %s" % path_root


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

@server.route('/images/:filename#.+#')
def images_static(filename):
    image_path = os.path.join(server_root, 'images')
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


def load_groups(full_source):
    """
    allows for custom editing of json files if needed
    """
    groups = []
    if not os.path.exists(full_source):
        #to get original version started
        #collections.scenes should have been loaded already
        #and star_order calculated

        raise ValueError, "No order file: %s" % full_source

        #comment this out if you want to initialize a list from scratch:
        #groups = [ self.scenes.star_order, [], [], [], [], [], [], [], [], [], [], ]
    else:
        #destination = "order.txt"
        json_file = codecs.open(full_source, 'r', encoding='utf-8', errors='ignore')
        lines = json_file.readlines()
        #split up the object so it is easier to edit
        split = ''
        for line in lines:
            line = line.replace(',]', ']')
            line = line.replace(', ]', ']')
            split += line.strip() + ' '

        #split = json_file.read()
        #split.replace('\r\n', '')
        #split.replace('\r', '')
        #split.replace('\n', '')
        #print split
        try:
            groups = json.loads(split)
        except:
            #try to pinpoint where the error is occurring:
            print split

            #get rid of outer list:
            split = split[1:-1]
            parts = split.split('], ')
            assert len(parts) == 11
            count = 0
            for p in parts:
                p = p + ']'
                try:
                    group = json.loads(p)
                except:
                    new_p = p[1:-1]
                    tags = new_p.split('", "')
                    summary = ''
                    for tag in tags:
                        summary += tag + "\n"

                    #print count
                    #print summary
                    print "%s - %s" % (count, summary)
                    #raise ValueError, "Trouble loading JSON in part %s: %s" % (count, p)
                    raise ValueError, "Trouble loading JSON in part %s: %s" % (count, summary)
                count += 1


            #raise ValueError, "Trouble loading JSON: %s" % split
        json_file.close()
        #groups = load_json(destination)

    return groups


def save_groups(destination, ordered_list):
    """
    similar to save json, but custom formatting to make editing easier

    to load, use collection.load_groups
    
    """
    #print "Saving: %s" % ordered_list
    #print "To: %s" % destination
    #journal = merge_simple(ordered_list, cloud_file)

    json_file = codecs.open(destination, 'w', encoding='utf-8', errors='ignore')
    #print "JSON FILE OPEN"
    split = json.dumps(ordered_list)
    split = split.replace('], ', ', ], \n')
    split = split.replace(']]', ', ]]')
    #print "Split version: %s" % split
    json_file.write(split)
    json_file.close()    
        

@server.post('/save_tabs/:relative#.+#')
@server.post('/save_tabs/')
@server.post('/save_tabs')
def save_tabs(relative=''):
    global path_root

    if re.match('~', relative):
        relative = os.path.expanduser(relative)

    if not relative:
        #could set a default here if it is desireable
        print "NO DESTINATION SENT!"
    elif not re.match('/', relative):
        relative = path_root + relative

    
    #destination = Path(relative, relative_prefix=path_root)
    destination = relative

    #print destination
    
    #debug:
    #print dir(request.forms)
    #print "Keys: %s" % (request.forms.keys())
    #print "Values: %s" % (request.forms.values())
    
    #gets a string
    cloud    = request.forms.get('cloud')
    #gets a list
    #cloud    = request.forms.getlist('cloud[]')
    
    #print cloud
    ordered_list = json.loads(cloud)

    #print ordered_list

    #save_json(destination, ordered_list)
    save_groups(destination, ordered_list)
    
    #d = open(destination, 'w')
    #d.write(' '.join(ordered_list))
    
    #return "Name: %s, Password: %s" % (name, password)
    return "Success!"

@server.route('/sort/:relative#.+#')
def sort(relative=''):
    """
    accept a path to a moment log and enable sorting on the items
    using jquery ui for a drag and drop interface
    """
    global path_root

    if re.match('~', relative):
        relative = os.path.expanduser(relative)
    if not re.match('/', relative):
        relative = path_root + relative

    #set some defaults here...
    #if they've been changed, this will get over written on load
    groups = { "all":[], "edit":[], "slide1":[], "slide2":[], "slide3":[], "slide4":[], "slide5":[], "slide6":[], "slide7":[], "slide8":[], "slide9":[], }

    tab_order = ['all', 'edit', "slide1", "slide2", "slide3", "slide4", "slide5", "slide6", "slide7", "slide8", "slide9"]

    path = Path(relative, relative_prefix=path_root)
    print path
    if path.exists() and path.type() == "Directory":
        response = "Error: need a file name to store the meta data in<br>"
        response = "You supplied a directory path: %s<br>" % path
        return response
    else:
        parent_directory = path.parent()
        if path.extension == ".txt":
            #create a text journal if we don't have one
            if not path.exists():
                #convert images to journal
                #print "PARENT: %s" % parent_directory
                directory = parent_directory.load()
                #print "directory: %s, of type: %s" % (directory, type(directory))
                directory.create_journal(journal=path.filename)
                #journal = path.load_journal(create=True)

            journal = path.load_journal()
            items = []
            for e in journal.entries():
                new_p = os.path.join(str(parent_directory), e.data.strip())
                #print new_p
                p = Path(new_p)
                #print p.exists()
                items.append(p)

            #initial version of groups:
            destination = Path(relative)
            destination.extension = '.json'

            groups['all'] = items
            
        elif path.extension == ".json":
            #we can make the initial version here...
            #skip the generation of a moments log step
            if not path.exists():
                directory = parent_directory.load()
                #print "directory: %s, of type: %s" % (directory, type(directory))
                directory.sort_by_date()
                directory.scan_filetypes()
                
                groups['all'] = directory.images
                
            else:
                loaded = load_groups(str(path))
                #template expects all items in groups to be Path objects.
                #do that now
                groups = {}
                for key, value in loaded.items():
                    groups[key] = []
                    for v in value:
                        groups[key].append(Path(v))
            
            destination = Path(relative)

        else:
            #dunno!
            print "UNKNOWN FILE TYPE: %s" % relative
            groups = {}
            destination = None

        #clean up tab_order as needed
        for key in groups.keys():
            if not key in tab_order:
                tab_order.append(key)
        for item in tab_order[:]:
            if item not in groups.keys():
                tab_order.remove(item)

        print tab_order
        
        #return template('sort', path=path, items=items)
        return template('sort', path=path, groups=groups, destination=destination, tab_order=tab_order)
    
@server.route('/series/:type/:relative#.+#')
@server.route('/series/:relative#.+#')
@server.route('/series/')
@server.route('/series')
def series(type="Image", relative=''):
    """
    show the current item in a series
    along with links to previous and next
    """
    global path_root

    if re.match('~', relative):
        relative = os.path.expanduser(relative)
    if not re.match('/', relative):
        relative = os.path.join(path_root, relative)

    path = Path(relative, relative_prefix=path_root)
    if path.type() != "Directory":
        parent = path.parent()
        parent_dir = parent.load()
        #parent_dir.sort_by_date()
        parent_dir.sort_by_path()
        parent_dir.scan_filetypes()
        if path.type() == "Image":
            count = 0
            position = None
            for i in parent_dir.images:
                if str(i) == str(path):
                    position = count
                    break
                count += 1

            if position is None:
                raise ValueError, "Couldn't find matching image in directory: %s" % str(parent)
            else:
                if position != 0:
                    prev_pos = position-1
                else:
                    prev_pos = 0
                previous = parent_dir.images[prev_pos]

                nexts = []
                next_len = 5
                end = position + next_len
                if end >= len(parent_dir.images):
                    nexts = parent_dir.images[position+1:]
                else:
                    nexts = parent_dir.images[position+1:end]

                return template('series', path=path, parent=parent, previous=previous, nexts=nexts)


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
    serve a static file

    this also allows pose to function as a customizable file system browser

    be careful with what you set path_root to
    if the machine you run this on has sensitive information
    and is connected to a public network
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

    (sl, contents) = gaze(full_path)
    return template('collection', path=path, contents=contents)

@server.route('/now')
def now(relative=''):
    return template('now')

@server.route('/')
def index():
    global path_root
    return template('home', path_root=path_root)
    
#port = 8088
#start the server loop
#run(host='localhost', port=8088)
#run(app=server, host='localhost', port=port)
#reloader=True enables Auto Reloading
#run(host=configs['host'], port=configs['port'], reloader=True)
run(app=server, host='localhost', port=port, reloader=True)
