

class OutputColumn :
    NAME_SUF = "name:"
    CELL_SPRDSHEET = "Cell"


    def __init__(self, input_str, spreadsheet=None) :
        self.name = None
        self.spreadsheet = spreadsheet


        input_str_parts = input_str.split('_')
        if input_str_parts[-1].startswith(OutputColumn.NAME_SUF) :
            self.name = input_str_parts[-1].replace(OutputColumn.NAME_SUF, '')
            input_str_parts = input_str_parts[:-1]

        if len(input_str_parts) == 3 :
            self.func = input_str_parts[0]
            input_str_parts = input_str_parts[1:]

        self.msrment = input_str_parts[0]
        self.dataset = input_str_parts[1]

        if self.name == None :
            self.name = self.make_default_name()


    def make_default_name(self) :
        if spreadsheet == OutputColumn.CELL_SPRDSHEET && self.dataset != "Cell":
            if self.func == None :
                tojoin = [self.dataset, self.msrment]
            else :
                tojoin = [self.dataset, self.func, self.msrment]

        else :
            if self.func == None :
                tojoin = [self.msrment, self.dataset]
            else :
                tojoin = [self.func, self.msrment, self.dataset]

        return "_".join(tojoin)
