#!/bin/bash

cp Run_BobPy.py ~/Desktop/FijiRun.app/plugins/

cd build


jython compile.j.py

jar cf bob_py.jar ./brutils/* ./bob_py/resources/*.png ./fiji_utils/* ./bob_py/*

rm ~/Desktop/FijiRun.app/plugins/bob_py.jar
mv bob_py.jar ~/Desktop/FijiRun.app/plugins/

~/Desktop/FijiRun.app/Contents/MacOS/ImageJ-macosx -run "Update..."
