#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import argparse
import json
import os
import sys
import zipfile

import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train plant disease classifier with CropNet."
    )
    parser.add_argument(
        "-src", "--source", required=True,
        help="Root dataset dir with subfolders per class."
    )
    parser.add_argument(
        "-dst", "--dest", required=True,
        help="Output dir for artifacts."
    )
    parser.add_argument(
        "--epochs", type=int, default=10,
        help="Number of training epochs."
    )
    parser.add_argument(
        "--batch", type=int, default=32,
        help="Batch size."
    )
    parser.add_argument(
        "--imgsize", type=int, default=224,
        help="Square image size."
    )
    parser.add_argument(
        "--save-aug", action="store_true",
        help="Save a few augmented samples per image."
    )
    parser.add_argument(
        "--aug-per-file", type=int, default=8,
        help="Number of augmented copies per original (if --save-aug)."
    )
    return parser.parse_args()


def build_datagens(img_size, batch_size, src):
    datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        validation_split=0.2,
        rotation_range=20,
        width_shift_range=0.10,
        height_shift_range=0.10,
        shear_range=0.20,
        zoom_range=0.20,
        horizontal_flip=True,
        fill_mode="nearest",
    )
    train_gen = datagen.flow_from_directory(
        src,
        target_size=img_size,
        batch_size=batch_size,
        subset="training",
        class_mode="categorical",
        shuffle=True,
    )
    val_gen = datagen.flow_from_directory(
        src,
        target_size=img_size,
        batch_size=batch_size,
        subset="validation",
        class_mode="categorical",
        shuffle=False,
    )
    return train_gen, val_gen

def build_model(num_classes, img_size):
    inputs = tf.keras.Input(shape=img_size + (3,))
    
    # Charger le feature extractor (pas le classifier figé)
    base_layer = hub.KerasLayer(
        "https://tfhub.dev/google/cropnet/feature_vector/cassava_disease_V1/1",
        trainable=True
    )
    
    x = base_layer(inputs)  # on applique le Hub layer sur l'Input
    outputs = layers.Dense(num_classes, activation="softmax")(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model

def save_label_map(gen, dst):
    labels_path = os.path.join(dst, "labels.json")
    with open(labels_path, "w", encoding="utf-8") as f:
        json.dump(gen.class_indices, f, indent=2, ensure_ascii=False)


def save_some_augmented(src, dst_aug_root, img_size, per_file):
    os.makedirs(dst_aug_root, exist_ok=True)
    aug_gen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=20,
        width_shift_range=0.10,
        height_shift_range=0.10,
        shear_range=0.20,
        zoom_range=0.20,
        horizontal_flip=True,
        fill_mode="nearest",
    )
    for class_name in sorted(os.listdir(src)):
        class_dir = os.path.join(src, class_name)
        if not os.path.isdir(class_dir):
            continue
        out_class = os.path.join(dst_aug_root, class_name)
        os.makedirs(out_class, exist_ok=True)
        for fname in sorted(os.listdir(class_dir)):
            path = os.path.join(class_dir, fname)
            if not os.path.isfile(path):
                continue
            img = tf.keras.utils.load_img(path, target_size=img_size)
            x = tf.keras.utils.img_to_array(img)
            x = x.reshape((1,) + x.shape)
            count = 0
            for batch in aug_gen.flow(x, batch_size=1):
                out = (batch[0] * 255.0).astype("uint8")
                out_img = tf.keras.utils.array_to_img(out)
                out_name = f"{os.path.splitext(fname)[0]}_aug{count}.jpg"
                out_img.save(os.path.join(out_class, out_name))
                count += 1
                if count >= per_file:
                    break


def zip_artifacts(dst):
    zip_path = os.path.join(dst, "train_artifacts.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(dst):
            for f in files:
                if f.endswith(".zip"):
                    continue
                full = os.path.join(root, f)
                rel = os.path.relpath(full, dst)
                zf.write(full, arcname=rel)


def main():
    args = parse_args()
    img_size = (args.imgsize, args.imgsize)

    if not os.path.isdir(args.source):
        print("Error: --source must be a directory.", file=sys.stderr)
        sys.exit(2)

    os.makedirs(args.dest, exist_ok=True)

    train_gen, val_gen = build_datagens(img_size, args.batch, args.source)
    model = build_model(train_gen.num_classes, img_size)

    save_label_map(train_gen, args.dest)

    ckpt = tf.keras.callbacks.ModelCheckpoint(
        os.path.join(args.dest, "model_best.keras"),
        monitor="val_accuracy",
        save_best_only=True,
        save_weights_only=False,
    )
    early = tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy", patience=3, restore_best_weights=True
    )

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=args.epochs,
        callbacks=[ckpt, early],
    )
    
    ckpt = tf.keras.callbacks.ModelCheckpoint(
    os.path.join(args.dest, "model_best.weights.h5"),
    monitor="val_accuracy",
    save_best_only=True,
    save_weights_only=True,
    )

    model.save_weights(os.path.join(args.dest, "model_final.weights.h5"))
    model.save(os.path.join(args.dest, "model_final.keras"), save_format="keras")

    print("Val accuracy history:", history.history.get("val_accuracy", []))
    print("Best val acc:", max(history.history.get("val_accuracy", [0.0])))

    if args.save_aug:
        aug_dir = os.path.join(args.dest, "augmented")
        save_some_augmented(args.source, aug_dir, img_size, args.aug_per_file)

    zip_artifacts(args.dest)
    print(f"✅ Artifacts zipped in: {os.path.join(args.dest, 'train_artifacts.zip')}")


if __name__ == "__main__":
    main()
