#!/bin/bash
cp Run_BobPy.py $AMELIA/Fiji/FijiRun.app/plugins/
cd build
jar cf bob_py.jar ./brutils/* ./fiji_utils/* ./bob_py/*
rm $AMELIA/Fiji/FijiRun.app/plugins/bob_py.jar
mv bob_py.jar $AMELIA/Fiji/FijiRun.app/plugins/

# $AMELIA/Fiji/FijiRun.app/Contents/MacOS/ImageJ-macosx -run "Run BobPy"

$AMELIA/Fiji/FijiRun.app/Contents/MacOS/ImageJ-macosx -run "/Users/baylieslab/Documents/Amelia/code_dev/projects/bob_py/master/run_bob_py_gui_dev.py"
