
import os
import sys
import imp

cwd = '/Users/baylieslab/Documents/Amelia/code_dev/projects/bob_py/bob_py_lazy_init'
sys.path.append(cwd)


import brutils as br
imp.reload(br)
import fiji_utils as futils
imp.reload(futils)


import bob_py
imp.reload(bob_py)


from ij.plugin.frame import RoiManager





exper_path = "/Users/baylieslab/Documents/Amelia/data/steffiData/150511_Lim3b-GFP_Hoe-GFP-H4K16ac-Fib-DL-Phal"
        
t = br.tic()

bob_py.Exper.setup()


exp = bob_py.Exper(exper_path)


print(exp)

h = exp.hsegs()[0]
c = h.cells()[0]
n = c.nucs()[0]

cell_roi_dict = h.get_roi_dict("Cell")
#print(cell_roi_dict)






br.ptoc(t)





