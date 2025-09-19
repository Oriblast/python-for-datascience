from re import L
import plantcv as pcv
import cv2
import numpy as np
from matplotlib import pyplot as plt
from typing import Tuple, Optional, List

class options:
    """les options de plantcv pcv
        debug, writeimg, resultat outdir
    """
    def __init__(self):
        self.debug = "plot"  
        self.writeimg= False
        self.result = "plantcv_results.json" 
        self.outdir = "."

pcv.params.debug = "plot"  # histoire d'avoir less images intermédiaires 

def ft_gaussien_blur(image: np.ndarray, ksize: Tuple[int, int] = (5, 5)) -> np.ndarray:
    """
    Applique un flou gaussien pour réduire le bruit et lisser l'image.
    Étape cruciale de prétraitement avant la segmentation.
    facilite la détection des contours et la segmentation.
    
    Args:
        image (np.ndarray): Image d'entrée
        ksize (Tuple[int, int]): Taille du noyau gaussien (doit être impair).
        
    Returns:
        np.ndarray: Image floutée.
    """

    if len(image.shape) == 3:
        img = pcv.rgb2gray_lab(image, channel='l')
    else:
        img = image

    blur_img = pcv.gaussien_blur(img=img, ksize=ksize)
    return blur_img

def leaf_mask(image: np.ndarray, blur_ksize: Tuple[int, int] = (5, 5)) -> np.ndarray:
    """
    Crée un masque binaire segmentant la feuille de l'arrière-plan.
    Cœur de l'analyse PlantCV - isole l'objet d'intérêt.
    
    Principe PlantCV : Utilise un seuillage dans l'espace colorimétrique LAB
    (canal bleu-jaune) qui est très efficace pour séparer le vert des plantes
    de la plupart des arrière-plans.
    
    Args:
        image (np.ndarray): Image couleur BGR.
        blur_ksize (Tuple[int, int]): Taille du noyau pour le pré-flou.
        
    Returns:
        np.ndarray: Masque binaire où la feuille est blanche (255) et le fond noir (0).
    """
    g_blur = ft_gaussien_blur(image, blur_ksize)

    a_channel = pcv.rgb2gray_lab(g_blur, channel='a')
    b_channel = pcv.rgb2gray_lab(g_blur, channel='b') #Le canal 'b' (bleu-jaune) est excellent pour segmenter le vert des plantes

    # Seuillage pour créer le masque
    # Ajuste ces valeurs en fonction de tes images !

    mask = pcv.threshold.binary(gray_img=b_channel,
                                threshold=125, 
                                max_value=255,
                                object_type="light")

    #on nettoie le mask pour se déparasser des petits artefacts
    clean_mask = pcv.fill(bin_img=mask, size=200)
    clean_mask = pcv.erode(clean_mask, ksize=3, iterations=1)
    clean_mask = pcv.dilate(clean_mask, ksize=3, iterations=1)

    return clean_mask

def roi_objects(image: np.ndarray, mask: np.ndarray) -> Tuple[np.ndarray, List]:
    """
        Identifie et extrait les Régions d'Intérêt (ROI) à partir du masque.
        
        Principe PlantCV : Utilise l'analyse des contours pour trouver tous les objets
        dans le masque et les hiérarchise pour identifier le contour principal (la feuille).
        
        Args:
            image (np.ndarray): Image originale.
            mask (np.ndarray): Masque binaire.
            
        Returns:
            Tuple[np.ndarray, List]: 
                - Image avec les ROI dessinées
                - Liste des objets identifiés
        """
    # Trouve les contours et hiérarchise les objets
    objets, hierarchy = pcv.find_objects(img=image, mask=mask)

    #cree le roi autour de la feuille
    roi_contour = pcv.roi.rectangle(img=image, x=0, y=0,
                                    w=image.shape[0],
                                    h=image.shape[1])
    filtered_object, filtered_hiérarchy, filtered_mask = pcv.roi.objets(
        img=image,
        roi_contour=roi_contour,
        roi_herarchy=[0],
        object_contour=objets,
        obj_hierarchy=hierarchy
    )
    #dessin des objets sur les images
    roi_img = pcv.analyse.objects(img=image, objects=filtered_object,
                                mask=filtered_mask)
    return roi_img, filtered_object


def analyze_objects(image: np.ndarray, mask: np.ndarray, objects: List) -> dict:
    """
    Analyse les objets détectés et extrait des caractéristiques morphologiques.
    
    Principe PlantCV : Mesure des propriétés géométriques comme l'aire, 
    le périmètre, la hauteur, la largeur, etc. de chaque objet.
    
    Args:
        image (np.ndarray): Image originale.
        mask (np.ndarray): Masque binaire.
        objects (List): Liste des objets à analyser.
        
    Returns:
        dict: Dictionnaire des caractéristiques morphologiques.
    """
    #mesure les traits de forme 
    analyze_img = image.copy()
    #analyse la forme 
    analyze_img = pcv.analyze.size(img=analyze_img, mask=mask,
                            labeled_mask=None)
    #mesure la couleurs dans divers zone
    analyze_img = pcv.analyse.color(img=analyze_img, mask=mask,
                            colorspaces="hsv")
    
    analyze_img = pcv.analyse.texture(img=analyze_img, mask=mask,
                        k=5, distance=1)
    return pcv.outputs.observations

