#!/usr/bin/env python3
"""
Use what is available to you

    python3 -i search.py [look_for] [look_in=./]

Search is one of the most important tasks that a computer can do. And yet we so often outsource it to third party proprietary solutions. 

Ideally results show up instantly. The system can continue to scan in the background after initial options are displayed. 

I've worked on searching before. Where are those previous efforts?  

see also:
/c/charles/system/hardware/keyboard/journal.txt


leverage a database for fast look ups. However, database should be read only. An automated process should update it. 
Should be able to re-generate it automatically, so no need to transport it with source / version controlled files.  

may even want to keep a copy of files in the database. When files move on the filesystem, it may be possible to recognize this event and update the database accordingly... not sure if this is necessary though. Maybe a full re-build is the way to go?

sort applies to all on front-end? (I think so...)


TODO:
how to run python interactively AND accept commands via a web connection

i.e. run a bottle server interactively?

see also:

"""

# get standard input
# or input via request
# could be rpc
# zerorpc?

#decide what modules to load
#from moments.journal import Journal, now

import os, sys

def usage():
    print(__doc__)
    
def search(look_for='search', look_in='./'):
    print("Searching for: ", look_for)
    # start with find first?
    # then go to grep

if __name__ == '__main__':
    look_for = 'search'
    look_in = './'
    if len(sys.argv) > 1:
        helps = ['--help', 'help', '-h']
        for i in helps:
            if i in sys.argv:
                usage()
                exit()
        look_for = sys.argv[1]
        if len(sys.argv) > 2:
            look_in = sys.argv[2]

    search(look_for, look_in)

