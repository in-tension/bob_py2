
import os
import sys
import imp
from pprint import pprint

cwd = '/Users/baylieslab/Documents/Amelia/code_dev/projects/bob_py/bob_idk'
sys.path.append(cwd)


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





exper_path = "/Users/baylieslab/Documents/Amelia/data/steffiData/150511_Lim3b-GFP_Hoe-GFP-H4K16ac-Fib-DL-Phal"

t = br.tic()

bob_py.Exper.setup()


exp = bob_py.Exper(exper_path)
h = exp.hsegs()[0]
c = h.cells()[0]
n = c.nucs()[0]


#h.create_data()
exp.make_data()
#exp.output()

exp.output_cell_cols_def()
exp.output_nuc_cols_def()

#print(n.vor_roi())

#print(c._nuc_data_hdings)
#print(c._cell_data_hdings)
#for hseg in exp.hsegs() :
#	try :				
#		hseg.create_data()
#	except bob_py.HsegDeactivated as hd:
#		print(hd)



#print(exp._inactive_hseg_dict.keys())



#print(exp.what_to_msr())

#h.create_data()
#exc = 

#try :					
#	exp.create_aggr_data()
#except Exception as e :
##	print(e.message)
#	exc = e
#	
#print(self.
#for hseg in exp.hsegs() :
#	try :
#
#		hseg.create_data() 
#	except bob_py.BobException as be :
#		print(be)
#
#br.print_coll_type(c.data())
#
#for img_src, img_src_data in c.data().items() :
#	print(img_src)
#	for key, val in img_src_data.items() :
#		if type(key) != tuple : print(val)
#	

#	print(exp._inactive_hseg_dict.keys())
	
##	for cell in hseg.cells() :
##		print(cell.data()
#for cell in exp.cell_iter() :
#		data = cell.data()
#		for grp_name, row_dict in data.items() :
#			
#			print('\t' + cell.get_short_id() + ': ' + str(grp_name))
#			for item in row_dict.keys() :
#				print(item)
##			print(row_dict.keys())
#
#print(type(exc))
#print(exc.message)
##hsegs = exp.hsegs() 
#
#for hseg in hsegs :
#	if 'L2-L1' in hseg.name :
#		h = hseg
#		print(h)

#exp.output_raw3()
#print(exp)
#

#print(h._data_cols.keys())
#print(c.name)
#print(bob_py.Exper.__dict__.keys())
#print(bob_py.Exper.ONE_HSEG)

#h = exp.one_hseg()
#print(h)


#h = exp.hsegs()[0]
#
#data = h.data()
#
#for grp_name, row_dict in data.items() :
#	print(grp_name)
#	for sample_name, row in row_dict.items() :
#		if sample_name == "col_hdings" : 
#			print(sample_name),
#			print(row)
#		else :
#			print(sample_name),
#			for val in row :
#				print(', {:.2f}'.format(val)),
#	#		print(row)
#			print('')

#print(data[("Cell", "Geo")])

#for src_data in data.values() :
#	print(src_data)
#	for inst_data in src_data.values() :
#		print(inst_data)
##		print(inst_data['Label'])


#for src, src_dict in data.items() :
#	print(src)
#	for l in src_dict['Label'] :
#		print(l)
#	print(src_dict['Label'])
#	for idk, idk_dict in src_dict.items() :
##		print('  {}'.format(idk))
#		print(idk_dict['Label'])
		








#h = exp.hsegs()[0]
#c = h.cells()[0]
#n = c.nucs()[0]
#
#
#
##print(exp.aggr_data()["nuc_sheet"][("Nuc", "Geo")].keys())
#
#temp = exp.aggr_data()



#print(exp.aggr_hdings())
#output_rows_dict =
#temp = exp.output_raw3()
#
#for key, d in exp.aggr_data()["nuc_sheet"][("Nuc", "Geo")].items() :
##	print('{}: {}'.format(key, d.keys()))
#	print(d)
#	break
#



#h.ihe()
#exp.dev_create_default_data()5
#print(exp.aggr_data())

#exp.create_rearranged_data()
#exp.dev_save()
#futils.jpprint(h._data.items())


#for h in exp.hsegs() :
#	h.data(("Cell",("Geo")))

br.ptoc(t)
