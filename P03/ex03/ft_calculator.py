class calculator:
    """classe calculator"""
    
    def __init__(self, vector):
        """init vecto and classe"""
        self.vector = vector

    def __add__(self, object) -> None:
        """add the ele of vector and object"""
        self.vector = [x + object for x in self.vector]
        print(self.vector)
        return [x + object for x in self.vector]

    def __mul__(self, object) -> None:
        """mul the élements of the vector"""
        self.vector = [x * object for x in self.vector]
        print(self.vector)
        return [x * object for x in self.vector]


    def __sub__(self, object) -> None:
        """sub element of vector and object"""
        self.vector = [x - object for x in self.vector]
        print(self.vector)
        return [x - object for x in self.vector]

    def __truediv__(self, object) -> None:
        """div elements of vector"""
        if object == 0:
            raise ZeroDivisionError("the division by zero is not autoryser")
        self.vector = [x / object for x in self.vector]
        print(self.vector)
        return [x / object for x in self.vector]