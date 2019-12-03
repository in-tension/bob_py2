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
from .bob_exception import BobException



class Hseg :

    RAW_SUF = '.tif'
    NUC_BIN_SUF = '_Nuc-bin.tif'

    JSON_SUF = '.json'              ## why is this here and not in exper?
    JSON_SPLIT_CHAR = 'json:'       ## why is this here and not in exper?

    CELL_SUF_REGEX = '_XY-([^\.]*).csv'
    CELL_SUF_PATTERN = re.compile(CELL_SUF_REGEX)


    # CELL_ROI_DICT_NAME = "cell"
    #
    # GEO = "geo"
    # INTENS = ""
    # NUC_ROI_DICT_NAME = "nucs"
    # VOR_ROI_DICT_NAME = "vors"





    def __init__(self, exper, dir_name) :
        self.exper = exper
        self.name = dir_name.replace(self.exper.name+'_', '')
        self.path = os.path.join(self.exper.path, dir_name)

        self._prj_imps = {}
        self._data = {}



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

    def slices(self) :
        try :
            return self._slices
        except :
            self._slices = self.exper.hseg_slices()[self.name]
            return self._slices


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


    # def cell_roi_dict(self) :
    #     """
    #     dict { name(str) = roi }
    #     roi_dicts can be used with fiji_utils/futils' measure_roi_dict, meas_rdict_geo, meas_rdict_intens
    #     """
    #     try :
    #         return self._cell_roi_dict
    #     except :
    #         self.create_roi_dicts()
    #         return self._cell_roi_dict

    # def cell_geo_data(self) :
    #     try :
    #         return self._cell_geo_data
    #     except :
    #         self.create_geo_data()
    #         return self._cell_geo_data
    #

    def prj_imps(self, prj_method) :
        try :
            return self._prj_imps[prj_method]
        except :
            self.create_prj_imp(prj_method)
            return self._prj_imps[prj_method]
        # if id in self._prj_imps :
        #     return self._prj_imps[""]
        # if len(self._prj_imps) > 0 :
        #     return self._prj_imps
        # else :
        #     self.create_prj_imps()
        #     return self._prj_imps


    def roi_dicts(self, roi_dict_name) :
        try :
            return self._roi_dicts[roi_dict_name]
        except :
            self.create_roi_dicts(roi_dict_name)
            return self._roi_dicts[roi_dict_name]


    def create_roi_dicts(self, roi_dict_name) :
        # self._cell_roi_dict = {}

        if roi_dict_name == "cell" :
            self._roi_dicts = {"cell":{}}
            for cell in self.cells() :
                label = cell.get_id().replace(self.exper.name, '')
                self._roi_dicts["cell"][label] = cell.roi()
        else :
            raise Exception('no roi_dict in hseg called {}'.format(roi_dict_name))

    def data(self, data_key) :
        """ key = (roi_dict_name, (imp_info))
        imp_info = (("geo"))
            or
                 = (("intens", prj_method, channel)
        """
        try :
            return self._data[data_key]
        except :
            self.create_data(data_key)
            return self._data[data_key]

    def create_data(self, data_key) :
        roi_dict_name = data_key[0]
        # print(data_key)
        roi_dict = self.roi_dicts(roi_dict_name)
        # print(roi_dict)
        imp_info = data_key[1]

        if imp_info[0] == "geo" :
            new_data = futils.meas_rdict_geo(self.raw_stack(), roi_dict)
            self._data[data_key] = new_data

        elif imp_info[0] == "intens" :
            imp = sefl.get_prj_imp_ch(*imp_info)
            new_data = futils.meas_rdict_intens(imp, roi_dict)
            self._data[data_key] = new_data


        else :
            raise(BobException('crap Hseg.create_data, data_key is wrong'))

    ## </properties>

