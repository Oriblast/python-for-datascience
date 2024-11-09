import matplotlib.pyplot as plt
from load_image import ft_load
import numpy as np


def transpose_image(image_array: np.ndarray) -> np.ndarray:
    """
    Manually transpose a 2D or 3D NumPy array (without using built-in transpose).
    
    :param image_array: NumPy array representing the image.
    :return: The transposed array.
    """
    # Initialiser une liste vide pour le transposé
    transposed = []
    # Boucle pour transposer chaque canal de couleur
    for i in range(image_array.shape[1]):  # Transposer les lignes en colonnes
        new_row = []
        for j in range(image_array.shape[0]):
            new_row.append(image_array[j][i])
        transposed.append(new_row)
    
    return np.array(transposed)


def crop_square(image_array: np.ndarray, size: int = 400) -> np.ndarray:
    """
    Crop a square portion from the center of the image.
    
    :param image_array: NumPy array representing the image.
    :param size: The size of the square to be cropped.
    :return: The cropped square as a NumPy array.
    """
    height, width, _ = image_array.shape
    
    # Calculer les coordonnées du carré central
    start_x = width // 2 - size // 6
    start_y = size // 4
    
    # Découper la portion carrée de l'image
    cropped_image = image_array[start_y:start_y + size, start_x:start_x + size]
    
    print(f"New shape after cropping: {cropped_image.shape}")
    
    return cropped_image


def display_image(image_array: np.ndarray, title: str = "Image"):
    """
    Display an image using matplotlib with axes labels.
    
    :param image_array: NumPy array representing the image.
    :param title: Title of the image display window.
    """
    plt.imshow(image_array)
    plt.title(title)
    plt.xlabel("X axis (pixels)")
    plt.ylabel("Y axis (pixels)")
    plt.show()


if __name__ == "__main__":
    try:
        # Charger l'image
        img_array = ft_load("animal.jpeg")
        
        # Découper une portion carrée de l'image
        cropped_img = crop_square(img_array, 400)
        
        # Afficher les données des pixels de l'image coupée (troncation pour clarté)
        print(cropped_img)
        
        # Transposer manuellement l'image coupée
        transposed_img = transpose_image(cropped_img)
        
        # Afficher les données des pixels après la transposition
        print(f"New shape after Transpose: {transposed_img.shape}")
        print(transposed_img)
        
        # Afficher l'image transposée
        display_image(transposed_img, title="Transposed Image")
    
    except Exception as e:
        print(f"An error occurred: {e}")
