import albumentations as A
import cv2
import numpy as np
from typing import Tuple, Optional

def flip(img):
    """
    Applique un retournement horizontal aléatoire à l'image.
    
    Principe : Retourne l'image sur l'axe vertical (effet miroir). 
    Cette transformation préserve toutes les caractéristiques de la feuille
    tout en créant une nouvelle perspective.
    
    Args:
        image (np.ndarray): Image d'entrée au format BGR (OpenCV) ou RGB.
        
    Returns:
        np.ndarray: Image retournée horizontalement.
    """
    transform = A.HorizontalFlip(p=1.0)
    my_flip = transform(image=img)
    return my_flip["image"]

def rotate(image: np.ndarray, angle: Tuple[int, int] = (-45, 45)) -> np.ndarray:
    """
    Applique une rotation aléatoire dans une plage d'angles spécifiée.
    
    Principe : Effectue une rotation autour du centre de l'image. Les zones qui 
    sortent du cadre sont remplies avec des pixels réfléchis, préservant ainsi
    la taille originale de l'image.
    
    Args:
        image (np.ndarray): Image d'entrée.
        angle_range (Tuple[int, int]): Plage d'angles en degrés pour la rotation.
        
    Returns:
        np.ndarray: Image tournée.
    """
    transform = A.Rotate(limit=angle,
    border_mode=cv2.BORDER_REFLECT_101, p=1.0)

    return transform(image=image)['image']
    transform = A.Rotate(limit=angle, 
                        border_mode=cv2.BORDER_REFLECT_101, 
                        p=1.0)
    transformed = transform(image=image)
    return transformed['image']

def skew(image: np.ndarray, my_scale: Tuple[float, float] = (0.05, 0.1)) -> np.ndarray:
    """
    Applique une distortion de perspective (inclinaison) aléatoire.
    
    Principe : Simule une prise de vue sous un angle non perpendicularité.
    Transforme le rectangle de l'image en un trapèze, préservant les lignes
    droites mais modifiant les angles.
    
    Args:
        image (np.ndarray): Image d'entrée.
        scale : est le facteur de deformation de l'image il indique 
        a quel point l'img peut etre etiré ou tordu 
    Returns:
        np.ndarray: Image avec distortion perspective.
        C’est la façon de remplir les bords si la transformation crée des “trous” autour de l’image.

        cv2.BORDER_REFLET_101 est une méthode qui reflète les pixels du bord pour combler les zones vides.

        C’est comme si tu faisais un miroir des bords pour éviter d’avoir du noir ou du vide.

        p =  a la probailité de faire une transformation je laisse tj a 1
    """
    transform = A.Perspective(scale=my_scale,keep_size=True, 
    pad_mode=cv2.BORDER_REFLECT_101, p=1.0)
    return transform(image=image)["image"]
    transform = A.Perspective(scale=(0.05, 0.1), 
                             keep_size=True, 
                             pad_mode=cv2.BORDER_REFLECT_101,
                             p=1.0)
    transformed = transform(image=image)
    return transformed['image']

def shear(image: np.ndarray, my_shear: Tuple[float, float] = (-0.1, 0.1)) -> np.ndarray:
    """
    Applique un cisaillement (shear) aléatoire à l'image.
    
    Principe : Déplace les pixels horizontalement en fonction de leur position
    verticale (ou vice versa), créant un effet de "glissement" des couches.
    Contrairement à la perspective, les lignes parallèles restent parallèles.
    
    Args:
        image (np.ndarray): Image d'entrée.
        my_shear (Tuple[float, float]): Intensité du cisaillement sur les axes X et Y.
        
    Returns:
        np.ndarray: Image cisaillée.
    """
    transform = A.Affine(shear=my_shear, keep_ratio=True,
    mode=cv2.BORDER_REFLECT_101, p=1.0)
    return transform(image=image)["image"]

