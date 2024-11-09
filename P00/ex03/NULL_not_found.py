import math

def NULL_not_found(object: any) -> int:
    # Vérification du type et impression du format spécifique pour chaque cas
    if object is None:
        print(f"Nothing: None <class 'NoneType'>", end="\n")
        return 0
    elif isinstance(object, float) and math.isnan(object): #verifiez si c'est un float et verifiez si il est nul ou pas nan
        print(f"Cheese: nan <class 'float'>", end="\n")
        return 0
    elif object == 0 and isinstance(object, int): #verifiez si c'est un int et si ce int = 0 
        print(f"Zero: 0 <class 'int'>", end="\n")
        return 0
    elif object == "": #verifiez si c'est un string
        print(f"Empty: <class 'str'>", end="\n")
        return 0
    elif object is False: #verifiez si c'est un bool
        print(f"Fake: False <class 'bool'>", end="\n")
        return 0
    else:
        print("Type not Found", end="\n")
        return 1
