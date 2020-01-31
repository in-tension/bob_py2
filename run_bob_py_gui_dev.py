
import os
import sys
import imp
from pprint import pprint

#cwd = '/Users/baylieslab/Documents/Amelia/code_dev/projects/bob_py/master'
#sys.path.append(cwd)


##from draw_package import *
#
#draw_package_path = os.path.join(cwd, 'draw_package.py')
#print('python3 {}'.format(draw_package_path))
#os.system('python3 {}'.format(draw_package_path))
#

#die
import brutils as br
imp.reload(br)
import fiji_utils as futils
imp.reload(futils)


import bob_py
imp.reload(bob_py)


from ij.plugin.frame import RoiManager



#from .bob_py_gui import BobGui

exper_path = "/Users/baylieslab/Documents/Amelia/data/steffiData/150511_Lim3b-GFP_Hoe-GFP-H4K16ac-Fib-DL-Phal"

#t = br.tic()

#bob_py.Exper.setup()

bpg = bob_py.BobGui()
bpg.got_exper(exper_path)


#br.ptoc(t)
