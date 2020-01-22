



class BobException(Exception) :

    def __init__(self, message, *args, **kwargs) :
        self.actual_message = message
        Exception.__init__(self, args, kwargs)


    def __str__(self) :
        return self.actual_message

    def __repr__(self) :
        return self.__str__()


class HsegDeactivated(BobException) :
    pass
    # def __init__(self)
