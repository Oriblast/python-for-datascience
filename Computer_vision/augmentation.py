from Augmentation import augment_one_file
from ls_file_in_dir import ls_of_file
import os
import sys
import cv2
import shutil
import matplotlib.pyplot as plt


def show_augmented(all_results: list, all_originals: list):

    num_images = len(all_originals)
    transform_names = list(all_results[0].keys())
    num_transforms = len(transform_names) + 1  # +1 pour "Original"

    # Taille dynamique
    fig, axes = plt.subplots(num_images + 1, num_transforms, figsize=(
        3.5 * num_transforms, 3.5 * (num_images + 1))
    )

    # Ligne 0 : titres bien visibles
    for col in range(num_transforms):
        title = "Original" if col == 0 else transform_names[col - 1]
        axes[0][col].text(
            0.5, 0.5, title, fontsize=14, ha='center', va='center'
        )
        axes[0][col].set_xticks([])
        axes[0][col].set_yticks([])
        axes[0][col].spines['top'].set_visible(False)
        axes[0][col].spines['right'].set_visible(False)
        axes[0][col].spines['bottom'].set_visible(False)
        axes[0][col].spines['left'].set_visible(False)

    # Lignes suivantes : images
    for row in range(num_images):
        axes[row + 1][0].imshow(cv2.cvtColor(
            all_originals[row], cv2.COLOR_BGR2RGB)
        )
        axes[row + 1][0].axis("off")
        for col, name in enumerate(transform_names):
            img = all_results[row][name]
            axes[row + 1][col + 1].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axes[row + 1][col + 1].axis("off")

    plt.tight_layout()
    plt.subplots_adjust(top=0.95)  # espace pour les titres
    plt.show()


def main():
    """
    programme principal permettant de faire l'augmentation """
    if len(sys.argv) < 2:
        return -1
    os.makedirs("augmented_directory", exist_ok=True)

    image = []
    imgs = []
    for z in sys.argv[1:]:
        root = z
        ig = cv2.imread(root)
        image.append(cv2.imread(root))
        if os.path.isfile(root):
            imgs.append(augment_one_file(ig))
            for i in range(len(imgs)):
                for j in imgs[i]:
                    cv2.imwrite(
                        f"augmented_directory/{root.split('/')[-1]}_{j}.jpg",
                        imgs[i][j]
                    )
    show_augmented(imgs, image)
    if os.path.isdir(sys.argv[1]):
        ls_dir = ls_of_file(root)
        root = sys.argv[1]
        max_nb_file = 0
        ad = "augmented_directory"
        for i in ls_dir:
            ad = "augmented_directory/" + i.split('/')[-1]
            if max_nb_file < len(ls_dir[i]):
                max_nb_file = len(ls_dir[i])
            shutil.copytree(os.path.join(root, i), ad, dirs_exist_ok=True)
        ls_dir = ls_of_file("augmented_directory")
        for path in ls_dir:
            if max_nb_file > len(ls_dir[path]):
                nb_transform = max_nb_file - len(ls_dir[path])
                if os.path.isdir(path):
                    for file in ls_dir[path]:
                        if nb_transform <= 0:
                            break
                        if os.path.isfile(file):
                            imgs = augment_one_file(cv2.imread(file))
                            for k in imgs:
                                if nb_transform <= 0:
                                    break
                                file_name = file.split('/')[-1] + f"_{k}.jpg"
                                cv2.imwrite(f"{path}/{file_name}", imgs[k])
                                nb_transform -= 1


if __name__ == "__main__":
    main()
