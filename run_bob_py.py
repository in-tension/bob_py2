
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


from ij.plugin.frame import RoiManager





#br.ptoc(t)

futils.force_close_all_images()

exper_path = "/Users/baylieslab/Documents/Amelia/data/steffiData/150511_Lim3b-GFP_Hoe-GFP-H4K16ac-Fib-DL-Phal"
        
t = br.tic()

bob_py.Exper.setup()

exp = bob_py.Exper(exper_path)





#print(exp.name)
print(exp)
h = exp.hsegs()[0]
c = h.cells()[0]
n = c.nucs()[0]

h.raw_stack().show()

#futils.add_roi(h.cells()[0].roi())
#print(h.cells()[0].roi())

#exp.hsegs()[0].create_nucs()


print(c.nucs()[0].vor_roi())



#RoiManager.addRoi()
rm = RoiManager.getRoiManager()
rm.reset()
for nuc in c.nucs() :
	futils.add_roi(nuc.roi(), nuc.name)
	futils.add_roi(nuc.vor_roi(), '_'.join([nuc.name,'vor']))
	
#	nuc.vor_roi()
	
#h.nuc_bin().flush()
h.nuc_bin().show()
#futils.wait()
#h.nuc_bin().deleteRoi()

#print(exp.hsegs())
#print(exp.hsegs()[0])

br.ptoc(t)





