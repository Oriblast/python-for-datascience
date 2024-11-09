import numpy as np
from PIL import Image
def ft_load(path: str) -> np.ndarray:
    """
    Charge une image, imprime son format et son contenu en pixels RGB.
    
    :param path: Chemin vers l'image.
    :return: Contenu de l'image sous forme de tableau numpy.
    """
    try:
        # Ouvrir l'image
        img = Image.open(path)
        
        # Vérifier le format de l'image
        if img.format not in ["JPEG", "JPG"]:
            raise ValueError("Format d'image non supporté. Seuls les formats JPG et JPEG sont supportés.")
        
        # Convertir l'image en RGB
        img = img.convert("RGB")
        
        # Convertir l'image en tableau numpy
        img_array = np.array(img)
        
        # Imprimer la forme de l'image
        print(f"The shape of image is: {img_array.shape}")
        
        return img_array
    
    except Exception as e:
        print(f"Erreur: {e}")
        return np.array([])  # Retourner un tableau vide en cas d'erreur