#!/bin/bash

# launch.py is availble in:
# https://github.com/charlesbrandt/moments

# path to launch.py is defined in:
# ~/.bashrc
# example .bashrc is available in moments/editors/ directory

#old way
#export PREFIX="python /c/mindstream/mindstream"
#echo "$PREFIX/launch.py -c $ROOT todo"

export ROOT=/c/public/sortable_list

launch.py -c $ROOT code

echo "Other common options:
launch.py -c $ROOT todo

#terminal:
cd web/
python application.py

#browser:
http://localhost:8888/
"

