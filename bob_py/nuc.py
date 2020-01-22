
import brutils as br

class Nuc :


    def __init__(self, cell, id_num, roi) :
        self.cell = cell
        self.id_num = id_num
        self.name = 'n-' + str(self.id_num)


        self._roi = roi             ## roi could be a member variable instead of a property but that would mean you'd have to remember what things were properties or not


# { <properties>

    @br.lazy_eval
    def roi(self) :
        ## only using br.lazy_eval for consistency, roi is always initialized in init
        pass

    @br.lazy_eval
    def vor_roi(self) :
        """use if none instead of try"""
        self.cell.create_vor_roi()

    # } </properties>

# { <general>

    def make_data_dict_label(self) :
        return (self.cell.hseg.name, self.cell.name, self.id_num)

    # } </general>

# { <to_string functions>

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

    def get_short_id_vor(self) :
        """
        short_id = <hseg.name>[_<cell.name>[_<nuc.name>]]
        created by recursively calling parent.get_short_id()
        """
        return '_'.join([self.cell.get_short_id(), 'v-{}'.format(self.id_num)])


    def __str__(self) :
        return self.get_short_id()

    def __repr__(self) :
        return self.get_short_id()

    # } </to_string functions>
