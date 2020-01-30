"""
abbr.
    prj = projection
    hseg = hemisegment
    exper = experiment
    suf = suffix
    msr_param = measurment parameter
"""


## TODO : documentation
## TODO : NND
## TODO : rel_y
## TODO :
## TODO :


## COULDDO: nuc_bin
## COULDDO: ploidy
## COULDDO:

## also make an iterator for exper to iterate throught the hseg
## where in the __next__ function it checks to see if macro has been cancelled



import os
import json
from runpy import run_path
from datetime import date

from ij import IJ, WindowManager
from ij.measure import ResultsTable
from ij.gui import NonBlockingGenericDialog, Roi, PolygonRoi
from ij.io import DirectoryChooser
from ij.plugin import Duplicator
from ij.plugin.frame import RoiManager

import fiji_utils as futils
import brutils as br

from .hseg import Hseg
from .bob_exceptions import BobException, HsegDeactivated
from .bob_hding import BobHding, BobChannelDef
from .default_output_hdings import default_cell_output_hdings, default_nuc_output_hdings


class Exper :
    """
    Attributes:
    """

    ## remove?
    IN_DEV = True
    ## remove?
    CATCH = False


    PRINT_PROGRESS = True
    """print progress"""



    META_SUF = '.py'
    """suffix of the meta data file
    prefix should be the Exper.name"""

# { <static_and_class_methods>

    @staticmethod
    def setup() :
        """setup"""

        if Exper.IN_DEV :
            canceled = False
        else :
            canceled = not IJ.showMessageWithCancel(__program__,'To proceed program will close all open images and windows, continue?')

        if not canceled :
            IJ.run("Colors...", "foreground=white background=black selection=yellow");

            ## aspirational todo: identify current settings and return settings at the end
            ## set setting to save column headers
            IJ.run("Input/Output...", "jpeg=85 gif=-1 file=.csv use_file save_column");

            ## set setting to copy column headers - not actually necessary
            IJ.run("Input/Output...", "jpeg=85 gif=-1 file=.csv copy_column save_column");

            futils.force_close_all_images()
            rm = RoiManager.getRoiManager()
            rm.reset()
            rm.show()


    def user_init(self, path) :
        exper = Exper(path)

        meta_path = exper.meta_data_path()

        if not os.path.exists(meta_path) :
            pass



    # } </static_and_class_methods>


    def __init__(self, path) :
        """
        Args:
            msg (str): Human readable string describing the exception.
            code (:obj:`int`, optional): Error code.
        """

        if path.endswith(os.sep) :
            path = path[:-1]
        self.path = path



        dir_name = os.path.basename(self.path)
        name = dir_name.split('_')[:2]
        self.name = '_'.join(name)
        """name is the first two terms of experiment directory name, where terms are split by '_'"""




# { <dev>

    # def overview_info(self) :

    def intens_im_to_load(self) :
        ## from hseg_archetype file contents
        pass

    def intens_im_to_make(self) :
        ## from meta_data
        pass

    def create_hseg_files_cabs(self) :
        # cab = br.CollectionArchetypeBuilder()
        #
        # for hseg in self.hsegs() :
        #     all_file_dict = hseg.file_dict()
        #     all_file_dict.update(hseg.cell_file_dict())
        #     all_file_dict.update(hseg.bin_file_dict())
        #     cab.add_collection(hseg.name, all_file_dict)
        #
        # hseg_at, hseg_at_deviations = cab.get_archetype_info()
        # hseg_at_inc = cab.archetype_inclusive
        #
        # at_str = ''
        # for val in hseg_at :
        #     at_str += str(val) + '\n'
        #
        # chf_panel = self.make_chf_panel(at_str)
        # hseg_tree_panel = self.make_hseg_tree_panel(hseg_at_deviations)

        self._hseg_all_files_cab = br.CollectionArchetypeBuilder()
        self._hseg_files_cab = br.CollectionArchetypeBuilder()
        self._hseg_bin_files_cab = br.CollectionArchetypeBuilder()
        self._hseg_cell_files_cab = br.CollectionArchetypeBuilder()

        for hseg in self.hsegs() :
            # temp_dict = hseg.file_dict()
            temp_dict = {}
            temp_dict.update(hseg.file_dict())
            temp_dict.update(hseg.bin_file_dict())
            temp_dict.update(hseg.cell_file_dict())
            self._hseg_all_files_cab.add_collection(hseg.name, temp_dict)
            self._hseg_files_cab.add_collection(hseg.name, hseg.file_dict())
            self._hseg_bin_files_cab.add_collection(hseg.name, hseg.bin_file_dict())
            self._hseg_cell_files_cab.add_collection(hseg.name, hseg.cell_file_dict())
        self._hseg_all_files_cab.create_all()
        self._hseg_files_cab.create_all()
        self._hseg_bin_files_cab.create_all()
        self._hseg_cell_files_cab.create_all()

    @br.lazy_eval
    def hseg_all_files_cab(self) :
        self.create_hseg_files_cabs()

    @br.lazy_eval
    def hseg_files_cab(self) :
        self.create_hseg_files_cabs()



    @br.lazy_eval
    def hseg_bin_files_cab(self) :
        self.create_hseg_files_cabs()

    @br.lazy_eval
    def hseg_cell_files_cab(self) :
        self.create_hseg_files_cabs()

    # } </dev>

