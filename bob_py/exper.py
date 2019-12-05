"""
abbr.
    prj = projection
    hseg = hemisegment
    exper = experiment
    suf = suffix
    msr_param = measurment parameter
"""

## ignore: todo : I think making the projections is a little slow
## ignore: change to see if they exist and save after if not
## runs fine if I select a different fucking application
##
## also make an iterator for exper to iterate throught the hseg
## where in the __next__ function it checks to see if macro has been cancelled



import os
import json
import traceback

from ij import IJ, WindowManager
from ij.measure import ResultsTable
from ij.gui import NonBlockingGenericDialog, Roi, PolygonRoi
from ij.io import DirectoryChooser
from ij.plugin import Duplicator
from ij.plugin.frame import RoiManager

import fiji_utils as futils

from .hseg import Hseg



class Exper :
    IN_DEV = True
    ONE_HSEG = False
    CATCH = False


    PRINT_PROGRESS = True

    JSON_KEY_SLICES = 'hseg slices'
    JSON_KEY_CHANNELS = 'channels'
    JSON_KEY_CALC = 'calc'
    JSON_SUF = '.json'
    JSON_SPLIT_CHAR = 'json:'

    TEMP_OUT_DIR = 'temp_out_dir'

    POSS_ROI_DICTS = {"cell" : "hseg", "nuc" : "cell", "vor" : "cell"}





    def __init__(self, path) :
        self.path = path

        dir_name = os.path.basename(self.path)
        name = dir_name.split('_')[:2]
        self.name = '_'.join(name)


        self._data = {"cell":{}, "vor":{}, "nuc":{}}





## <properties>

    def hsegs(self) :
        try :
            return self._hsegs
        except :

            self.create_hsegs()
            return self._hsegs

    def hseg_dict(self) :
        try :
            return self._hseg_dict
        except :

            self.create_hsegs()
            return self._hseg_dict


    def channels(self) :
        """
            dict
            keys -> channel_num
            vals -> [channel_name, [prj_method, roi_set_name]]
        """
        try :
            return self._channels
        except :
            self.load_json_info()
            return self._channels

    def prj_method_dict(self) :
        """
            dict
            keys -> prj_method
            vals -> [[channel_num, roi_set_name]]

            Is simply a reorganization of some of the data in channels
        """
        try :
            return self._prj_method_dict
        except :
            self.load_json_info()
            return self._prj_method_dict

    def hseg_slices(self) :
        """
            dict
            keys -> hseg_name
            vals -> pairs of ints -> starting and ending slices to be used for that hseg
        """
        try :
            return self._hseg_slices
        except :
            self.load_json_info()
            return self._hseg_slices


    def calc_dict(self) :
        """
            currently
            dict for each roi_set (cell/vor/nuc)
            with what measurements to calculate (e.g. "Norm": ["Area"]

            and a dict for each channel and what to calc

            I think I'm gonna make this as some sort of default and it can be added to
        """
        try :
            return self._calc_dict
        except :
            self.load_json_info()
            return self._calc_dict


    def rearranged_data(self) :
        try :
            return self._rearranged_data
        except :
            self.create_rearranged_data()
            return self._rearranged_data

    def create_rearranged_data(self) :
        self._rearranged_data = {}
        msr_param_dict = self.msr_param_dict()


        for sheet_name in msr_param_dict.keys() :
            self._rearranged_data[sheet_name] = {}
            sheet_dict = msr_param_dict[sheet_name]

            for data_src in sheet_dict.keys() :
                self._rearranged_data[sheet_name][data_src] = {}
                msr_params = sheet_dict[data_src]

                for msr_param in msr_params :
                    if type(msr_param) == str :
                        self._rearranged_data[sheet_name][data_src].update( self.get_data(data_src))
                    else :
                        ## calc data
                        pass


    def aggr_data(self) :
        # print('dafuq? {}'.format(self._aggr_data))
        try :
            return self._aggr_data
        except :
            self.create_aggr_data()
            return self._aggr_data

    def create_aggr_data(self) :
        self._aggr_data = {}
        msr_param_dict = self.msr_param_dict()
        # print(msr_param_dict)

        for sheet_name in msr_param_dict.keys() :
            self._aggr_data[sheet_name] = {}
            sheet_dict = msr_param_dict[sheet_name]

            for data_src in sheet_dict.keys() :
                # print(data_src)
                self._aggr_data[sheet_name][data_src] = self.get_data(data_src)








    def get_data(self, data_src) :
        try :
            data_src_level = Exper.POSS_ROI_DICTS[data_src[0]]
        except :
            raise Exception('no roi_dict called {}'.format(roi_dict_name))

        data = {}

        if data_src_level == "hseg" :
            for hseg in self.hsegs() :
                data.update(hseg.data(data_src))
                # pass
                # raw_data
        else :
            for hseg in self.hsegs() :
                for cell in hseg.cells() :
                    data.update(cell.data(data_src))
        return data







    def msr_param_dict(self) :
        try :
            return self._msr_param_dict
        except :
            self.create_msr_param_dict()
            return self._msr_param_dict

    ## need to figure out where and how I'm actually gonna get this information
    ## this way is only temporary
    def create_msr_param_dict(self) :
        from msr_param_dict import msr_param_dict
        self._msr_param_dict = msr_param_dict


    ## </properties>

