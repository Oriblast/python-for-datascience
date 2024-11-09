import sys

def main():
    # Vérifier que seulement un argument est fourni
    if len(sys.argv) != 2:
        raise AssertionError("more than one argument is provided" if len(sys.argv) > 2 else "No argument provided")
    
    # Vérifier que l'argument est un entier
    arg = sys.argv[1]
    if not arg.lstrip('-').isdigit():
        raise AssertionError("argument is not an integer")
    
    # Convertir l'argument en entier
    number = int(arg)
    
    # Vérifier si le nombre est pair ou impair
    if number % 2 == 0:
        print("I'm Even.")
    else:
        print("I'm Odd.")

if __name__ == "__main__":
    main()