# { <properties>

    @br.lazy_eval
    def hsegs(self) :
        self.create_hsegs()

    @br.lazy_eval
    def inactive_hseg_dict(self) :
        self.create_hsegs()

    def create_hsegs(self) :
        """given folders in self.path, initialize self.hsegs() and self.inactive_hseg_dict()"""
        files = os.listdir(self.path)
        self._hsegs = []
        self._inactive_hseg_dict = {}
        for file_name in files :
            if file_name.startswith(self.name) and os.path.isdir(os.path.join(self.path, file_name)):
                if Exper.IN_DEV :
                    self._hsegs.append(Hseg(self, file_name))
                else :
                    try :
                        self._hsegs.append(Hseg(self, file_name))
                    except Exception as e :
                        print('exception trying to init hseg {}: {}'.format(file_name, e))

    @br.lazy_eval
    def meta_data_path(self) :
        self._meta_data_path = os.path.join(self.path, self.name + Exper.META_SUF)

    @br.lazy_eval
    def meta_data(self) :
        # meta_data_path = os.path.join(self.path, self.name + Exper.META_SUF)
        self._meta_data = run_path(self._meta_data_path)

    @br.lazy_eval
    def hseg_slices(self) :
        self._hseg_slices = self.meta_data()["hseg_slices"]

    @br.lazy_eval
    def channel_dict(self) :
        ## TODO: make default dict if channel_dict doesn't exist

        channel_dict_raw = self.meta_data()["channel_dict"]

        self._channel_dict = {}
        for key, val in channel_dict_raw.items() :
            # channel_str
            if type(key) == str :
                channel_str = key
                channel_def = BobChannelDef(val)

            elif type(val) == str :
                channel_str = val
                channel_def = BobChannelDef(key)
            else :
                raise BobException('channel_dict')

            self._channel_dict[channel_str] = channel_def
            self._channel_dict[channel_def] = channel_str

    @br.lazy_eval
    def to_msr(self) :
        self._to_msr = []
        channel_dict = self.channel_dict()
        for item in self.meta_data()["to_msr"] :
            self._to_msr.append(BobHding.make_bob_hding(item, channel_dict))

    @br.lazy_eval
    def to_summarize(self) :
        self._to_summarize = []
        channel_dict = self.channel_dict()
        for item in self.meta_data()["to_summarize"] :
            self._to_summarize.append(BobHding.make_bob_hding(item, channel_dict))


    @br.lazy_eval
    def output_path(self) :
        # self._output_path = os.path.join(self.path, '_'.join([self.name, 'spreadsheets']))

        self._output_path = os.path.join(self.path,'spreadsheets')


        br.ensure_dir(self._output_path)

    @br.lazy_eval
    def cell_aggr_labels(self) :
        self.create_aggr_col_dicts()

    @br.lazy_eval
    def cell_aggr_col_dict(self) :

        self.create_aggr_col_dicts()

    @br.lazy_eval
    def nuc_aggr_col_dict(self) :
        self.create_aggr_col_dicts()

    @br.lazy_eval
    def nuc_aggr_labels(self) :
        self.create_aggr_col_dicts()

    ## will possibly replace some of output_cols
    def create_aggr_col_dicts(self) :

        one_cell = self.hsegs()[0].cells()[0]
        cell_hdings = one_cell.cell_data_hdings()   ## these hdings are for checking
        nuc_hdings = one_cell.nuc_data_hdings()

        cell_aggr_rows = []
        nuc_aggr_rows = []

        self._cell_aggr_labels = []
        self._nuc_aggr_labels = []

        for hseg in self.hsegs() :
            try :
                for cell in hseg.cells() :
                    if cell.cell_data_hdings() != cell_hdings :
                        raise BobException('exper.output: crap')

                    self._cell_aggr_labels.append(cell.get_short_id())
                    cell_aggr_rows.append(cell.cell_data())

                    if cell.nuc_data_hdings() != nuc_hdings :
                        raise BobException('exper.output: shit')
                    for nuc_label, nuc_row in sorted(cell.nuc_data().items()) :
                        self._nuc_aggr_labels.append(nuc_label)
                        nuc_aggr_rows.append(nuc_row)

            except Exception as e :
                print(e)
                print(hseg.name)

        self._cell_aggr_col_dict = {}
        for c in range(len(cell_hdings)) :
            col = []

            for r in range(len(cell_aggr_rows)) :
                col.append(cell_aggr_rows[r][c])

            self._cell_aggr_col_dict[cell_hdings[c]] = col
            ## cell_aggr_label indices match the indices of a col of cell_aggr_col_dict

        self._nuc_aggr_col_dict = {}
        for c in range(len(nuc_hdings)) :
            col = []

            for r in range(len(nuc_aggr_rows)) :
                col.append(nuc_aggr_rows[r][c])

            self._nuc_aggr_col_dict[nuc_hdings[c]] = col
            ## nuc_aggr_label indices match the indices of a col of nuc_aggr_col_dict

    # } </properties>


