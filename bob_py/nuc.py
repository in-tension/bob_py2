
class Nuc :

    def __init__(self, cell, id_num, roi) :
        self.cell = cell
        self.id_num = id_num
        self.name = 'n' + str(self.id_num)


        self._roi = roi
        self._vor_roi = None

## <properties>

    def roi(self) :
        try :
            return self._roi
        except :
            return self._roi

    def vor_roi(self) :
        """use if none instead of try"""
        if self._vor_roi != None :
            return self._vor_roi
        else :
            self.cell.create_vor_roi()
            return self._vor_roi
        # try :
        #     return self._vor_roi
        # except :
        #     self.cell.create_vor_roi()
        #     return self._vor_roi


    ## </properties>



## <to_string functions>

    def get_prefix(self) :
        """For logging: prints name tabbed out appropriately"""
        return '  '*3 + self.get_long_name() + ':'

    def get_id(self) :
        """
        id = <exper.name>[_<hseg.name>[_<cell.name>[_<nuc.name>]]]
        created by recursively calling parent.get_id()
        """
        return '_'.join([self.cell.get_id(), self.name])

    def get_short_id(self) :
        """
        short_id = <hseg.name>[_<cell.name>[_<nuc.name>]]
        created by recursively calling parent.get_short_id()
        """
        return '_'.join([self.cell.get_short_id(), self.name])


    def __str__(self) :
        return self.get_short_id()

    def __repr__(self) :
        return self.get_short_id()

    ## </to_string functions>
