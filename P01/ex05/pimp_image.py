import numpy as np
import matplotlib.pyplot as plt


def ft_invert(array: np.ndarray) -> np.ndarray:
    """
    Inverts the colors of the image by subtracting each pixel value from 255.
    
    :param array: NumPy array representing the image.
    :return: The image with inverted colors.
    """
    return 255 - array


def ft_red(array: np.ndarray) -> np.ndarray:
    """
    Applies a red filter to the image by zeroing out the green and blue channels.
    
    :param array: NumPy array representing the image.
    :return: The image with the red filter applied.
    """
    red_array = array.copy()
    red_array[:, :, 1] = 0  # Mettre le canal vert à zéro
    red_array[:, :, 2] = 0  # Mettre le canal bleu à zéro
    return red_array


def ft_green(array: np.ndarray) -> np.ndarray:
    """
    Applies a green filter to the image by zeroing out the red and blue channels.
    
    :param array: NumPy array representing the image.
    :return: The image with the green filter applied.
    """
    green_array = array.copy()
    green_array[:, :, 0] = 0  # Mettre le canal rouge à zéro
    green_array[:, :, 2] = 0  # Mettre le canal bleu à zéro
    return green_array


def ft_blue(array: np.ndarray) -> np.ndarray:
    """
    Applies a blue filter to the image by zeroing out the red and green channels.
    
    :param array: NumPy array representing the image.
    :return: The image with the blue filter applied.
    """
    blue_array = array.copy()
    blue_array[:, :, 0] = 0  # Mettre le canal rouge à zéro
    blue_array[:, :, 1] = 0  # Mettre le canal vert à zéro
    return blue_array


def ft_grey(array) -> np.ndarray:
    """
    Applique un filtre gris à l'image.

    :param array: Tableau numpy représentant l'image.
    :return: Image en niveaux de gris.
    """
    grey_array = array.copy()
    grey = grey_array[:, :, 0] * 0.2989 + grey_array[:, :, 1] * 0.587 + grey_array[:, :, 2] * 0.114
    grey_array[:, :, 0] = grey
    grey_array[:, :, 1] = grey
    grey_array[:, :, 2] = grey
    return grey_array


def display_image(array: np.ndarray, title: str = "Image"):
    """
    Displays an image using matplotlib.
    
    :param array: NumPy array representing the image.
    :param title: Title of the image display window.
    """
    plt.imshow(array)
    plt.title(title)
    plt.axis('off')  # Désactiver les axes
    plt.show()

