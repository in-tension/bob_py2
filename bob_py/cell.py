
import copy


from ij import IJ, WindowManager
from ij.measure import ResultsTable
from ij.gui import NonBlockingGenericDialog, Roi, PolygonRoi
from ij.io import DirectoryChooser
from ij.plugin import Duplicator
from ij.plugin.frame import RoiManager


import fiji_utils as futils
import brutils as br

from .nuc import Nuc
from .bob_exceptions import BobException
from .bob_hding import BobHding

class Cell :


# { <static_and_class_methods>

    @staticmethod
    def read_roi_csv(file_path, cal) :
        """open and xy csv file, uncalibrates the values and creates and returns a polygon roi"""
        roi_csv_headings = ['X', 'Y']

        coord_rows = br.csv_to_rows(file_path, cast_type=float)
        if coord_rows[0] == roi_csv_headings :
            coord_col_dict = br.csv_to_col_dict(file_path, cast_type=float)
        else :
            coord_cols = br.rotate(coord_rows)
            coord_col_dict = {'X':coord_cols[0], 'Y':coord_cols[1]}

        cal_func_dict = {'X' : cal.getRawX, 'Y' : cal.getRawY}
        for col_name, cal_func in zip(coord_col_dict.keys(), cal_func_dict.values()) :
            for i in range(len(coord_col_dict[col_name])) :

                coord_col_dict[col_name][i] = cal_func(coord_col_dict[col_name][i])

        roi = PolygonRoi(coord_col_dict['X'], coord_col_dict['Y'],len(coord_col_dict['X']),Roi.POLYGON)

        return roi

    # } </static_and_class_methods>


    def __init__(self, hseg, name, cell_path) :
        """init"""
        self.hseg = hseg
        self.name = name
        self.roi_csv_path = cell_path


# { <dev>



    # } </dev>

# { <properties>

    @br.lazy_eval
    def roi(self) :
        self._roi = Cell.read_roi_csv(self.roi_csv_path, self.hseg.cal())

    @br.lazy_eval
    def nucs(self) :
        self.hseg.create_nucs()

    def add_nuc(self, nuc_roi) :
        """
        adds a nuc to self._nucs (self.nucs())
        called by hseg.create_nucs
        """
        nuc_id_num = len(self.nucs())
        self.nucs().append(Nuc(self, nuc_id_num, nuc_roi))


    @br.lazy_eval
    def cell_data(self) :
        self.hseg.make_data()

    @br.lazy_eval
    def cell_data_hdings(self) :
        self.hseg.make_data()


    @br.lazy_eval
    def nuc_data_hdings(self) :
        self.hseg.make_data()

    @br.lazy_eval
    def nuc_data(self) :
        self.hseg.make_data()


    def init_data_attrs(self) :
        self._cell_data = []
        self._cell_data_hdings = []


        self._nuc_data_hdings = []
        self._nuc_data = {}
        for nuc in self.nucs() :
            self._nuc_data[nuc.make_data_dict_label()] = []

    def add_to_cell_data(self, hdings, new_data) :
        if len(hdings) != len(new_data) :
            raise BobException('cell.add_to_cell_data: length of hdings not equal length of new data')

        self.cell_data_hdings().extend(hdings)
        self.cell_data().extend(new_data)

    def add_to_nuc_data(self, hdings, new_data) :
        col_cnt = len(hdings)


        if len(new_data) != self.get_nuc_cnt() :
            raise BobException('cell.add_to_nuc_data: nuc_cnt does not match number of rows')

        self.nuc_data_hdings().extend(hdings)
        for nuc_label in self.nuc_data().keys() :
            if nuc_label not in new_data :
                print(nuc_label)
                print(new_data.keys())
                raise BobException('cell.add_to_nuc_data: nuc not in new data')

            new_row = new_data[nuc_label]
            if len(new_row) != col_cnt :
                raise BobException('cell.add_to_nuc_data: length of hdings does not equal length of row')

            self.nuc_data()[nuc_label].extend(new_row)

        self.verify_nuc_data()


    def calc_summary_data(self, hding) :
        col = self.get_nuc_data_col(hding)

        tot = 0
        for val in col.values() :
            tot += val

        avg = tot/len(col)


        norm_col = {}
        for nuc_label, val in col.items() :
            norm_col[nuc_label] = [val/avg]


        avg_hding = copy.copy(hding)
        avg_hding.func = "Avg"
        tot_hding = copy.copy(hding)
        tot_hding.func = "Tot"
        norm_hding = copy.copy(hding)
        norm_hding.func = "Norm"


        new_cell_hdings = [avg_hding, tot_hding]
        new_cell_data = [avg, tot]
        self.add_to_cell_data(new_cell_hdings, new_cell_data)


        self.add_to_nuc_data([norm_hding], norm_col)

    def get_nuc_data_col(self, hding) :
        if hding not in self.nuc_data_hdings() :

            raise br.LazyEvalException('Cell.get_nuc_data_col', 'cell.get_nuc_data_col: hding {} not in nuc_data_hdings'.format(hding))

        ind = self.nuc_data_hdings().index(hding)

        col = {}
        for nuc_label, row in self.nuc_data().items() :
            col[nuc_label] = row[ind]

        return col


    ## creates vor_roi in nuc class
    def create_vor_roi(self) :
        """
        creates vor_roi
        is called by nuc to create vor_roi
        vor_roi are created and then matched to respective nuc
        """
        vor_rois = self.creating_vor_roi()
        self.match_vor_nuc(vor_rois)

    def creating_vor_roi(self) :
        """
        runs voronoi on cell to create vor_rois
        """
        rm = RoiManager.getRoiManager()
        rm.reset()
        d = Duplicator()
        nuc_bin_copy = d.run(self.hseg.nuc_bin())
        nuc_bin_copy.show()

        IJ.run(nuc_bin_copy, "Make Binary", "")
        nuc_bin_copy.setRoi(self.roi())
        IJ.run(nuc_bin_copy, "Clear Outside", "")

        IJ.run(nuc_bin_copy, "Voronoi", "")
        nuc_bin_copy.setRoi(None)
        ip = nuc_bin_copy.getProcessor()
        ip.setMinAndMax(0,1)
        IJ.run(nuc_bin_copy, "Apply LUT", "")

        nuc_bin_copy.setRoi(self.roi())
        IJ.run(nuc_bin_copy, "Analyze Particles...", "add")
        vor_rois = rm.getRoisAsArray()

        futils.force_close(nuc_bin_copy)

        return vor_rois

    def match_vor_nuc(self, vor_rois) :
        """
            matches vor_rois with their respective nucs
            by checking if nuc_cent in vor_roi

            currently having issues/not working
        """
        ## if IJ.escapePressed() : IJ.exit()
        ## did this work?

        rm = RoiManager.getRoiManager()
        nuc_inds = [x for x in range(len(self.nucs()))]
        for vor_roi in vor_rois :


            temp = None
            for i, nuc_ind in enumerate(nuc_inds) :
                nuc_roi = self.nucs()[nuc_ind].roi()

                nuc_cent = futils.roi_cent(nuc_roi, integer=True)

                if vor_roi.contains(*nuc_cent) :
                    self.nucs()[nuc_ind]._vor_roi = vor_roi

                    temp = i
                    break

            else :

                raise BobException('issue matching voronoi and nuc')

            if temp is not None :
                del nuc_inds[temp]

    # } </properties>

