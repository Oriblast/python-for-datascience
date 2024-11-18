import sys


def morse_conversion(text: str) -> None:
    """
    Convert normal language into Morse code.
    """
    MORSE = {
        "A": ".- ", "B": "-... ", "C": "-.-. ", "D": "-.. ", "E": ". ",
        "F": "..-. ", "G": "--. ", "H": ".... ", "I": ".. ", "J": ".--- ",
        "K": "-.- ", "L": ".-.. ", "M": "-- ", "N": "-. ", "O": "--- ",
        "P": ".--. ", "Q": "--.- ", "R": ".-. ", "S": "... ", "T": "- ",
        "U": "..- ", "V": "...- ", "W": ".-- ", "X": "-..- ", "Y": "-.-- ",
        "Z": "--.. ", "0": "----- ", "1": ".---- ", "2": "..--- ",
        "3": "...-- ", "4": "....- ", "5": "..... ", "6": "-.... ",
        "7": "--... ", "8": "---.. ", "9": "----. ", " ": "/ "
    }

    morse_code = ""
    for char in text:
        char = char.upper()
        if char in MORSE:
            morse_code += MORSE[char]
        else:
            raise AssertionError("The arguments are bad")
    morse_code = morse_code.rstrip()
    print(morse_code.rstrip(), end="\n")


def main() -> None:
    """function principal"""

    try:
        if len(sys.argv) != 2:
            raise AssertionError("the argument are bad")
        text = sys.argv[1]
        if not isinstance(text, str):
            raise AssertionError("the arguments are bad")
        morse_conversion(text)
    except AssertionError as e:
        print(f"AssertionError: {e}\n")


if __name__ == "__main__":
    main()
