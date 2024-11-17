from abc import ABC, abstractmethod

class Character(ABC):
    """
    base class for creating character  
    def __init__ are fonction of construction 
    and die are abstract method of dead
    @abstratmethod -> show that die should imprémentary by class girl  
    """

    def __init__(self, first_name, is_alive=True):
        """constructor of character"""

        self.first_name = first_name
        self.is_alive = is_alive
    @abstractmethod
    def die(self):
        """abstract method that will been implémentary by class heritage"""
        pass

class Stark(Character):
    """class girl for Character"""

    def __init__(self, first_name, is_alive=True):
        """here the constructor for girl class call 
class mother with fonction super().__init__ sans le self"""
        super().__init__(first_name, is_alive)

    def die(self):
        """change the situation of alive in dead """
        
        self.is_alive = False