def crop(image: np.ndarray, my_scale: Tuple[float, float] = (0.8, 0.9)) -> np.ndarray:
    """
    Applique un recadrage aléatoire suivi d'un redimensionnement.
    
    Principe : Sélectionne une sous-région aléatoire de l'image, puis redimensionne
    cette région à la taille originale. Force le modèle à se concentrer sur des
    détails locaux plutôt que sur l'image entière.
    
    Args:
        image (np.ndarray): Image d'entrée.
        my_scale (Tuple[float, float]): Plage de pourcentage de la zone à recadrer.
        
    Returns:
        np.ndarray: Image recadrée et redimensionnée.
    """
    transform = A.RandomResizedCrop(
    size=(image.shape[0], image.shape[1]),
    scale=my_scale, ratio=(0.8, 1.2), p=1.0
    )
    return transform(image=image)["image"]
    transform = A.RandomResizedCrop(height=image.shape[0], 
                                   width=image.shape[1],
                                   scale=my_scale,
                                   ratio=(0.8, 1.2),
                                   p=1.0)
    transformed = transform(image=image)
    return transformed['image']

def distortion(image: np.ndarray, distortion_limit: float = 0.2) -> np.ndarray:
    """
    Applique une distortion de barillet (barrel) ou coussinet (pincushion).
    
    Principe : Simule les distortions d'objectif d'appareil photo. La distortion
    de barillet pousse les bords vers l'extérieur, tandis que la distortion
    en coussinet les tire vers l'intérieur. Les lignes droites deviennent courbes.
    
    Args:
        image (np.ndarray): Image d'entrée.
        distortion_limit (float): Intensité maximale de la distortion.
        
    Returns:
        np.ndarray: Image avec distortion optique.
    """
    transform = A.OpticalDistortion(distort_limit=distortion_limit, shift_limit=0,
    interpolation=cv2.INTER_CUBIC, border_mode=cv2.BORDER_REFLECT_101, p=1.0)
    return transform(image=image)["image"]
    transform = A.OpticalDistortion(distort_limit=distortion_limit,
                                   shift_limit=0,
                                   interpolation=cv2.INTER_CUBIC,
                                   border_mode=cv2.BORDER_REFLECT_101,
                                   p=1.0)
    transformed = transform(image=image)
    return transformed['image']
def blur(image: np.ndarray, blur_limit: Tuple[int, int] = (11, 13)) -> np.ndarray:
    """
    Applique un flou gaussien aléatoire à l'image.
    
    Principe : Réduit le bruit et les détails fins en mélangeant chaque pixel
    avec ses voisins selon une distribution gaussienne. Simule une mise au point
    floue ou une image basse résolution.
    
    Args:
        image (np.ndarray): Image d'entrée.
        blur_limit (Tuple[int, int]): Plage pour le noyau de flou (doit être impair).
        
    Returns:
        np.ndarray: Image floutée.
    """

    transform = A.Blur(blur_limit=blur_limit, p=1.0)
    return transform(image=image)["image"]

def contrast(image: np.ndarray, contrast_limit: Tuple[float, float] = (0.8, 1.2)) -> np.ndarray:
    """
    Ajuste le contraste de l'image de manière aléatoire.
    
    Principe : Modifie la différence entre les pixels clairs et sombres.
    Un contraste faible rend l'image plus grise, un contraste fort accentue
    les différences entre les zones claires et sombres.
    
    Args:
        image (np.ndarray): Image d'entrée.
        contrast_limit (Tuple[float, float]): Facteur de modification du contraste.
        
    Returns:
        np.ndarray: Image avec contraste modifié.
    """
    transform = A.RandomBrightnessContrast(brightness_limit=0,  # On ne change que le contraste
                                          contrast_limit=contrast_limit,
                                          p=1.0)
    transformed = transform(image=image)
    return transformed['image']

def augment_one_file(image: np.ndarray) -> dict:
    """
    Applique les 8 transformations d'augmentation à une image et retourne les résultats.
    
    Cette fonction sert principalement pour le mode démonstration où l'on veut
    visualiser l'effet de chaque transformation individuellement.
    
    Args:
        image (np.ndarray): Image d'entrée au format OpenCV (BGR).
        
    """
    results = {}
    
    
    
    
    shear(image, my_shear=(-0.5, 0.5))



    results['Flip'] = flip(image)
    #results['Rotate'] = rotate(image, angle=(-90, 90))
    results['Skew'] = skew(image, my_scale=(0.2, 0.4))
    results['Shear'] = shear(image, my_shear=(-25.0, 25.0))
    #results['Crop'] = crop(image, my_scale=(1.0, 1.0))
    results['Distortion'] = distortion(image, distortion_limit=25)
    results['Blur'] = blur(image)
    results['Contrast'] = contrast(image)
    
    return results
