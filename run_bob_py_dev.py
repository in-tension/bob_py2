
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





#exper_path = "/Users/baylieslab/Documents/Amelia/data/steffiData/150511_Lim3b-GFP_Hoe-GFP-H4K16ac-Fib-DL-Phal"

exper_path = "/Users/baylieslab/Desktop/200130_w1118-18C"
t = br.tic()

#bob_py.Exper.setup()

#1/0
exp = bob_py.Exper(exper_path)
h = exp.hsegs()[1]
c = h.cells()[0]
n = c.nucs()[0]

#h.raw_stack().show()
exp.make_data()

#1/0

#h.raw_stack().show()
#
#
#sb = br.SimilarityBuilder() 
#
#for hseg in exp.hsegs() :
#	all_file_dict = hseg.file_dict()
#	all_file_dict.update(hseg.cell_file_dict())
#	all_file_dict.update(hseg.bin_file_dict())
#	sb.add_group(hseg.name, all_file_dict)
#
#simprofile, comparisons = sb.simprofile_comparison()
#pprint(simprofile)
#pprint(comparisons)



#exp.make_data()
#
#exp.output_cell_cols_def()
#exp.output_nuc_cols_def()



br.ptoc(t)