# { <general>

    def get_hseg(self, ind_key) :
        if type(ind_key) == int :
            return self.hsegs()[ind_key]
        elif type(ind_key) == str :
            return self.hsegs()[self.hsegs_dict()[ind_key]]
        else :
            raise(BobException("exper.get_hseg - ind_key must be an int or string"))

    def get_hseg_dict(self) :

        hseg_dict = {}
        for hseg in self.hsegs() :
            hseg_dict[hseg.name] = hseg

        return hseg_dict


    def deactivate_hseg(self, hseg_name, message=None) :

        print('error occured and hseg {} is no longer being processed'.format(hseg_name))
        hseg = self.get_hseg_dict()[hseg_name]
        hseg.inactive = True

        self._inactive_hseg_dict[hseg_name] = hseg


        hseg_ind = self._hsegs.index(hseg)
        del self._hsegs[hseg_ind]

        full_message = 'hseg {} deactivated'.format(hseg_name)
        if message != None :
            full_message += ': ' + message

        raise HsegDeactivated(full_message)

    def cell_iter(self) :
        for hseg in self.hsegs() :
            for cell in hseg.cells() :
                yield cell

    # } </general>

# { <processing>

    def make_data(self) :
        for hseg in self.hsegs() :
            try :
                hseg.make_data()
            except HsegDeactivated as hd :
                print(hd)

    # } </processing>