def create_pseudolandmarks(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Génère des pseudorepères (landmarks) le long du contour de la feuille.
    
    Principe PlantCV : Place des points équidistants le long du contour
    principal pour capturer la forme globale de la feuille. Très utile
    pour comparer des formes.
    
    Args:
        image (np.ndarray): Image originale.
        mask (np.ndarray): Masque binaire.
        
    Returns:
        np.ndarray: Image avec les pseudorepères dessinés.
    """

    land_mask = image.copy()

    contours = pcv.find_objects(img=image, mask=mask)

    if len(contours) > 0:
        #prend el plus grand contours de la feuille
        main_contour = max(contours, key=lambda x: cv2.contourArea(x))
        # repere
        land_mask = pcv.landmarks.reference_pts(img=land_mask, 
            roi_contour=[main_contour], npts=30
            )
    return land_mask

def create_color_histogram(image: np.ndarray, mask: np.ndarray) -> plt.Figure:
    """
    Génère et affiche l'histogramme des couleurs de la feuille dans différents espaces colorimétriques.
    
    Principe PlantCV : Analyse la distribution des couleurs dans les zones de la feuille 
    à travers différents espaces colorimétriques (RGB, LAB, HSV). Chaque canal apporte 
    des informations différentes sur la santé de la feuille.
    
    Args:
        image (np.ndarray): Image originale au format BGR (OpenCV).
        mask (np.ndarray): Masque binaire où la feuille est blanche (255).
        
    Returns:
        plt.Figure: Figure matplotlib contenant les histogrammes.
    """
    # Crée une figure avec plusieurs subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Histogrammes des Couleurs de la Feuille', fontsize=16)
    
    # Applique le masque pour ne garder que les pixels de la feuille
    leaf_pixels = image[mask > 0]
    
    # -------------------------------------------------------------------------
    # 1. Histogramme RGB
    # -------------------------------------------------------------------------
    colors = ('blue', 'green', 'red')
    channels = cv2.split(image)  # B, G, R (OpenCV format)
    
    for i, (color, channel) in enumerate(zip(colors, channels)):
        # Prend seulement les pixels de la feuille
        channel_values = channel[mask > 0].flatten()
        axes[0, 0].hist(channel_values, bins=256, range=[0, 256], 
                       color=color, alpha=0.7, density=True)
    
    axes[0, 0].set_title('Espace RGB')
    axes[0, 0].set_xlabel('Intensité des Pixels (0-255)')
    axes[0, 0].set_ylabel('Proportion de Pixels')
    axes[0, 0].legend(['Blue', 'Green', 'Red'])
    axes[0, 0].grid(True, alpha=0.3)
    
    # -------------------------------------------------------------------------
    # 2. Histogramme HSV (Teinte, Saturation, Valeur)
    # -------------------------------------------------------------------------
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_channels = cv2.split(hsv_image)
    hsv_names = ['Hue (Teinte)', 'Saturation', 'Value (Valeur)']
    hsv_ranges = [(0, 180), (0, 256), (0, 256)]  # Hue va de 0-180 dans OpenCV
    
    for i, (channel, name, channel_range) in enumerate(zip(hsv_channels, hsv_names, hsv_ranges)):
        channel_values = channel[mask > 0].flatten()
        axes[0, 1].hist(channel_values, bins=50, range=channel_range, 
                       alpha=0.7, density=True, label=name)
    
    axes[0, 1].set_title('Espace HSV')
    axes[0, 1].set_xlabel('Intensité des Pixels')
    axes[0, 1].set_ylabel('Proportion de Pixels')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # -------------------------------------------------------------------------
    # 3. Histogramme LAB (Luminosité, Green-Magenta, Blue-Yellow)
    # -------------------------------------------------------------------------
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lab_channels = cv2.split(lab_image)
    lab_names = ['Lightness (L)', 'Green-Magenta (A)', 'Blue-Yellow (B)']
    
    # Les canaux A et B de LAB vont de 0-255 mais centrés autour de 128
    for i, (channel, name) in enumerate(zip(lab_channels, lab_names)):
        channel_values = channel[mask > 0].flatten()
        axes[1, 0].hist(channel_values, bins=50, range=[0, 256], 
                       alpha=0.7, density=True, label=name)
    
    axes[1, 0].set_title('Espace LAB')
    axes[1, 0].set_xlabel('Intensité des Pixels (0-255)')
    axes[1, 0].set_ylabel('Proportion de Pixels')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # -------------------------------------------------------------------------
    # 4. Histogramme des Teintes (Hue) uniquement - très utile pour les plantes
    # -------------------------------------------------------------------------
    hue_channel = hsv_channels[0]  # Canal H de HSV
    hue_values = hue_channel[mask > 0].flatten()
    
    # Le canal Hue va de 0-180 dans OpenCV (0-360° divisé par 2)
    axes[1, 1].hist(hue_values, bins=180, range=[0, 180], 
                   color='purple', alpha=0.7, density=True)
    
    axes[1, 1].set_title('Distribution des Teintes (Hue)')
    axes[1, 1].set_xlabel('Teinte (0-180 ≈ 0-360°)')
    axes[1, 1].set_ylabel('Proportion de Pixels')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Ajoute des labels de couleur pour l'axe des teintes
    hue_colors = ['Rouge', 'Jaune', 'Vert', 'Cyan', 'Bleu', 'Magenta', 'Rouge']
    hue_positions = [0, 30, 60, 90, 120, 150, 180]
    for pos, color in zip(hue_positions, hue_colors):
        axes[1, 1].axvline(x=pos, color='gray', linestyle='--', alpha=0.5)
        if pos < 180:
            axes[1, 1].text(pos + 15, axes[1, 1].get_ylim()[1] * 0.9, 
                           color, ha='center', fontsize=8)
    
    plt.tight_layout()
    return fig