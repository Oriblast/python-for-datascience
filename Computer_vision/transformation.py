from test import process_image_pipeline
from ls_file_in_dir import ls_of_file
import os
import sys
import cv2
import shutil
import matplotlib.pyplot as plt
import argparse
import cv2


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
    return parser.parse_args()


def main():
    """
    programme principal permettant de faire l'augmentation """

    arg = parse_args()
    if arg.dest == arg.source and (os.path.isdir(arg.source) and os.path.isdir(arg.dest)):
        print("verifier bien la source et la destination")
    if os.path.isdir(arg.dest):
        shutil.rmtree(arg.dest)
    os.makedirs(arg.dest, exist_ok=True)
    image = []
    imgs = []
    root = arg.source

    if os.path.isfile(arg.source):
        ig = cv2.imread(root)
        if os.path.isfile(root):
            imgs = process_image_pipeline(ig)
            for i in imgs:
                    cv2.imwrite(
                        f"{arg.dest}/{root.split('/')[-1]}_{i}.jpg",
                        imgs[i]
                    )
                    cv2.imshow(i, imgs[i])

                    cv2.waitKey(10000)
                    cv2.destroyAllWindows()
    if os.path.isdir(root):
        ls_dir = ls_of_file(root)
        max_nb_file = 0
        ad = arg.dest

        for i in ls_dir:
            if os.path.isdir(i):
                ad = f"{arg.dest}/" + i.split('/')[-1]
                print(i)
                print(os.path.join(root, i))
                shutil.copytree(os.path.join(root, i), ad, dirs_exist_ok=True)
                #dernier_dossier = os.path.basename(os.path.normpath(i))
                #os.makedirs(ad, exist_ok=True)
            elif os.path.isfile(i):
                ad = f"{arg.dest}/" + i.split('/')[-1]
                shutil.copy2(i, ad)
        ls_dir = ls_of_file(arg.dest)

        for path in ls_dir:
            if os.path.isdir(path):
                for file in ls_dir[path]:
                    if os.path.isfile(file):
                        imgs = process_image_pipeline(cv2.imread(file))
                        os.remove(file)
                        for k in imgs:
                            file_name = file.split('/')[-1] + f"_{k}.jpg"
                            cv2.imwrite(f"{path}/{file_name}", imgs[k])
            else:
                
                if os.path.isfile(path):
                    imgs = process_image_pipeline(cv2.imread(path))
                    os.remove(path)
                    for k in imgs:
                        file_name = path.split('/')[-1] + f"_{k}.jpg"
                        cv2.imwrite(f"{arg.dest}/{file_name}", imgs[k])

    print("strar gang")

if __name__ == "__main__":
    main()
