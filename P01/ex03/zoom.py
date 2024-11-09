from load_image import ft_load
import numpy as np
import matplotlib.pyplot as plt

def zoom_image(img_array: np.ndarray, start_x: int, start_y: int, zoom_width: int, zoom_height: int) -> np.ndarray:
    """
    Retourne une zone zoomée de l'image.
    
    :param img_array: Tableau numpy de l'image.
    :param start_x: Coordonnée de début en x.
    :param start_y: Coordonnée de début en y.
    :param zoom_width: Largeur de la zone de zoom.
    :param zoom_height: Hauteur de la zone de zoom.
    :return: Zone zoomée de l'image.
    """
    try:
        zoomed_img = img_array[start_y:start_y + zoom_height, start_x:start_x + zoom_width]
        print(f"New shape after slicing: {zoomed_img.shape}")
        return zoomed_img
    
    except Exception as e:
        print(f"Erreur lors du zoom: {e}")
        return np.array([])  # Retourner un tableau vide en cas d'erreur

# Charger l'image
img_array = ft_load("animal.jpeg")

if img_array.size > 0:
    # Effectuer le zoom
    zoomed_img = zoom_image(img_array, 100, 100, 400, 400)
    
    if zoomed_img.size > 0:
        # Afficher l'image zoomée
        plt.imshow(zoomed_img)
        plt.title("Zoomed Image")
        plt.xlabel("X axis")
        plt.ylabel("Y axis")
        plt.show()
