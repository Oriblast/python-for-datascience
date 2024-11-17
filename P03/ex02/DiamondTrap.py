from S1E7 import Baratheon, Lannister

class King(Baratheon, Lannister):
    """king of baratheon and lannister and joffrey of game of trones"""

    def __init__(self, first_name, is_alive=True):
        """fonction that init the king"""

        super().__init__(first_name, is_alive=True)
    
    @property
    def eyes(self):
        """method getter eyes"""
        return self.yes
    @eyes.setter
    def eyes(self, color):
        """method setter eyes"""
        self.yes = color

    @property
    def hairs(self):
        """method detter hairs"""
        return self.airs
    @hairs.setter
    def hairs(self, color):
        """setter hairs"""
        self.airs = color

    def set_eyes(self, color):
        """Méthode pour changer la couleur des yeux du roi."""
        self._eyes = color

    def set_hairs(self, color):
        """Méthode pour changer la couleur des cheveux du roi."""
        self.hairs = color

    def get_eyes(self):
        """Méthode pour obtenir la couleur des yeux du roi."""
        return self._eyes

    def get_hairs(self):
        """Méthode pour obtenir la couleur des cheveux du roi."""
        return self.hairs
    