## <create properties>

    # {
    # def load_json_info(self) :
    #     """
    #     read json file with metadata and intialize relevant properties
    #     creates channels, prj_method_dict, and hseg_slices
    #     """
    #     json_file_path = os.path.join(self.path, self.name + Exper.JSON_SUF)
    #
    #     if not os.path.exists(json_file_path) :
    #         IJ.log('no experiment json file for experiment {}\npath:{}'.format(self.name, json_file_path))
    #
    #     else :
    #         with open(json_file_path, 'r') as f :
    #             raw_text = f.read()
    #
    #         ignore, json_text = raw_text.split(Exper.JSON_SPLIT_CHAR)
    #         json_raw = json.loads(json_text)
    #         self._hseg_slices = json_raw[Exper.JSON_KEY_SLICES]
    #         self._calc_dict = json_raw[Exper.JSON_KEY_CALC]
    #
    #         channels_raw = json_raw[Exper.JSON_KEY_CHANNELS]
    #         self._channels = {int(key): value for key, value in channels_raw.items()}
    #
    #         self._prj_method_dict = {}
    #
    #         for channel, info_list in self._channels.items() :
    #             if info_list[1] == None :
    #                 continue
    #
    #             channel_name = info_list[0]
    #             print('info_list = {}'.format(info_list))
    #             for pair in info_list[1:] :
    #                 # print(pair)
    #                 prj_method = pair[0]
    #                 roi_set_name = pair[1]
    #
    #                 if prj_method not in self._prj_method_dict :
    #                     self._prj_method_dict[prj_method] = [[channel, roi_set_name]]
    #
    #                 else :
    #                     self._prj_method_dict[prj_method].append([channel, roi_set_name])
    # }


    def load_json_info(self) :
        """
        read json file with metadata and intialize relevant properties
        creates channels, prj_method_dict, and hseg_slices
        """
        json_file_path = os.path.join(self.path, self.name + Exper.JSON_SUF)

        if not os.path.exists(json_file_path) :
            IJ.log('no experiment json file for experiment {}\npath:{}'.format(self.name, json_file_path))

        else :
            with open(json_file_path, 'r') as f :
                raw_text = f.read()

            ignore, json_text = raw_text.split(Exper.JSON_SPLIT_CHAR)
            json_raw = json.loads(json_text)
            self._hseg_slices = json_raw[Exper.JSON_KEY_SLICES]
            self._calc_dict = json_raw[Exper.JSON_KEY_CALC]

            channels_raw = json_raw[Exper.JSON_KEY_CHANNELS]
            self._channels = {int(key): value for key, value in channels_raw.items()}
            self._ch_name_to_num = {value[0] : int(key) for key, value in channels_raw.items()}

            # self._prj_method_dict = {}

            # for channel, info_list in self._channels.items() :
            #     if info_list[1] == None :
            #         continue
            #
            #     channel_name = info_list[0]
            #     print('info_list = {}'.format(info_list))
            #     for pair in info_list[1:] :
            #         # print(pair)
            #         prj_method = pair[0]
            #         roi_set_name = pair[1]
            #
            #         if prj_method not in self._prj_method_dict :
            #             self._prj_method_dict[prj_method] = [[channel, roi_set_name]]
            #
            #         else :
            #             self._prj_method_dict[prj_method].append([channel, roi_set_name])

    def create_hsegs(self) :
        """find hseg directories and initialize hseg"""
        files = os.listdir(self.path)
        self._hsegs = []
        self._hseg_dict = {}
        for file_name in files :
            if file_name.startswith(self.name) and os.path.isdir(os.path.join(self.path, file_name)):
                #self.self._hsegs[f.replace(self.name + '_','')] = InputHseg(self, f)
                if Exper.IN_DEV :
                    self._hsegs.append(Hseg(self, file_name))
                    self._hseg_dict[self._hsegs[-1]] = len(self._hsegs) - 1
                else :
                    try :
                        self._hsegs.append(Hseg(self, file_name))
                        self._hseg_dict[self._hsegs[-1]] = len(self._hsegs) - 1
                    except Exception as e :
                        print('exception trying to init hseg {}: {}'.format(file_name, e))

    ## </create properties>

