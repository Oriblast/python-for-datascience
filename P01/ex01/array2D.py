import numpy as np


def slice_me(family: list, start: int, end: int) -> list:
    """
    Slice a 2D array (list of lists) and return the truncated version.
    
    :param family: 2D list to slice.
    :param start: Starting index for slicing.
    :param end: Ending index for slicing.
    :return: Sliced 2D list.
    """

    if not isinstance(family, list) or not all(isinstance(row, list) for row in family):
        raise TypeError("Input should be a list of lists.")
    
    row_length = len(family[0])
    if not all(len(row) == row_length for row in family):
        raise ValueError("All rows must have the same size.")
    
    # Vérifier si start et end sont des entiers
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("Start and end must be integers.")
    

    array = np.array(family)
    
    print(f"My shape is : {array.shape}")
    
    # Trancher l'array
    sliced_array = array[start:end]
    
    # Afficher la nouvelle forme après tranchage
    print(f"My new shape is : {sliced_array.shape}")
    
    return sliced_array.tolist()
