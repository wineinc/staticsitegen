#!/bin/bash 

HOME=/home/wineinc/workspace/wineinc/staticsitegen
SRC=$HOME/src
BIN=/usr/bin
$BIN/python3 $SRC/main.py

cd public && python3 -m http.server 8888
