from S1E9 import Character

class Baratheon(Character):
    """representing Baratheon family."""

    def __init__(self, first_name, is_alive=True):
        """init"""
        super().__init__(first_name, is_alive)
        
        self.family_name = "Baratheon"
        self.eyes = "brown"
        self.hairs = "dark"

    def die(self):
        """dear or alive"""
        self.is_alive = False

    def __str__(self):
        """ return string caracteristic for character"""
        return f"<bound method Baratheon.__str__ of Vector: ('{self.family_name}', '{self.eyes}', '{self.hairs}')>"
    
    def __repr__(self):
        """ return string caracteristic for character"""
        return f"<bound method Baratheon.__repr__ of Vector: ('{self.family_name}', '{self.eyes}', '{self.hairs}')>"


class Lannister(Character):
    """representing Lannister family"""
    def __init__(self, first_name, is_alive=True):
        """init"""
        super().__init__(first_name, is_alive)
        
        self.family_name = "Lannister"
        self.eyes = "Blue"
        self.hairs = "light"

    def die(self):
        """dear or alive"""
        self.is_alive = False

    def __str__(self):
        """ return string caracteristic for character"""
        return f"<bound method Lannister.__str__ of Vector: ('{self.family_name}', '{self.eyes}', '{self.hairs}')>"
    
    def __repr__(self):
        """ return string caracteristic for character"""
        return f"<bound method Lannister.__repr__ of Vector: ('{self.family_name}', '{self.eyes}', '{self.hairs}')>"
    @classmethod
    def create_lannister(cls, first_name, is_alive):
        """method of creation of new Lannister (kid)"""
        return cls(first_name, is_alive)