# { <general>

    def get_nuc_dict(self) :
        nuc_dict = {}

        for nuc in self.nucs() :
            nuc_dict[nuc.name] = nuc

        return nuc_dict

    def get_nuc(ind_key) :
        if type(ind_key) == int :
            return self.nucs()[ind_key]
        elif type(ind_key) == str :
            return self.get_nuc_dict()[ind_key]
        else :
            raise(BobException("exper.get_hseg - ind_key must be an int or string"))

    def get_nuc_cnt(self) :
        return len(self.nucs())


    def cell_data_col_cnt(self) :
        if not self.verify_cell_data() :
            raise BobException('{}: cell_data failed to verify'.format(self.get_short_id()))

        return len(self.cell_data_hdings())

    def verify_cell_data(self) :
        col_cnt = len(self.cell_data_hdings())
        if len(self.cell_data()) != col_cnt :
            return False
        else :
            return True


    def nuc_data_col_cnt(self) :
        if not self.verify_nuc_data() :
            raise BobException('{}: nuc_data failed to verify'.format(self.get_short_id()))

        return len(self.nuc_data_hdings())

    def verify_nuc_data(self) :
        valid = True
        col_cnt = len(self.nuc_data_hdings())

        for label, row in self.nuc_data().items() :
            if len(row) != col_cnt :
                print('{}: {} row is len {} not {}'.format(self.get_short_id(), label, len(row), col_cnt))
                valid = False

        return valid

    # } </general>

# { <to_string functions>

    def get_prefix(self) :
        """For logging: prints name tabbed out appropriately"""
        return '  '*2 + self.get_long_name() + ':'

    def get_id(self) :
        """
        id = <exper.name>[_<hseg.name>[_<cell.name>[_<nuc.name>]]]
        created by recursively calling parent.get_id()
        """
        return '_'.join([self.hseg.get_id(), self.name])

    def get_short_id(self) :
        """
        short_id = <hseg.name>[_<cell.name>[_<nuc.name>]]
        created by recursively calling parent.get_short_id()
        """
        return '_'.join([self.hseg.get_short_id(), self.name])

    # } </to_string functions>
