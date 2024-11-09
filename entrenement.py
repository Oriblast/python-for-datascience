class animal:

    def __init__(self, nom, crit, attaque, degat, health):
        self.nom = nom 
        self.crit = crit
        self.attaque = attaque
        self.degat = degat
        self.health = health
        print(f"animal {nom} apparait {crit} attaque {attaque} degat {degat}\n")
    
    def get_nom(self):
        return self.nom
    def get_health(self):
        return self.health
    def get_degat(self):
        return self.degat
    def evolution(self):
        self.degat += 50

    def set_health(self, taget):
        print(f"{self.nom} attaque {taget.get_nom()}\n")
        self.health -= taget.get_degat()
        print(f"{self.nom} il vous rest {self.health}\n") 
        if (self.health == 0):
            print("vous etes mort")
    

def main():
    animal1 = animal("insect", "ziziz", "piqure", 30, 200)
    animal2 = animal("tigre", "grrrraaaaaaa", "griffe", 200, 500)
    animal1.set_health(animal2)
if __name__ == "__main__":
    main()       
