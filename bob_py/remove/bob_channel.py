



class BobChannel :



    def __init__(self, num, prj_method) :
        self.num = num
        self.prj_method = prj_method




    def __hash__(self) :
        return hash(repr(self))

    def __eq__(self, other) :
        return hash(self) == hash(other)


    def __str__(self) :
        if prj_method == "sum" :
            return 'Ch{}'.format(self.num)
        else :
            return 'Ch{}-{}'.format(self.num, self.prj_method)

    def __repr__(self) :
        return 'BobChannel: {}, {}'.format(self.num, self.prj_method())
