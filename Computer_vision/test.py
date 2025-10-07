#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import matplotlib

import cv2
import shutil
from plantcv import plantcv as pcv

matplotlib.use("Agg")  # backend non interactif

# --- Transformation 1 : Original ---
def transform_original(img):
    return img


# --- Transformation 2 : Gaussian blur (canal 'a' Lab) + threshold intermédiaire ---
def transform_gaussian_blur(img):
    a = pcv.rgb2gray_lab(rgb_img=img, channel='a')
    a_blur = pcv.gaussian_blur(img=a, ksize=(5, 5), sigma_x=0, sigma_y=0)
    mask = pcv.threshold.binary(
        gray_img=a_blur,
        threshold=120,        # ajuste si nécessaire pour ton dataset
        max_value=255,
        object_type='dark'    # 'dark' si la feuille apparaît sombre sur le canal 'a'
    )
    mask = pcv.fill(bin_img=mask, size=200)
    return mask


def transform_mask(img):
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
    mask = pcv.threshold.binary(
        gray_img=s, threshold=40, max_value=255,
            object_type='light'
    )
    mask = pcv.fill(bin_img=mask, size=200)
    masked = pcv.apply_mask(img=img, mask=mask, mask_color='white')
    return masked, mask


def transform_roi_objects(img, mask):
    roi_contour, roi_hierarchy = pcv.roi.rectangle(
        img=img, x=0, y=0, h=img.shape[0], w=img.shape[1]
    )
    objects, hierarchy = pcv.find_objects(img, mask)
    roi_objects, hierarchy, kept_mask, obj_area = pcv.roi_objects(
        img=img,
        roi_contour=roi_contour,
        roi_hierarchy=roi_hierarchy,
        object_contour=objects,
        obj_hierarchy=hierarchy
    )

    # Construire un overlay vert (BGR) uniquement sur les zones retenues
    overlay = np.zeros_like(img)                # BGR
    overlay[kept_mask > 0] = (0, 255, 0)        # vert vif en BGR

    # Fusion : garder les couleurs naturelles, mettre le vert en avant
    roi_img = cv2.addWeighted(img, 1.0, overlay, 0.45, 0.0)
    return roi_img


# --- Transformation 5 : Analyze object ---
def transform_analyze_object(img, mask):
    objects, hierarchy = pcv.find_objects(img, mask)
    obj, mask_comb = pcv.object_composition(img, objects, hierarchy)
    analyze_img = pcv.analyze_object(img, obj, mask_comb)
    return analyze_img


def transform_pseudolandmarks(img, mask):
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output")

    objects, hierarchy = pcv.find_objects(img, mask)
    obj, mask_comb = pcv.object_composition(img, objects, hierarchy)

    pcv.params.debug = "print"
    pcv.params.debug_outdir = "output"
    
    _coords, top, bottom = pcv.y_axis_pseudolandmarks(
        img=img, obj=obj, mask=mask_comb
    )

    
    pcv.params.debug = None

    files = os.listdir("output")
    if len(files) != 1:
        raise RuntimeError(
            f"Expected 1 image in output/, found {len(files)}"
        )
    return cv2.imread(os.path.join("output", files[0]))


def transform_color_histogram(img, mask):
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output")

    pcv.params.debug = "print"
    pcv.params.debug_outdir = "output"

    pcv.analyze_color(rgb_img=img, mask=mask, colorspaces="all")

    pcv.params.debug = None

    files = os.listdir("output")
    if len(files) != 1:
        raise RuntimeError(f"Expected 1 image in output/, found {len(files)}")
    return cv2.imread(os.path.join("output", files[0]))



# --- Pipeline principal ---
def process_image_pipeline(image: np.ndarray) -> dict:
    """
    Applique une série de transformations d'analyse d'image 
    et retourne les résultats.

    Cette fonction est utile pour visualiser les étapes successives 
    du pipeline
    d'analyse d'image sans sauvegarder les fichiers.

    Args:
        image (np.ndarray): Image d'entrée au format OpenCV (BGR).

    Returns:
        dict: Dictionnaire contenant les images transformées 
        à chaque étape.
    """
    results = {}

    # 1. Original
    results['Original'] = transform_original(image)

    # 2. Gaussian Blur + masque binaire
    results['Gaussian Blur Mask'] = transform_gaussian_blur(image)

    # 3. Masque HSV + application
    masked, mask = transform_mask(image)
    results['Masked Image'] = masked
    results['Mask'] = mask

    # 4. ROI (extraction des objets d'intérêt)
    results['ROI'] = transform_roi_objects(image, mask)

    # 5. Analyse des objets
    results['Analyzed Object'] = transform_analyze_object(image, mask)

    results['pseudo'] = transform_pseudolandmarks(image, mask)

    results['histogram'] = transform_color_histogram(image, mask)

    return results



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test.py <image_path>")
        sys.exit(1)
    main(sys.argv[1])
