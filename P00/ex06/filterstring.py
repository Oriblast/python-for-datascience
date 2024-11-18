import sys
from ft_filter import ft_filter


def main():
    """Main function that processes the input and
returns the list of words with length greater than N."""
    # Vérifier qu'il y a exactement deux arguments
    if len(sys.argv) != 3:
        raise AssertionError("the arguments are bad")

    # Récupérer les arguments
    S = sys.argv[1]
    if not isinstance(S, str):
        raise AssertionError("the arguments are bad")
    try:
        N = int(sys.argv[2])
    except ValueError:
        raise AssertionError("the arguments are bad")
    # Séparer les mots de la chaîne S
    words = S.split()

    # lambda pour filtrer les mots de longueur supérieure à N
    filtered_words = list(ft_filter(lambda word: len(word) > N, words))

    # Afficher le résultat
    print(filtered_words)


if __name__ == "__main__":
    main()
