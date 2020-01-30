from runpy import run_path

#import imp
##
##import brutils as br
#imp.reload(br)



cwd = '/Users/baylieslab/Documents/Amelia/code_dev/projects/bob_py/master/gui/'
#butt = run_path(cwd + 'gui_try1.py')
butt = run_path(cwd + 'mig_gui.py')

butt['bpg'].got_exper("/Users/baylieslab/Documents/Amelia/data/steffiData/150511_Lim3b-GFP_Hoe-GFP-H4K16ac-Fib-DL-Phal")
#print(butt['bpg'].dir_path)



