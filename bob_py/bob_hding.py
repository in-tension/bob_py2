from functools import total_ordering

import brutils as br
import fiji_utils as futils

from .bob_exception import BobException


@total_ordering
class BobHding (object) :

    POSS_STR_FUNCS = ["Avg", "Tot", "Norm"]
    POSS_ROI_SETS = ["Cell", "Nuc", "Vor"]
    POSS_PRJ_METHODS = ["avg", "min", "max", "sum", "sd", "median"]

    INCLUDE_PRJ_METHOD_IN_STR = False

    DEFAULT_PRJ_METHOD = "sum"

    DEBUG = False



    POSS_MSR_PARAMS = futils.GEO_HDINGS
    POSS_MSR_PARAMS.extend(futils.INTENS_HDINGS)

    MSR_PARAM_DICT = {'Perim.':'Perim', }

    for val in MSR_PARAM_DICT.values() :
        POSS_MSR_PARAMS.append(val)

    INTDEN_CHANGE = False

    INTDEN_DICT = {'IntDen':'SumIntens', 'RawIntDen':'RawSumIntens'}
    if INTDEN_CHANGE :
        MSR_PARAM_DICT.update(INTDEN_DICT)
        for val in MSR_PARAM_DICT.values() :
            POSS_MSR_PARAMS.append(val)


    @staticmethod
    def parse_channel_input(channel_input, channel_dict) :

        input_type = type(channel_input)
        if input_type == int :
            ch_def = BobChannelDef(channel_input, BobHding.DEFAULT_PRJ_METHOD)
            ch_str = channel_dict[ch_def]
        elif input_type == list :
            ch_def = BobChannelDef(*channel_input)
            ch_str = channel_dict[ch_def]

        elif input_type == str :
            ch_str = channel_input
            ch_def = channel_dict[ch_str]

        return ch_def, ch_str

    @staticmethod
    def make_bob_hding(args, channel_dict) :
        # print(args)
        if len(args) == 0 :
            raise BobException('BobHding.make_bob_hding: args empty')
        if len(args) == 1 and (isinstance(args[0], list)) :
            args = args[0]

        args_iter = args.__iter__()

        roi_set = next(args_iter)
        if roi_set not in BobHding.POSS_ROI_SETS :
            raise BobException('BobHding.make_bob_hding: unknown roi_set {}'.format(roi_set))

        try :
            temp = next(args_iter)
        except StopIteration :
            return BobHding(roi_set=roi_set)


        if temp in BobHding.POSS_MSR_PARAMS :
            channel_def = None
            channel_name = None
            msr_param = temp
        else :
            channel_def, channel_name = BobHding.parse_channel_input(temp, channel_dict)
            try :
                msr_param = next(args_iter)
                if msr_param not in BobHding.POSS_MSR_PARAMS :
                    raise BobException('BobHding.make_bob_hding: unknown msr_param {}'.format(msr_param)) ##
            except StopIteration :
                return BobHding(roi_set=roi_set, channel_def=channel_def, channel_name=channel_name)


        try :
            func = next(args_iter)
        except StopIteration :
            func = None

        return BobHding(roi_set=roi_set, msr_param=msr_param, channel_def=channel_def, channel_name=channel_name, func=func)


    def __init__(self, msr_param=None, roi_set=None, channel_def=None, channel_name=None, func=None, ) :


        self.set_msr_param(msr_param)
        self.roi_set = roi_set
        self.channel_def = channel_def
        self.channel_name = channel_name

        self.func = func


    def old_col_hding_str(self) :


        if self.channel_name == None :
            src = self.roi_set.title()
            if src == "Vor" :
                src = "Voronoi"

        else :
            src = self.channel_name

        if self.func is not None :
            old_col_hding = '-'.join([self.func.title(),self.msr_param, src])
        else :
            old_col_hding = '-'.join([self.msr_param, src])

        return old_col_hding


    def is_geo(self) :
        return self.channel_def == None

    def is_cell_sheet(self) :
        if self.roi_set == "Cell" :
            return True

        elif self.func == "Avg" or self.func == "Tot" :
            return True

        else :
            return False


    def set_msr_param(self, new_msr_param) :
        if new_msr_param in BobHding.MSR_PARAM_DICT :
            new_msr_param = BobHding.MSR_PARAM_DICT[new_msr_param]
        self.msr_param = new_msr_param


    def __str__(self) :
        func = self.func
        if func is not None :
            func = func.title()

        parts_raw = [func, self.msr_param, self.channel_name, self.roi_set]
        parts = [str(s) for s in parts_raw if s is not None]
        return '_'.join(parts)

    def __repr__(self) :

        return self.__str__()

    def __hash__(self) :
        hash_str = '{},{},{},{},{}'.format(self.msr_param, self.roi_set, self.channel_def, self.channel_name, self.func)
        return hash(hash_str)

    def __eq__(self, other) :
        return hash(self) == hash(other)

    def __gt__(self, other) :
        return self.msr_param > other.msr_param



class BobChannelDef :
    DEFAULT_PRJ_METHOD = "sum"
    POSS_PRJ_METHODS = ["avg", "min", "max", "sum", "sd", "median"]


    def __init__(self, arg) :

        if type(arg) == int :
            self.num = arg
            self.prj_method = BobChannelDef.DEFAULT_PRJ_METHOD

        elif type(arg) == list :
            self.num = arg[0]
            self.prj_method = arg[1]



        if type(self.prj_method) != str :
            raise BobException('BobChannelDef:init:prj_method-type')
        if self.prj_method not in BobChannelDef.POSS_PRJ_METHODS :
            raise BobException('BobChannelDef:init:prj_method-val')


    def __str__(self) :
        if self.prj_method == "sum" :
            return 'Ch{}'.format(self.num)
        else :
            return 'Ch{}-{}'.format(self.num, self.prj_method)

    def __repr__(self) :
        return 'BobChannel: {}, {}'.format(self.num, self.prj_method)

    def __hash__(self) :
        return hash('{},{}'.format(self.num, self.prj_method))

    def __eq__(self, other) :
        return hash(self) == hash(other)
