raw_str = """def {0}(self) :
    try :
        return self._{0}
    except :
        self.{1}()
        return self._{0}"""

def gen_boiler_plate(var, *args) :
    if len(args) >= 1 and args[0] != None :
        func = args[0]
    else :
        func = '_'.join(["create", var])

    raw_str = """def {0}(self) :
        try :
            return self._{0}
        except :
            self.{1}()
            return self._{0}"""

    new_str = raw_str.format(var, func)
    print(new_str)
    print()
    # return new_str



def gen_boiler(vars, funcs) :
    for var, func in zip(vars, funcs) :
        gen_boiler_plate(var,func)