## <create properties>


    def make_file_dicts(self) :     ## change to create?
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

    def ihe(self, sheet_dict) :

        for sheet_dict in ihe_dict.values() :

            for data_key in sheet_dict.keys() :
                print(self.data(data_key))


    # def create_roi_dicts(self) :
    #     self._cell_roi_dict = {}
    #     for cell in self.cells :
    #         label = cell.get_id().replace(self.exper.name, '')
    #         self._cell_roi_dict[label] = cell.roi
    #
    #     for cell in self.cells() :
    #         for nuc in cell.nucs() :
    #             label = nuc.get_short_id()
    #
    #             cell._nuc_roi_dict[label] = nuc.roi()
    #             cell._vor_roi_dict[label] = nuc.vor_roi()

    # def create_geo_data(self) :
    #     self._cell_geo_data = futils.meas_rdict_geo(self.nuc_bin, self.cell_roi_dict())
    #
    #     for cell in self.cells :
    #         cell._vnuc_geo_data = futils.meas_rdict_geo(self.nuc_bin, cell.nuc_roi_dict())
    #         cell._vor_geo_data = futils.meas_rdict_geo(self.nuc_bin, cell.vor_roi_dict())
    #
    # def create_intens_data(self) :
    #     intens_dict = {}
    #
    #     for prj_method, prj_infos in self.exper.prj_method_dict().items() :
    #         prj_imp = self.prj_imps()[prj_method]
    #         # prj_imp.show()
    #
    #
    #         for prj_info in prj_infos :
    #             channel = prj_info[0]
    #             roi_dict_name = prj_info[1]
    #
    #             # roi_dict = self.get_roi_dict_by_name(roi_dict_name)
    #             ## could change this later for more generality
    #             # if roi_dict_name == "nucs"
    #
    #
    #             prj_imp.setC(channel)
    #             prj_imp_name = '_'.join([self.exper.get_channel_name(channel), prj_method])
    #             for cell in self.cells()
    #                 cell.intens_data
    #
    #             intens_data = futils.roi_dict_intens(prj_imp, roi_dict)
    #             intens_data_name = '_'.join([self.exper.get_channel_name(channel), roi_dict_name])
    #
    #             intens_dict[intens_data_name] = intens_data
    #


    # def create_prj_imps(self) :
    #     # slices = self.exper.hseg_slices()[self.name]
    #
    #     self._prj_imps = {}
    #
    #     for prj_method in self.exper.prj_method_dict() :
    #         prj_imp = futils.make_projection(self.raw_imp, prj_method, self.slices())
    #
    #         self._prj_imps[prj_method] = prj_imp

    def create_prj_imp(self, prj_method) :
        # slices = self.exper.hseg_slices()[self.name]


        # for prj_method in self.exper.prj_method_dict() :
        # print(prj_method)
        # print(type(prj_method))
        prj_imp = futils.make_projection(self.raw_stack(), prj_method, self.slices())

        self._prj_imps[prj_method] = prj_imp

    def get_prj_imp_ch(self, prj_method, channel_id) :
        # print(type(prj_method))
        prj_imp = self.prj_imps(prj_method)
        if type(channel_id) == str :
            channel_num = self.exper.get_channel_num(channel_id)
        else :
            channel_num = channel_id
        prj_imp.setC(channel_num)
        return prj_imp

    ## </create properties>

    # def create_data(self, roi_dict_name, param) :
    #     if roi_dict_name == 'cell' :
    #         roi_dict = self.cell_roi_dict()
    #
    #         if param[0] == "geo" :
    #             imp = self.raw_stack()
    #
    #             data = futils.meas_rdict_geo(imp, roi_dict)
    #         else :
    #             imp.setC
    #             data = futils.meas_rdict_intens(imp)
    #     else :
    #         if roi_dict_name == "nuc"
    #             roi_dict =
    #



    def get_roi_dict(self, roi_dict_name) :
        return self.roi_dicts()[roi_dict_name]

    def open_hseg_imp(self, suf) :
        """open imp which starts with <hseg.get_id()>_<suf>"""
        if suf not in self.file_dict() :
            imp = None
            IJ.log('hemisegment {} does not have raw tif file {}'.format(self.name, self.name + suf))
            ## raise Exception('hemisegment {} does not have raw tif file {}'.format(self.name, self.name + suf))

        else :
            imp = IJ.openImage(self.file_dict()[suf])

        return imp


    # def make_prj_func(prj_method) :
    #     return futils.make





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
