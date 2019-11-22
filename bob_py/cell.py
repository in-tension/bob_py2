
from ij import IJ, WindowManager
from ij.measure import ResultsTable
from ij.gui import NonBlockingGenericDialog, Roi, PolygonRoi
from ij.io import DirectoryChooser
from ij.plugin import Duplicator
from ij.plugin.frame import RoiManager


import fiji_utils as futils
import brutils as br

from .nuc import Nuc

class Cell :

    def __init__(self, hseg, name, cell_path) :
        self.hseg = hseg
        self.name = name
        self.roi_csv_path = cell_path

        self._nucs = []
        self._nuc_dict = {}

    ## <properties>

    def roi(self) :
        try :
            return self._roi
        except :
            self._roi = Cell.read_roi_csv(self.roi_csv_path, self.hseg.cal())
            return self._roi

    def nucs(self) :
        """unlike others, instead of checking if exists,
        checks if empty"""
        if len(self._nucs) > 0 :
            return self._nucs
        else :
            self.hseg.create_nucs()


        # try :
        #     return self._nucs
        # except :
        #     # self.create_nucs()
        #     return self._nucs



    ## </properties>

    ## <create properties>

    def create_nucs() :
        pass





    ## </create properties>

    def add_nuc(self, nuc_roi) :
        nuc_id_num = len(self._nucs)
        self._nucs.append(Nuc(self, nuc_id_num, nuc_roi))
        self._nuc_dict[self.nucs()[-1].name] = nuc_id_num





    def get_prefix(self) :
        return '  '*2 + self.get_long_name() + ':'

    def get_id(self) :
        return '_'.join([self.hseg.get_id(), self.name])


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
