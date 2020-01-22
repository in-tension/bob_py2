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
import copy


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
from .bob_hding import BobHding


class Hseg :

    RAW_SUF = '.tif'
    NUC_BIN_SUF = '_Nuc-bin.tif'

    CELL_SUF_REGEX = '_XY-([^\.]*).csv'
    CELL_SUF_PATTERN = re.compile(CELL_SUF_REGEX)


# { <static_and_class_methods>
    @staticmethod
    def parse_rt_label(label) :
        temp = label.split(':')[1]
        if not temp.startswith('L') :
            raise BobException('issue processing results table Label name')

        parts = temp.split('_')

        if len(parts) == 2 :
            new_label = (parts[0], parts[1])
            cell_name = temp

        else :
            idk = parts[2].split('-')
            new_label = (parts[0], parts[1], int(idk[1]))
            cell_name = '_'.join([parts[0], parts[1]])

        return new_label, cell_name


    # } </static_and_class_methods>


    def __init__(self, exper, dir_name) :
        self.exper = exper
        self.name = dir_name.replace(self.exper.name+'_', '')
        self.path = os.path.join(self.exper.path, dir_name)

        self.inactive = False

        self._prj_imps = {}
        self._roi_dicts = {}


# { <dev>



    # } </dev>

# { <properties>

    @br.lazy_eval
    def file_dict(self) :
        """
            `property`
            keys -> file_suf
            vals -> file_path
        """
        self.create_file_dicts()

    @br.lazy_eval
    def cell_file_dict(self) :
        """
            `property`
            just cell rois
            keys -> cell_name (not the actually file_suf)
            vals -> file_path
        """
        self.create_file_dicts()

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
                suf = file_name.replace(self.get_id(), '')
                file_path = os.path.join(self.path, file_name)

                m = Hseg.CELL_SUF_PATTERN.match(suf)
                if m :
                    self._cell_file_dict[m.group(1)] = file_path

                else :
                    self._file_dict[suf] = file_path

    @br.lazy_eval
    def slices(self) :
        self._slices = self.exper.hseg_slices()[self.name]

    @br.lazy_eval
    def raw_stack(self) :
        self._raw_stack = self.open_hseg_imp(Hseg.RAW_SUF)

    @br.lazy_eval
    def cal(self) :
        self._cal = self.raw_stack().getCalibration()

    @br.lazy_eval
    def nuc_bin(self) :
        self._nuc_bin = self.open_hseg_imp(Hseg.NUC_BIN_SUF)

    def open_hseg_imp(self, suf) :
        """open imp which starts with <hseg.get_id()>_<suf>"""
        if suf not in self.file_dict() :
            imp = None
            IJ.log('hemisegment {} does not have raw tif file {}'.format(self.name, self.name + suf))
            ## raise Exception('hemisegment {} does not have raw tif file {}'.format(self.name, self.name + suf))

        else :
            imp = IJ.openImage(self.file_dict()[suf])

        return imp


    @br.lazy_eval
    def cells(self) :
        """create cells from cell rois"""
        if len(self.cell_file_dict()) == 0 :
            self.exper.deactivate_hseg(self.name, 'no cell coordinate files found')

        self._cells = []
        for cell_name, cell_path in self.cell_file_dict().items() :
            self._cells.append(Cell(self, cell_name, cell_path))


    @br.lazy_eval_dict
    def prj_imps(self, prj_method) :
        prj_imp = futils.make_projection(self.raw_stack(), prj_method, self.slices())

        self._prj_imps[prj_method] = prj_imp


    @br.lazy_eval_dict
    def roi_dicts(self, roi_dict_name) :
        self._roi_dicts[roi_dict_name] = {}
        ## should I put if statements within for loop, or repeat for loop in each if statement?
        for cell in self.cells() :

            if roi_dict_name == "Cell" :
                label = cell.get_short_id()
                self._roi_dicts[roi_dict_name][label] = cell.roi()

            elif roi_dict_name == "Nuc" :

                for nuc in cell.nucs() :
                    label = nuc.get_short_id()
                    self._roi_dicts[roi_dict_name][label] = nuc.roi()

            elif roi_dict_name == "Vor" :
                for nuc in cell.nucs() :
                    label = nuc.get_short_id_vor()
                    self._roi_dicts[roi_dict_name][label] = nuc.vor_roi()

            else :
                raise Exception('no roi_dict in hseg called {}'.format(roi_dict_name))

    ## creates nucs in cell class
    def create_nucs(self) :
        """ """
        for cell in self.cells() :
            cell._nucs = []

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
        return problem_nucs

    # } </properties>

