
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
        """init"""
        self.hseg = hseg
        self.name = name
        self.roi_csv_path = cell_path

        self._nucs = []
        self._nuc_dict = {}

## <properties>

    def roi(self) :
        """roi of cell"""
        try :
            return self._roi
        except :
            self._roi = Cell.read_roi_csv(self.roi_csv_path, self.hseg.cal())
            return self._roi

    def nucs(self) :
        """
        nucs of cell

        unlike others, instead of checking if exists,
        checks if empty
        this is because instead of being created by cell,
        it is easiest to create nuc in hseg and then match to cell
        thus _nucs needs to be initialized in __init__
        """
        if len(self._nucs) > 0 :
            return self._nucs
        else :
            self.hseg.create_nucs()


    ## </properties>

## <create properties>

    def add_nuc(self, nuc_roi) :
        """
        adds a nuc to self._nucs (self.nucs())
        called by hseg.create_nucs
        """
        nuc_id_num = len(self._nucs)
        self._nucs.append(Nuc(self, nuc_id_num, nuc_roi))
        self._nuc_dict[self._nucs[-1].name] = nuc_id_num


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
        print('creating_vor_roi')
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
        IJ.run(nuc_bin_copy, "Invert", "")

        nuc_bin_copy.setRoi(self.roi())
        IJ.run(nuc_bin_copy, "Analyze Particles...", "add")
        vor_rois = rm.getRoisAsArray()

        futils.force_close(nuc_bin_copy)

        return vor_rois
        # self.match_vor_nuc(vor_rois)


    def match_vor_nuc(self, vor_rois) :
        """
            matches vor_rois with their respective nucs
            by checking if nuc_cent in vor_roi

            currently having issues/not working
        """
        # if IJ.escapePressed() : IJ.exit()

        print("match_vor_nuc")
        rm = RoiManager.getRoiManager()
        nuc_inds = [x for x in range(len(self.nucs()))]
        print(nuc_inds)
        for vor_roi in vor_rois :
            # print(vor_roi)
            # print(nuc_inds)

            temp = None
            for i, nuc_ind in enumerate(nuc_inds) :
                nuc_roi = self.nucs()[nuc_ind].roi()
                print('\t{}'.format(nuc_roi))

                nuc_cent = futils.roi_cent(nuc_roi, integer=True)

                if vor_roi.contains(*nuc_cent) :
                    print("huh")
                    self.nucs()[nuc_ind]._vor_roi = vor_roi
                    ## I don't think I need to do this, I could just use i outside of loop but it feels so insecure or something
                    temp = i
                    break

            else :
                IJ.log('self: {}, issue with voronoi nuc match up'.format(self.name))
                rm.reset()
                for i, nuc in enumerate(self.nucs()) :

                    x = int(nuc.roi.getXBase())
                    y = int(nuc.roi.getYBase())
                    IJ.log('{}. ({},{})'.format(i,x,y))
                    futils.add_roi(Roi(x,y,10,10), str(i))
                IJ.log(str(nuc_inds))
                futils.add_roi(vor_roi, "vor_roi")

                ## raise RuntimeError('self: {}, issue with voronoi nuc match up'.format(self.name))

            if temp is not None :
                del nuc_inds[temp]




    ## </create properties>




## <to_string functions>

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

    ## </to_string functions>


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
