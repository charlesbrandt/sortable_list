#!/usr/bin/env python
"""
#
# By: Charles Brandt [code at charlesbrandt dot com]
# On: [date]
# License: MIT Copyright? Copyleft? Free/BSD/GPL/Open?

# Requires:
#

# Description:
#

"""
from __future__ import print_function

import os, sys, codecs
import re
from moments.path import Path, check_ignore
from moments.sortable_list import SortableList

def usage():
    print(__doc__)

def is_path(source):
    """
    check if the supplied source is a valid path
    (this does not appear to be part of moments.path module,
     but could be relocated there)

    ** this will not match relative paths ** 
    """
    if re.match('/', source):
        return True
    else:
        return False
    
def is_url(source):
    """
    check if the supplied source is a valid URL
    """
    if re.match('http', source):
        return True
    else:
        return False

def scan_directory(path, sl, contents, current=None):
    """
    helper function...
    might need to do this in different places

    generate a generic, JSON safe, common object representation for everything
    """
    #debug helper
    #print "SORTABLE LIST:"
    #for item in sl:
    #    print item
    #print

    matched = None
    #verify the sent path.type == directory
    assert path.type() == "Directory"

    # moving to folder.sortable_list() call below
    ## #look to see if there is an existing json/list in the path
    ## #with the same name as the current directory...
    ## #if so, this may be the configuration file for the content
    ## #load that and investigate
    ## #(could also look for some standard names, like 'config.json', etc)
    ## list_file = path.name + ".list"
    ## list_path = os.path.join(str(path), list_file)
    ## if os.path.exists(list_path):
    ##     sl.load(list_path)
    ##     print "Loaded Sortable List from: %s" % list_path
    ##     #print sl

    #print dir(path)
    folder = path.load()
    #print dir(folder)

    folder.sortable_list(sl)

    folder.ignores.extend(['sized', 'action.txt', '\._*'])
    #this is called when doing a Directory.__init__
    #but we need to do it again after updating ignores
    folder.scan_directory()

    #print len(folder.contents)
    #sort by types:
    folder.scan_filetypes()
    #print len(folder.contents)

    #should still be able to apply one of these, if desired
    #folder.sort_by_date()
    folder.sort_by_path()
    #print len(folder.contents)

    #easier to work with strings at this point...
    #Paths are not being recognized as the same python object
    default_order = []
    default_order.extend( [item.path for item in folder.directories] )
    #print "default_order: %s" % len(default_order)
    default_order.extend( [item.path for item in folder.images] )
    #default_order.extend(folder.images)
    #print "default_order: %s" % len(default_order)
    default_order.extend( [item.path for item in folder.movies] )
    #default_order.extend(folder.movies)
    #print "default_order: %s" % len(default_order)
    default_order.extend( [item.path for item in folder.sounds] )
    #default_order.extend(folder.sounds)
    #print "default_order: %s" % len(default_order)

    #pick up everything else now
    #print default_order
    for remainder in folder.contents:
        #print type(remainder), remainder
        if not remainder.path in default_order:
            default_order.append(remainder.path)
        #else:
        #    print "Already had: %s" % remainder.path

    #print "default_order: %s" % len(default_order)
    #print len(default_order)

    #first reverse the order of the default...
    #next step will insert at the beginning (effectively reversing it again)
    default_order.reverse()

    #run through a similar routine as medley...
    #check for anything new...
    #add it to the beginning of the list if found:
    for cur_path in default_order:
        #print d.name
        dpath = Path(cur_path)
        if not dpath.filename in sl:
            sl.insert(0, dpath.filename)
            #sl.append(dpath.filename)

    ## print "SORTABLE LIST:"
    ## for item in sl:
    ##     print item
    ## print

    #now use the order of the sl to create corresponding content objects
    for list_item in sl:
        for cur_path in default_order:
            dpath = Path(cur_path)
            if dpath.filename == list_item:
                #create the corresponding minimal, json-friendly content objects
                
                #TODO:
                #could consider including content type here 
                if dpath.type() == "Directory":
                    #TODO:
                    #consider counting items in a directory (photos, etc):
                    #this would help for showing a summary
                    #  {{len(d.images)}} images<br>

                    d = dpath.load()
                    simple = {'name': dpath.filename, 'image': d.default_image(), 'path': dpath, 'type': 'directory'} 
                elif dpath.type() == "Image":
                    simple = {'name': dpath.filename, 'image': dpath, 'path': dpath, 'type': 'image'}
                else:
                    simple = {'name': dpath.filename, 'image': '', 'path': dpath, 'type': 'unknown'}

                contents.append( simple )
                if dpath.filename == current:
                    matched = simple
                    
    return matched

