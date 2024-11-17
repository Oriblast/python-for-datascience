class calculator:
    """pour acceder au meme index d'un autre vecteur dont on connait la valeurs actuelle
il suffit de faire vecteur2[vecteur1.index(i)] o ce qui est entre crochet devient index de la valeus de i
val:.1f signifie la valeurs de val avec un chiffre apres la virgule val etant un nombre decimal"""
    @staticmethod
    def dotproduct(V1: list[float], V2: list[float]) -> None:
        """produit sclaire = doc product
Produit scalaire= 
i=0
∑
n
V1[i]*V2[i] pour v[1,2,3] et v1 [5, 6 , 7] sca = 1 * 5 + 2 * 6 + 3 * 7"""

        dot_prod = 0.0
        for i in V1:
            dot_prod += i * V2[V1.index(i)]
        print(f"dot product is : {int(dot_prod)}")


    @staticmethod
    def add_vec(V1: list[float], V2: list[float]) -> None:
        """Addition de deux vecteurs"""
        addvec = []
        for i in V1:
            addvec.append(i + V2[V1.index(i)])
        print(f"add Vector is: {[f'{val:.1f}' for val in addvec]}")
            

    @staticmethod
    def sous_vec(V1: list[float], V2: list[float]) -> None:
        """Soustraction des vecteurs"""
        svec = []
        for i in V1:
            svec.append(i - V2[V1.index(i)])
        print(f"Sous Vector is: {[f'{val:.1f}' for val in svec]}")