# { <general>

    def get_cell(self, ind_key) :
        if type(ind_key) == int :
            return self.cells()[ind_key]
        elif type(ind_key) == str or type(ind_key) == unicode :
            if ind_key.startswith(self.name) :
                ind_key = ind_key.replace(self.name + '_','')
            return self.get_cell_dict()[ind_key]
        else :
            raise(BobException("hseg.get_cell - ind_key ({}) is {}, it must be an int or string".format(ind_key, type(ind_key))))

    def get_cell_dict(self) :
        cell_dict = {}
        for cell in self.cells() :
            cell_dict[cell.name] = cell

        return cell_dict

    def get_prj_imp_ch(self, channel_def) :
        prj_imp = self.prj_imps(channel_def.prj_method)

        prj_imp.setC(channel_def.num)
        return prj_imp

    # } </general>

# { <processing:make_data>

    def make_data(self) :
        for cell in self.cells() :
            cell.init_data_attrs()
            ## these are initialized here so that when other cell functions are called
            ## they can get these attrs using their functions instead the variables

        self.make_raw_data()
        self.make_summary_data()

    def make_raw_data(self) :
        to_msr = self.exper.to_msr()

        for hding in to_msr :


            roi_dict = self.roi_dicts(hding.roi_set)
            if len(roi_dict) == 0 : self.log('roi_dict empty')
            if hding.is_geo() :

                imp = self.raw_stack()
                meas_int = futils.MEAS_GEO

            else :

                imp = self.get_prj_imp_ch(hding.channel_def)
                meas_int = futils.MEAS_INTENS_XY

            rt_dict = futils.measure_roi_dict(imp, roi_dict, set_measure=meas_int)


            self.rt_data_to_cells(rt_dict, hding)

    def make_summary_data(self) :
        to_summarize = self.exper.to_summarize()

        for hding in to_summarize :
            for cell in self.cells() :
                cell.calc_summary_data(hding)

    def rt_data_to_cells(self, rt_dict, hding_subpart) :

        row_labels = rt_dict.pop('Label')
        hdings = []
        for msr_param in rt_dict.keys() :
            new_hding = copy.copy(hding_subpart)
            new_hding.set_msr_param(msr_param)
            hdings.append(new_hding)
        cols = [col for col in rt_dict.values()]


        rows = br.rotate(cols)

        if hding_subpart.is_cell_sheet() :
            for i in range(len(rows)) :
                new_label, cell_name = Hseg.parse_rt_label(row_labels[i])
                self.get_cell(cell_name).add_to_cell_data(hdings, rows[i])

        else :
            cell_rows = {}
            for i in range(len(rows)) :
                new_label, cell_name = Hseg.parse_rt_label(row_labels[i])

                if cell_name in cell_rows :
                    cell_rows[cell_name][new_label] = rows[i]
                else :
                    cell_rows[cell_name] = {new_label: rows[i]}

            for cell_name, rows in cell_rows.items() :
                self.get_cell(cell_name).add_to_nuc_data(hdings, rows)

    # } </processing:make_data>

# { <to_string functions>

    def log(self, message) :
        print(self.get_short_id() + ': ' + message)

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

    # } </to_string functions>
