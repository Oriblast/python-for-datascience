import string
import sys


def count_characters(text: str) -> dict:
    """
    This function counts the number of upper-case letters, lower-case letters,
    punctuation marks, spaces, and digits in a given text.
    :param text: The text to analyze.
    :return: A dictionary with the counts of different character types.
    """

    counts = {
        "upper": 0,
        "lower": 0,
        "punctuation": 0,
        "spaces": 0,
        "digits": 0,
        "total": len(text)
    }
    for char in text:
        if char.isupper():
            counts["upper"] += 1
        elif char.islower():
            counts["lower"] += 1
        elif char in string.punctuation:
            counts["punctuation"] += 1
        elif char.isspace():
            counts["spaces"] += 1
        elif char.isdigit():
            counts["digits"] += 1
    return counts


def display_counts(counts: dict) -> None:
    """fonction display the counts of each characters"""
    print(f"The text contains {counts['total']} characters:")
    print(f"{counts['upper']} upper letters")
    print(f"{counts['lower']} lower letters")
    print(f"{counts['punctuation']} punctuation marks")
    print(f"{counts['spaces']} spaces")
    print(f"{counts['digits']} digits")


def main() -> None:
    """main fonction of the program. it hundles imput
chexk erreur in call fonction"""
    try:

        if len(sys.argv) == 1:
            text = input("what is the text to count?\n")
        elif len(sys.argv) > 2:
            raise AssertionError("more than one argument is provided")
        else:
            text = sys.argv[1]

        display_counts(count_characters(text))

    except AssertionError as e:
        print(f"AssertionError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