## <other>

    # def save_cell_sheet(self) :
    #     for hseg in self.hsegs() :
    #         # for cell in hseg.cells() :
    #         pass
    # def get_dev_sheet_dicts(self) :
    #     from temp import ihe_dict
    #     self.sheet_dicts = ihe_dict
    #

    def aggr_data_old(self) :
        from temp import ihe_dict
        self.all_hseg_data = {}
        self.all_cell_data = {}

        for sheet_dict in ihe_dict.values() :
            for data_key in sheet_dict.keys() :
                if type(data_key[1]) == str :
                    data_key = (data_key[0], (data_key[1],))
                try :
                    data_src_level = Exper.POSS_ROI_DICTS[data_key[0]]
                except :
                    raise Exception('no roi_dict called {}'.format(roi_dict_name))

                if data_src_level == "hseg" :

                    for hseg in self.hsegs() :
                        # self.all_cell_sheet_data.append(hseg.data(data_key))
                        hseg_data = hseg.data(data_key)
                else :
                    try :
                        for hseg in self.hsegs() :
                            for cell in hseg.cells() :
                                pass
                                # self.all_nuc_sheet_data.append(cell.data(data_key))
                    except Exception as e :
                        print(e)
        # futils.jpprint(all_cell_sheet_data)

    # def sort_sheet_data(self) :
    #     try :
    #         self.all_cell_sheet_data
    #     except :
    #         self.get_all_sheet_data()
    #
    #
    #     cell_sheet_data = {}
    #     for group in self.all_cell_sheet_data :
    #


    def dev_create_default_data(self) :
        from temp import ihe_dict

        for sheet_dict in ihe_dict.values() :
            for data_key in sheet_dict.keys() :
                if type(data_key[1]) == str :
                    data_key = (data_key[0], (data_key[1],))
                try :
                    data_src_level = Exper.POSS_ROI_DICTS[data_key[0]]
                except :
                    raise Exception('no roi_dict called {}'.format(roi_dict_name))

                if data_src_level == "hseg" :
                    for hseg in self.hsegs() :
                        hseg.data(data_key)
                else :
                    try :
                        for hseg in self.hsegs() :
                            for cell in hseg.cells() :
                                cell.data(data_key)
                    except Exception as e :
                        print(e)



    def create_out_dir(self) :
        out_dir_path = os.path.join(self.path, Exper.TEMP_OUT_DIR)

        if not os.path.exists(out_dir_path) :
            os.mkdir(out_dir_path)

        return out_dir_path

    def get_channel_name(self, channel_num) :
        return self.channels[channel_num][0]

    def get_channel_num(self, channel_name) :
        return self._ch_name_to_num[channel_name]


    def get_hseg(ind_key) :
        if type(ind_key) == int :
            return self.hsegs()[ind_key]
        elif type(ind_key) == str :
            return self.hsegs()[self.hsegs_dict()[ind_key]]
        else :
            raise(BobException("exper.get_hseg - ind_key must be an int or string"))

    ## </other

## <to_string functions>

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

    ## </to_string functions>


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
