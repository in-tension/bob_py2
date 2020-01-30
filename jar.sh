cd build
jar cf bob_py.jar ./brutils/* ./fiji_utils/* ./bob_py/*
mv bob_py.jar $AMELIA/Fiji/FijiRun.app/plugins/
$AMELIA/Fiji/FijiRun.app/Contents/MacOS/ImageJ-macosx -run "Run BobPy"
