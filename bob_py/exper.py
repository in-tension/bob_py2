"""
abbr.
    prj = projection
    hseg = hemisegment
    exper = experiment
    suf = suffix
"""



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





    @staticmethod
    def setup() :
        """setup"""

        if Exper.IN_DEV :
            canceled = False
        else :
            canceled = not IJ.showMessageWithCancel(__program__,'To proceed program will close all open images and windows, continue?')

        if not canceled :

            ## aspirational todo: identify current settings and return settings at the end
            ## set setting to save column headers
            IJ.run("Input/Output...", "jpeg=85 gif=-1 file=.csv use_file save_column");

            ## set setting to copy column headers - not actually necessary
            IJ.run("Input/Output...", "jpeg=85 gif=-1 file=.csv copy_column save_column");

            futils.force_close_all_images()
            rm = RoiManager.getRoiManager()
            rm.reset()
            rm.show()


    def    __init__(self, path) :
        self.path = path

        dir_name = os.path.basename(self.path)
        name = dir_name.split('_')[:2]
        self.name = '_'.join(name)

    # def load_exper(self) :



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



    ## </properties>

## <create properties>

    def load_json_info(self) :
        """read json file with metadata and intialize relevant properties"""
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

            self._prj_method_dict = {}

            for channel, info_list in channels.items() :
                if info_list[1] == None :
                    continue

                channel_name = info_list[0]
                print("info_list = {}".format(info_list))
                for pair in info_list[1:] :
                    # print(pair)
                    prj_method = pair[0]
                    roi_set_name = pair[1]

                    if prj_method not in prj_method_dict :
                        self._prj_method_dict[prj_method] = [[channel, roi_set_name]]

                    else :
                        self._prj_method_dict[prj_method].append([channel, roi_set_name])

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
                        print("exception trying to init hseg {}: {}".format(file_name, e))

    ## </create properties>


    def create_out_dir(self) :
        out_dir_path = os.path.join(self.path, Exper.TEMP_OUT_DIR)

        if not os.path.exists(out_dir_path) :
            os.mkdir(out_dir_path)

        return out_dir_path

    def get_channel_name(self, channel_num) :
        return self.channels[channel_num][0]




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
