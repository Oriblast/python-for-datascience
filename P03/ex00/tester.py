from S1E9 import Character, Stark

# Création d'une instance de Stark
Ned = Stark("Ned")
print(Ned.__dict__)  # Affiche les attributs de Ned
print(Ned.is_alive)  # Vérifie si Ned est en vie
Ned.die()            # Tue Ned en changeant son état
print(Ned.is_alive)  # Vérifie si Ned est en vie après avoir appelé die
print(Ned.__doc__)   # Affiche la docstring de la classe Stark
print(Ned.__init__.__doc__)  # Affiche la docstring du constructeur
print(Ned.die.__doc__)       # Affiche la docstring de la méthode die
print("---")

# Création d'une autre instance de Stark
Lyanna = Stark("Lyanna", False)
print(Lyanna.__dict__)  # Affiche les attributs de Lyanna
