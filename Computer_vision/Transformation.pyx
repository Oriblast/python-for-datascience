from re import L
from plantcv import plantcv as pcv
import cv2
import os
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

#pcv.set_param("debug", "print")
 # histoire d'avoir less images intermédiaires 
def load_image_rgb_safe(image) -> np.ndarray:

    if image is None:
        raise ValueError(f"⚠️ Image introuvable ou corrompue")

    if len(image.shape) == 2:
        # Image en niveaux de gris → convertir en RGB artificiel
        print(f"ℹ️ Image en niveaux de gris détectée, conversion forcée en RGB")
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    elif image.shape[2] == 4:
        # Image avec canal alpha → retirer alpha
        print(f"ℹ️ Image avec transparence détectée, suppression du canal alpha ")
        image = image[:, :, :3]

    elif image.shape[2] != 3:
        raise ValueError(f"❌ Nombre de canaux inattendu ({image.shape[2]}) dans l'image")

    # Convertir BGR → RGB pour compatibilité PlantCV
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb

def ft_gaussien_blur(image: np.ndarray, ksize: Tuple[int, int] = (555, 555)) -> np.ndarray:
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

    blur_img = pcv.gaussian_blur(img=img, ksize=ksize)
    return blur_img

def leaf_mask(image: np.ndarray) -> np.ndarray:
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
    a_channel = pcv.rgb2gray_lab(rgb_img=image, channel='a')
    bin_mask = pcv.threshold.binary(gray_img=a_channel, threshold=100, object_type='light')
    
    # Nettoyage du masque
    cleaned_mask = pcv.fill(bin_img=bin_mask, size=200)
    cleaned_mask = pcv.erode(gray_img=cleaned_mask, ksize=3, i=1)
    cleaned_mask = pcv.dilate(gray_img=cleaned_mask, ksize=3, i=1)
    
    return cleaned_mask

def roi_objects(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
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
    height, width = image.shape[:2]
    roi = pcv.roi.rectangle(img=image, x=width//4, y=height//4, 
                           w=width//2, h=height//2)
    
    # Filtrage du masque avec la ROI
    filtered_mask = pcv.roi.filter(mask=mask, roi=roi, roi_type='partial')
    
    return filtered_mask


def analyze_objects(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
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
    # Analyse de la taille et de la forme
    analysis_img = pcv.analyze.size(img=image, labeled_mask=mask, n_labels=1)
    return analysis_img

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

    landmarks_img = image.copy()
    
    # Utilise OpenCV directement pour trouver les contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        # Prend le plus grand contour (la feuille)
        main_contour = max(contours, key=cv2.contourArea)
        
        # Convertit le contour au format attendu par PlantCV
        contour_points = main_contour.reshape(-1, 2)
        
        # Génère les pseudorepères (vérifie si cette fonction existe toujours)
        try:
            landmarks_img = pcv.landmarks.reference_pts(img=landmarks_img, 
                                                      roi_contour=[contour_points],
                                                      npts=12)
        except AttributeError:
            # Fallback si landmarks.reference_pts n'existe pas
            print("⚠️  pcv.landmarks.reference_pts non disponible, utilisation d'OpenCV")
            # Dessine les points manuellement
            for i in range(12):
                angle = 2 * np.pi * i / 12
                radius = min(image.shape[0], image.shape[1]) // 3
                center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
                x = int(center_x + radius * np.cos(angle))
                y = int(center_y + radius * np.sin(angle))
                cv2.circle(landmarks_img, (x, y), 5, (0, 255, 0), -1)
    
    return landmarks_img
    
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

def transform_one_file(img) -> dict:
    """
    Exécute le pipeline complet de transformation PlantCV sur une image.
    
    Args:
        image_path (str): Chemin vers l'image à analyser.
        output_dir (str): Dossier de sortie pour les résultats.
        
    Returns:
        dict: Tous les résultats d'analyse et images transformées.
    """
    
    # Redimensionne si nécessaire pour la démo
    
    results = {}
    
    # 1. Flou Gaussien (prétraitement)
    gray_img = pcv.rgb2gray_lab(rgb_img=img, channel='l')
    results['Gaussian_Blur'] = pcv.gaussian_blur(img=gray_img, ksize=(5, 5))
    
    # 2. Création du masque
    results['Mask'] = leaf_mask(img)
    
    # 3. ROI et filtrage (CORRIGÉ - plus de roi_objects)
    results['Filtered_Mask'] = roi_objects(img, results['Mask'])
    
    # 4. Analyse morphologique (CORRIGÉ)
    results['Analysis_Image'] = analyze_objects(img, results['Filtered_Mask'])
    
    # 5. Pseudorepères
    results['Landmarks'] = create_pseudolandmarks(img, results['Filtered_Mask'])
    
    # 6. Histogramme des couleurs (TA VERSION CORRECTE)
    color_hist_fig = create_color_histogram(img, results['Mask'])
    hist_path = os.path.join(".", "color_histogram.png")
    color_hist_fig.savefig(hist_path, dpi=150, bbox_inches='tight')
    plt.close(color_hist_fig)  # Libère la mémoire
    results['Color_Histogram'] = hist_path
    pcv.outputs.save_results(filename=os.path.join(".", "results.json"))
    return results