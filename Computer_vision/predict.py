#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
os.environ["TF_USE_LEGACY_KERAS"] = "1"  # force tf.keras legacy
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import tensorflow_hub as hub
from rembg import remove
from PIL import Image
#from keras.utils import get_custom_objects

#get_custom_objects()['KerasLayer'] = hub.KerasLayer

# === Paramètres fixes ===
MODEL_PATH = "training/model_final.keras"       modèle entraîné
LABELS_PATH = "training/labels.json"   # mapping classes
IMG_SIZE = 224                # taille d'entrée du modèle

def extract_zip(zip_path, output_dir):
    """
    Extrait le contenu d'un fichier ZIP dans un dossier spécifié.
    """
    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    print(f"✅ Extraction terminée : {zip_path} -> {output_dir}")

def load_labels(labels_path):
    with open(labels_path, "r", encoding="utf-8") as f:
        class_indices = json.load(f)
    return {v: k for k, v in class_indices.items()}  # index -> nom classe

def preprocess_image(img_path, img_size):
    img = tf.keras.utils.load_img(img_path, target_size=(img_size, img_size))
    
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0) / 255.0
    return img, x

def main():
    if len(sys.argv) < 2:
        print("Usage: ./predict.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    # Charger modèle et labels je n'ai rien defini au cas ou mais c'est pas grave 
    model = tf.keras.models.load_model(MODEL_PATH,
        custom_objects={'KerasLayer': hub.KerasLayer},
        compile=False
    )
    labels = load_labels(LABELS_PATH)

    # Préparer image
    orig_img, x = preprocess_image(image_path, IMG_SIZE)

    # Prédiction
    preds = model.predict(x)
    pred_idx = np.argmax(preds[0])
    pred_class = labels[pred_idx]
    confidence = preds[0][pred_idx]

    # Affichage images
    
    input_img = Image.open(image_path).convert("RGB")
    no_bg_img = remove(input_img) 
    
    resized = no_bg_img.resize((IMG_SIZE, IMG_SIZE))
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    fig.patch.set_facecolor('black')

    img_trans = Image.new("RGB", resized.size, (255, 255, 255)) #je cree une image blanche 

    img_trans.paste(resized, mask=resized.split()[3]) #j'y colle mon image transparent

    axes[0].imshow(orig_img)
    axes[0].axis("off")

    axes[1].imshow(img_trans)  # image transformée (224x224 normalisée)
    axes[1].axis("off")
    
    fig.text(0.5, 0.12, "=== DL Classification ===", ha='center',
    fontsize=16, fontweight='bold', color='white'
    )
    fig.text(0.5, 0.05, f"Class predicted: {pred_class}",
    ha='center', fontsize=12, color='white')
    #plt.suptitle(f"Prediction: {pred_class} ({confidence:.2%})")
    plt.subplots_adjust(bottom=0.2)
    plt.savefig("prediction.png")
    plt.show()

    print(f"✅ Prediction: {pred_class} (confidence {confidence:.2%})")

if __name__ == "__main__":
    main()
