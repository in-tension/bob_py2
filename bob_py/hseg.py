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
            self.create_file_dicts()
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
            self.create_file_dicts()
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
            self.create_raw_stack()
            return self._raw_stack

    def cal(self) :
        try :
            return self._cal
        except :
            self.create_raw_stack()
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
    def cell_dict(self) :
        try :
            return self._cell_dict
        except :
            self.create_cells()
            return self._cell_dict


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



    ## </properties>

## <create properties>


    def create_file_dicts(self) :
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

    def create_raw_stack(self) :
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

        IJ.run(self.nuc_bin(), "Invert", "")


        rt = ResultsTable.getResultsTable()
        rt.reset()
        IJ.run(self.nuc_bin(), "Analyze Particles...", "add")

        rois = rm.getRoisAsArray()
        IJ.run(self.nuc_bin(),"Remove Overlay", "");



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



    def create_prj_imp(self, prj_method) :
        prj_imp = futils.make_projection(self.raw_stack(), prj_method, self.slices())

        self._prj_imps[prj_method] = prj_imp


    def create_roi_dicts(self, roi_dict_name) :
        # self._cell_roi_dict = {}

        if roi_dict_name == "cell" :
            self._roi_dicts = {"cell":{}}
            for cell in self.cells() :
                # label = cell.get_id().replace(self.exper.name + '_', '')
                label = cell.name;
                self._roi_dicts["cell"][label] = cell.roi()
        else :
            raise Exception('no roi_dict in hseg called {}'.format(roi_dict_name))

    def create_data(self, data_key) :
        # print(data_key)
        roi_dict_name = data_key[0]
        roi_dict = self.roi_dicts(roi_dict_name)
        imp_info = data_key[1]


        if (type(imp_info) == str and imp_info == "geo") or imp_info[0] == "geo" :
                cell_rt_data = futils.meas_rdict_geo(self.raw_stack(), roi_dict)
                new_data = self.process_cell_rt_data(cell_rt_data)
                self._data[data_key] = new_data

        elif imp_info[0] == "intens" :
            imp = self.get_prj_imp_ch(*imp_info)
            cell_rt_data = futils.meas_rdict_intens(imp, roi_dict)
            new_data = self.process_cell_rt_data(cell_rt_data)
            self._data[data_key] = new_data


        else :
            raise BobException('crap Hseg.create_data, data_key is wrong')


    def process_cell_rt_data(self, cell_rt_data) :
        new_data = {}


        # for label in cell_rt_data["Label"] :
        for i in range(len(cell_rt_data["Label"])) :
            cell_name = futils.results_label_to_roi_label(cell_rt_data["Label"][i])
            if cell_name not in self.cell_dict() :
                raise BobException("hseg.process_cell_rt_data: roi_name should match the name of one of the cells")
            cell_key = (self.name, cell_name) ## todo: parse_name function to replace self.name with (larva, side, seg))
            new_data[cell_key] = {}
            for msr_param in cell_rt_data.keys() :
                if msr_param == "Label" :
                    continue
                else :
                    new_data[cell_key][msr_param] = cell_rt_data[msr_param][i]
        return new_data



    ## </create properties>

## <other>
    def get_prj_imp_ch(self, prj_method, channel_id) :
        prj_imp = self.prj_imps(prj_method)
        if type(channel_id) == str :
            channel_num = self.exper.get_channel_num(channel_id)
        else :
            channel_num = channel_id
        prj_imp.setC(channel_num)
        return prj_imp

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

    def get_cell(ind_key) :
        if type(ind_key) == int :
            return self.cells()[ind_key]
        elif type(ind_key) == str :
            return self.cells()[self.cell_dict()[ind_key]]
        else :
            raise(BobException("hseg.get_cell - ind_key must be an int or string"))
    ## </other>


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
