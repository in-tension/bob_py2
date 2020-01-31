#!/bin/bash
cp Run_BobPy.py $AMELIA/Fiji/FijiDev.app/plugins/
cd build
jar cf bob_py.jar ./brutils/*.py ./fiji_utils/*.py ./bob_py/*.py
cp bob_py.jar $AMELIA/Fiji/FijiDev.app/plugins/
# $AMELIA/Fiji/FijiDev.app/Contents/MacOS/ImageJ-macosx -run "Run BobPy"
