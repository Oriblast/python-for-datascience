import numpy as np


def give_bmi(
    height: list[int | float],
    weight: list[int | float]
) -> list[float]:
    """
    Calculate the BMI values from the height and weight lists.
    The BMI is defined as: weight (kg) / (height (cm)^2).
    #np.divide two paramettre first is the nunbber divide the
    """
    if len(height) != len(weight):
        raise ValueError("Height and weight lists must have the same length.")
    if not all(isinstance(h, (int, float)) for h in height):
        raise TypeError("All elements in the height list must be int/float")
    if not all(isinstance(w, (int, float)) for w in weight):
        raise TypeError("All elements in the weight list must be int/float.")
    bmi = np.divide(weight, np.power(height, 2))
    return bmi.tolist()


def apply_limit(bmi: list[float], limit: int) -> list[bool]:
    """
    Apply a limit to the BMI values and return a list of booleans indicating
    if the BMI is above the limit.

    :param bmi: List of BMI values.
    :param limit: BMI limit to compare against.
    :return: List of booleans.
    """
    if not all(isinstance(b, (int, float)) for b in bmi):
        raise TypeError("All elements in the BMI list must be int or float.")
    if not isinstance(limit, int):
        raise TypeError("The limit must be an integer.")
    return [b > limit for b in bmi]
