from Transformation import transform_one_file, load_image_rgb_safe
from ls_file_in_dir import ls_of_file
import os
import sys
import cv2
import shutil


def main():
    """
    programme principal permettant de faire l'augmentation """
    if len(sys.argv) < 2:
        return -1
    os.makedirs("Transformed_directory", exist_ok=True)
    root = sys.argv[1]
    image = load_image_rgb_safe(cv2.imread(root))

    if os.path.isfile(root):
        imgs = transform_one_file(image)
        for i in imgs:
            cv2.imshow(i, imgs[i])
            cv2.waitKey(5000)
            cv2.imwrite(f"Transformed_directory/{root.split('/')[-1]}_{i}.jpg", imgs[i])
    if os.path.isdir(root):
        ls_dir = ls_of_file(root)
        max_nb_file = 0
        ad = "Transformed_directory"
        for i in ls_dir:
            ad = "Transformed_directory/" + i.split('/')[-1]
            if max_nb_file < len(ls_dir[i]):
                max_nb_file = len(ls_dir[i])
            shutil.copytree(os.path.join(root, i), ad, dirs_exist_ok=True)
        ls_dir = ls_of_file("Transformed_directory")
        for path in ls_dir:
            if max_nb_file > len(ls_dir[path]):
                nb_transform = max_nb_file - len(ls_dir[path])
                if os.path.isdir(path):
                    for file in ls_dir[path]:
                        if nb_transform <= 0:
                            break
                        if os.path.isfile(file):
                            imgs = transform_one_file(cv2.imread(file))
                            for k in imgs:
                                if nb_transform <= 0:
                                    break
                                file_name = file.split('/')[-1] + f"_{k}.jpg"
                                cv2.imwrite(f"{path}/{file_name}", imgs[k])
                                nb_transform -= 1


if __name__ == "__main__":
    main()
