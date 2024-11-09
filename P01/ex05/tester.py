from load_image import ft_load
from pimp_image import ft_invert, ft_red, ft_green, ft_blue, ft_grey, display_image

if __name__ == "__main__":
    # Charger l'image
    img_array = ft_load("landscape.jpg")

    # Appliquer les différents filtres et afficher les images
    inverted_img = ft_invert(img_array)
    display_image(inverted_img, title="Inverted Image")
    
    red_img = ft_red(img_array)
    display_image(red_img, title="Red Filter")

    green_img = ft_green(img_array)
    display_image(green_img, title="Green Filter")

    blue_img = ft_blue(img_array)
    display_image(blue_img, title="Blue Filter")

    grey_img = ft_grey(img_array)
    display_image(grey_img, title="Greyscale Image")
