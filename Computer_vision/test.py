#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")  # backend non interactif
import matplotlib.pyplot as plt
import cv2
from plantcv import plantcv as pcv


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


# --- Transformation 3 : Mask (HSV, vert) ---
def transform_mask(img):
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
    mask = pcv.threshold.binary(gray_img=s, threshold=40, max_value=255, object_type='light')
    mask = pcv.fill(bin_img=mask, size=200)
    masked = pcv.apply_mask(img=img, mask=mask, mask_color='white')
    return masked, mask


# --- Transformation 4 : ROI avec vert lumineux sur zones retenues et couleurs naturelles ailleurs ---
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


# --- Transformation 6 : Pseudolandmarks ---
def transform_pseudolandmarks(img, mask):
    objects, hierarchy = pcv.find_objects(img, mask)
    obj, mask_comb = pcv.object_composition(img, objects, hierarchy)
    pcv.params.debug = "print"
    pcv.params.debug_outdir = "output"
    _coords, top, bottom = pcv.y_axis_pseudolandmarks(
        img=img,
        obj=obj,
        mask=mask_comb
    )
    pcv.params.debug = None
    return img  # les visuels sont sauvegardés automatiquement par PlantCV


# --- Transformation 7 : Color histogram ---
def transform_color_histogram(img, mask):
    pcv.params.debug = "print"
    pcv.params.debug_outdir = "output"
    pcv.analyze_color(
        rgb_img=img,
        mask=mask,
        colorspaces="all"
    )
    pcv.params.debug = None


# --- Pipeline principal ---
def main(image_path):
    if not os.path.exists("output"):
        os.makedirs("output")

    img, path, filename = pcv.readimage(image_path)

    # 1. Original
    pcv.print_image(transform_original(img), "output/1_original.png")

    # 2. Gaussian Blur + threshold intermédiaire (masque binaire)
    blur_mask = transform_gaussian_blur(img)
    pcv.print_image(blur_mask, "output/2_gaussian_blur_mask.png")

    # 3. Mask HSV + application
    masked, mask = transform_mask(img)
    pcv.print_image(masked, "output/3_mask.png")

    # 4. ROI (vert lumineux, pas de violet)
    roi_img = transform_roi_objects(img, mask)
    pcv.print_image(roi_img, "output/4_roi.png")

    # 5. Analyze Object
    analyze_img = transform_analyze_object(img, mask)
    pcv.print_image(analyze_img, "output/5_analyze.png")

    # 6. Pseudolandmarks (sauvegardés automatiquement)
    transform_pseudolandmarks(img, mask)

    # 7. Color histogram (sauvegardés automatiquement)
    transform_color_histogram(img, mask)

    print("✅ Toutes les images ont été générées dans le dossier 'output/'")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test.py <image_path>")
        sys.exit(1)
    main(sys.argv[1])
