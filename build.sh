#!/bin/bash

cp Run_BobPy.py $AMELIA/Fiji/FijiRun.app/plugins/

cd build


jython compile.j.py

jar cf bob_py.jar ./brutils/* ./bob_py/resources/*.png ./fiji_utils/* ./bob_py/*

rm $AMELIA/Fiji/FijiRun.app/plugins/bob_py.jar
mv bob_py.jar $AMELIA/Fiji/FijiRun.app/plugins/

$AMELIA/Fiji/FijiRun.app/Contents/MacOS/ImageJ-macosx -run "Run BobPy"
