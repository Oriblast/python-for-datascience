def afficher_tout(*args, **kwargs):
    print("Arguments positionnels :")
    for arg in args:
        print(arg)
    
    print("Arguments nommés :")
    for key, valeur in kwargs.items():
        print(f"{key}:{valeur}")

afficher_tout(1, 2, 3, nom="Bob", age=25)