def gaze_within(source):
    """
    at this point we know we have a local path (of some kind)...
    now we need to figure out what to do with it.
    
    depending on what we find at the path,
    we want to normalize the result into a list of json 'content' objects
    these should contain all of the information needed
    for displaying any of the variations of objects that may end up on a list
    name and default image are two of the most important

    this is where you will customize based on the type of list
    the inverse will be needed on the post route

    This is also the point where you will want to scan sources
    for anything new that is not in the list
    and add it to the front of the list (or however you want to handle that)

    may need to consider an import or convert process for some types
    in order to look up more information
    and make the necessary metadata (json) files
    e.g. convert a moments list to a list of content for a given time

    """
    sl = SortableList()
    contents = []
    current = None

    #TODO:
    #check for relative path here.. fill in the blanks as needed:
    if not re.match('/', source):
        raise ValueError("Don't know how to handle relative paths yet")
    
    path = Path(source)
    
    print(path.name)
    
    if path.type() == "Directory":

        current = scan_directory(path, sl, contents)
            
        #print item.directories

        #parent = item.path.parent()
        #print parent.name
    
    elif path.type() == "JSON":
        #could load it here... loop over each object
        pass
    
    elif path.type() == "List":
        #could load it here... loop over each object
        #however, 
        #loading now happens as part of loading the path in scan_directory call
        #should choose one or the other
        #otherwise we end up with multiple copies of the list
        #if os.path.exists(source):
        #    sl.load(source)

        #now that the list has loaded, see if it's a list for the parent dir:

        if path.name == path.parent().name:
            current = scan_directory(path.parent(), sl, contents)
        else:
            #TODO
            #next option would be to look for a json file with the same name
            #if it exists, load that for content list
            print("%s != %s" % (path.name, path.parent().name))
            exit()


    else:
        #some other type of file...
        #load the parent directory in this case
        #and set this file to be the current content
        current = scan_directory(path.parent(), sl, contents, path.filename)


    #print "Sortable List: %s" % (sl)
    #print "Contents: %s" % (contents)
    
    #go ahead and save the updated version
    #(e.g. any new files found during scan)
    if sl.source:
        sl.save()

    return (sl, contents, current)
    
def gaze(source):
    """
    many things to gaze at...
    
    start by figuring out what the source is: local path or remote url?

    if local path, many options to consider... see gaze_within
    """
    #it's easier to check for urls...
    #they should all start with http
    if is_url(source):
        #can process the url here.
        #e.g. do a scrape, look for contents, etc
        pass

    #if it's a path, open it:
    #elif is_path(source):
    #rather than check (not easy to do... ), assume everything else is a path:
    else:
        #just in case a url version of a local path gets sent:
        if re.match('file://', source):
            source = source.replace('file:/', '')
        #print source

        (sl, contents, current) = gaze_within(source)


    return (sl, contents, current)

if __name__ == '__main__':
    source = None
    destination = None
    if len(sys.argv) > 1:
        helps = ['--help', 'help', '-h']
        for i in helps:
            if i in sys.argv:
                usage()
                exit()
        source = sys.argv[1]

    sl = gaze(source)




