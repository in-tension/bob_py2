import compileall
folders = ['bob_py', 'brutils', 'fiji_utils']
for folder in folders :
    compileall.compile_dir(folder)