# { <output>
    def output_new_hdings(self) :
        cell_sheet = []
        nuc_sheet = []

        one_cell = self.hsegs()[0].cells()[0]
        cell_hdings = one_cell.cell_data_hdings()
        cell_hdings_temp = ['Label']
        cell_hdings_temp.extend(cell_hdings)
        cell_sheet.append(cell_hdings_temp)

        nuc_hdings = one_cell.nuc_data_hdings()
        nuc_hdings_temp = ['Label']
        nuc_hdings_temp.extend(nuc_hdings)
        nuc_sheet.append(nuc_hdings_temp)

        self.output_all_cols(cell_sheet, nuc_sheet)

    def output_old_hdings(self) :
        cell_sheet = []
        nuc_sheet = []

        one_cell = self.hsegs()[0].cells()[0]
        cell_hdings = one_cell.cell_data_hdings()
        cell_hdings_temp = ['Label']

        for hding in cell_hdings :
            cell_hdings_temp.append(hding.old_col_hding_str())


        cell_hdings_temp.extend(cell_hdings)
        cell_sheet.append(cell_hdings_temp)

        nuc_hdings = one_cell.nuc_data_hdings()
        nuc_hdings_temp = ['Label']
        for hding in nuc_hdings :
            nuc_hdings_temp.append(hding.old_col_hding_str())

        nuc_sheet.append(nuc_hdings_temp)

        self.output_all_cols(cell_sheet, nuc_sheet)

    def output_all_cols(self, cell_sheet, nuc_sheet) :
        """
        it is assumed that each sheet already has col hdings, and just needs data to be appended
        """
        one_cell = self.hsegs()[0].cells()[0]
        cell_hdings = one_cell.cell_data_hdings()   ## these hdings are for checking


        nuc_hdings = one_cell.nuc_data_hdings()


        for hseg in self.hsegs() :
            try :

                for cell in hseg.cells() :
                    if cell.cell_data_hdings() != cell_hdings :
                        raise BobException('exper.output: crap')

                    row = [cell.get_short_id()]
                    row.extend(cell.cell_data())
                    cell_sheet.append(row)

                    if cell.nuc_data_hdings() != nuc_hdings :
                        raise BobException('exper.output: shit')

                    for nuc_label, nuc_row in sorted(cell.nuc_data().items()) :
                        row = [nuc_label]
                        row.extend(nuc_row)
                        nuc_sheet.append(row)
            except Exception as e :
                print(e)
                print(hseg.name)
                # raise


        output_folder = br.dated_output_dir(self.path)

        cell_sheet_path = os.path.join(output_folder, '_'.join([self.name, 'cell-sheet.csv']))
        nuc_sheet_path = os.path.join(output_folder, '_'.join([self.name, 'Nuc-sheet.csv']))

        br.rows_to_csv(cell_sheet, cell_sheet_path)
        br.rows_to_csv(nuc_sheet, nuc_sheet_path)


    def output_cell_cols_def(self) :

        cell_col_hdings = self.make_bob_hdings_list(default_cell_output_hdings)
        self.output_cell_cols(cell_col_hdings)


    def output_cell_cols(self, cell_col_hdings) :

        rows = []
        for label in self.cell_aggr_labels() :
            rows.append([label])

        for cell_col_hding in cell_col_hdings :
            # br.temp_print(cell_col_hding)
            for i in range(len(self.cell_aggr_col_dict()[cell_col_hding])) :
                rows[i].append(self.cell_aggr_col_dict()[cell_col_hding][i])
        hdings = ['Labels']
        hdings.extend(cell_col_hdings)
        rows.insert(0, hdings)

        outpath = br.dated_file_path(self.output_path(), '_'.join([self.name, 'cells.csv']))
        # print(outpath)
        br.rows_to_csv(rows, outpath)
        print('cell data saved: {}'.format(outpath))


    def output_nuc_cols_def(self) :
        nuc_col_hdings = self.make_bob_hdings_list(default_nuc_output_hdings)
        self.output_nuc_cols(nuc_col_hdings)


    def output_nuc_cols(self, nuc_col_hdings) :

        # hdings = ['']
        # hdings.extend(nuc_col_hdings)
        # rows = [hdings]
        rows = []

        for label in self.nuc_aggr_labels() :
            rows.append([label])

        for nuc_col_hding in nuc_col_hdings :
            for i in range(len(self.nuc_aggr_col_dict()[nuc_col_hding])) :
                rows[i].append(self.nuc_aggr_col_dict()[nuc_col_hding][i])

        outpath = br.dated_file_path(self.output_path(), '_'.join([self.name, 'nucs.csv']))

        hdings = ['Labels']
        hdings.extend(nuc_col_hdings)
        rows.insert(0, hdings)

        br.rows_to_csv(rows, outpath)

        print('nuc data saved: {}'.format(outpath))


    def make_bob_hdings_list(self,input_hdings) :
        output_bob_hdings = []
        for item in input_hdings :
            # print(item)
            output_bob_hdings.append(BobHding.make_bob_hding(item, self.channel_dict()))
        return output_bob_hdings



    # } </output>

# { <to_string functions>

    def get_prefix(self) :
        """For logging: prints name tabbed out appropriately"""
        return self.name + ':'

    def get_id(self) :
        """
        id = <exper.name>[_<hseg.name>[_<cell.name>[_<nuc.name>]]]
        created by recursively calling parent.get_id()
        ends the recursive calls by return self.name
        """
        return self.name


    def __str__(self) :
        return self.get_id()

    def __repr__(self) :
        return self.get_id()

    # } </to_string functions>


# class ExperMetaData :
#
#     def __init__(hseg_slices
