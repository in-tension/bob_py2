
import os
import sys
import imp

cwd = '/Users/baylieslab/Documents/Amelia/code_dev/projects/bob_py/bob_py_lazy_init'
sys.path.append(cwd)


import brutils as br
imp.reload(br)
import fiji_utils as futils
imp.reload(futils)

#t = br.tic()
import bob_py
imp.reload(bob_py)

#br.ptoc(t)



exper_path = "/Users/baylieslab/Documents/Amelia/data/steffiData/150511_Lim3b-GFP_Hoe-GFP-H4K16ac-Fib-DL-Phal"
        
t = br.tic()

#bob_py.Exper.setup()

exp = bob_py.Exper(exper_path)

#print(exp.name)
print(exp)

exp.hsegs()[0].raw_stack().show()

futils.add_roi(exp.hsegs()[0].cells()[0].roi())
print(exp.hsegs()[0].cells()[0].roi())

exp.hsegs()[0].make_nucs()

#print(exp.hsegs())
#print(exp.hsegs()[0])

br.ptoc(t)





