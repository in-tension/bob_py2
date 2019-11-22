
class Nuc :

    def __init__(self, cell, id_num, roi) :
        self.cell = cell
        self.id_num = id_num
        self.name = 'n' + str(self.id_num)


        # self.roi = roi
        # self.vor_roi = None

    ## <properties>

    def roi(self) :
        try :
            return self._roi
        except :
            self.get_roi()
            return self._roi

    def vor_roi(self) :
        try :
            return self._vor_roi
        except :
            self.get_vor_roi()
            return self._vor_roi


    ## </properties>




    def get_prefix(self) :
        return '  '*3 + self.get_long_name() + ':'


    def get_id(self) :
        return '_'.join([self.cell.get_id(), self.name])

    def short_id(self) :
        s_id = self.get_id()
        s_id = s_id.replace(self.cell.hseg.exper.name+'_','')
        # print(self.cell.hseg.exper.name)
        return s_id


    def __str__(self) :
        return self.short_id()

    def __repr__(self) :
        return self.short_id()
