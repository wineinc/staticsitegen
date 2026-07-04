#!/bin/bash

HOME=/home/wineinc/workspace/wineinc/staticsitegen
SRC=$HOME/src
BIN=/usr/bin

$BIN/python3 -m unittest discover -s $SRC
