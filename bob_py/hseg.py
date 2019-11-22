"""
abbr.
    prj = projection
    hseg = hemisegment
    exper = experiment
    suf = suffix
    nuc = nuclei/nucleus
    bin = binary
    imp = ImagePlus/image
    vor = voronoi
"""


import os
import re


from ij import IJ, WindowManager
from ij.measure import ResultsTable
from ij.gui import NonBlockingGenericDialog, Roi, PolygonRoi
from ij.io import DirectoryChooser
from ij.plugin import Duplicator
from ij.plugin.frame import RoiManager

import brutils as br
import fiji_utils as futils

from .cell import Cell




class Hseg :

    RAW_SUF = '.tif'
    NUC_BIN_SUF = '_Nuc-bin.tif'

    JSON_SUF = '.json'
    JSON_SPLIT_CHAR = 'json:'

    CELL_SUF_REGEX = '_XY-([^\.]*).csv'
    CELL_SUF_PATTERN = re.compile(CELL_SUF_REGEX)

    CELL_ROI_DICT_NAME = "cells"
    NUC_ROI_DICT_NAME = "nucs"
    VOR_ROI_DICT_NAME = "vors"




    def __init__(self, exper, dir_name) :
        self.exper = exper
        self.name = dir_name.replace(self.exper.name+'_', '')
        self.path = os.path.join(self.exper.path, dir_name)



## <properties>
    def file_dict(self) :
        """
            `property`
            keys -> file_suf
            vals -> file_path
        """
        try :
            return self._file_dict
        except :
            self.make_file_dicts()
            return self._file_dict

    def cell_file_dict(self) :
        """
            `property`
            just cell rois
            keys -> cell_name (not the actually file_suf)
            vals -> file_path
            """
        try :
            return self._cell_file_dict
        except :
            self.make_file_dicts()
            return self._cell_file_dict


    def raw_stack(self) :
        try :
            return self._raw_stack
        except :
            self.open_raw_stack()
            return self._raw_stack

    def cal(self) :
        try :
            return self._cal
        except :
            self.open_raw_stack()
            return self._cal

    def nuc_bin(self) :
        try :
            return self._nuc_bin
        except :
            self._nuc_bin = self.open_hseg_imp(Hseg.NUC_BIN_SUF)
            return self._nuc_bin


    def cells(self) :
        try :
            return self._cells
        except :
            self.create_cells()
            return self._cells





    ## </properties>

## <create properties>


    def make_file_dicts(self) :
        """
            makes
            - _file_dict
            - _cell_file_dict
        """
        self._file_dict = {}
        self._cell_file_dict = {}
        files = os.listdir(self.path)
        for file_name in files :
            if file_name.startswith(self.get_id()) :
                # suf = file_name.replace(self.get_id(), '', 1)
                suf = file_name.replace(self.get_id(), '')
                file_path = os.path.join(self.path, file_name)

                m = Hseg.CELL_SUF_PATTERN.match(suf)
                if m :
                    self._cell_file_dict[m.group(1)] = file_path

                else :
                    self._file_dict[suf] = file_path


    def open_raw_stack(self) :
        """
            creates
            - _raw_stack
            - _cal
        """
        self._raw_stack = self.open_hseg_imp(Hseg.RAW_SUF)
        self._cal = self._raw_stack.getCalibration()

    def create_cells(self) :
        """create cells from cell rois"""
        self._cells = []
        self._cell_dict = {}
        for cell_name, cell_path in self.cell_file_dict().items() :
            self._cells.append(Cell(self, cell_name, cell_path))
            self._cell_dict[cell_name] = len(self._cells) - 1



    def create_nucs(self) :
        """ """
        rm = RoiManager.getRoiManager()
        rm.reset()

        # if UPDATE1 :
        IJ.run(self.nuc_bin(), "Invert", "")
        # self.nuc_bin().show()
        # len()
        # from ij.gui import WaitForUserDialog
        # wfug = WaitForUserDialog('butts')
        # wfug.show()

        rt = ResultsTable.getResultsTable()
        rt.reset()
        IJ.run(self.nuc_bin(), "Analyze Particles...", "add")

        rois = rm.getRoisAsArray()
        IJ.run(self.nuc_bin(),"Remove Overlay", "");
        # self.nuc_bin().deleteRoi()
        # self.nuc_bin().show()
        # len()


        problem_nucs = []
        for roi in rois :
            nuc_cent = futils.roi_cent(roi, integer=True)

            found_cell = False
            for cell in self.cells() :
                if cell.roi().contains(*nuc_cent) :
                    cell.add_nuc(roi)
                    found_cell = True
                    break

            if not found_cell :
                IJ.log('Nuc not in any cell for hemisegment {}'.format(self.name))
                problem_nucs.append(roi)
        # print(self.cells['vl3'].nucs)
        return problem_nucs


    ## </create properties>




    def open_hseg_imp(self, suf) :
        """open imp which starts with <hseg.get_id()>_<suf>"""
        if suf not in self.file_dict() :
            imp = None
            IJ.log('hemisegment {} does not have raw tif file {}'.format(self.name, self.name + suf))
            ## raise Exception('hemisegment {} does not have raw tif file {}'.format(self.name, self.name + suf))

        else :
            imp = IJ.openImage(self.file_dict()[suf])

        return imp



## <to_string functions>

    def get_prefix(self) :
        """For logging: prints name tabbed out appropriately"""
        return '  ' + self.name + ':'

    def get_id(self) :
        """
        id = <exper.name>[_<hseg.name>[_<cell.name>[_<nuc.name>]]]
        created by recursively calling parent.get_id()
        """
        return '_'.join([self.exper.get_id(), self.name])

    def get_short_id(self) :
        """
        short_id = <hseg.name>[_<cell.name>[_<nuc.name>]]
        created by recursively calling parent.get_short_id()
        ends the recursive calls by return self.name
        """
        return self.name


    def __str__(self) :
        return self.get_id()

    def __repr__(self) :
        return self.get_id()

    ## </to_string functions>
