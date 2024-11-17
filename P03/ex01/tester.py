from S1E7 import Baratheon, Lannister

# Tester la classe Baratheon
Robert = Baratheon("Robert")
print(Robert.__dict__)          # Affiche les attributs de Robert
print(Robert.__str__())         # Affiche la description du personnage avec __str__
print(Robert.__repr__())        # Affiche la représentation officielle du personnage avec __repr__
print(Robert.is_alive)          # Vérifie si Robert est en vie
Robert.die()                    # Tue Robert
print(Robert.is_alive)          # Vérifie si Robert est en vie après die
print(Robert.__doc__)           # Affiche la docstring de la classe Baratheon

print("---")

# Tester la classe Lannister
Cersei = Lannister("Cersei")
print(Cersei.__dict__)          # Affiche les attributs de Cersei
print(Cersei.__str__())         # Affiche la description du personnage avec __str__
print(Cersei.is_alive)          # Vérifie si Cersei est en vie

print("---")

# Tester la méthode de classe create_lannister
Jaine = Lannister.create_lannister("Jaine", True)
print(f"Name : ({Jaine.first_name}, {type(Jaine).__name__}), Alive : {Jaine.is_alive}")
