from PIL import Image
import cv2
import os

# img = Image.open('perro.jpg')


def augment_image(image_path, output_folder):
    # Cargar la imagen original
    image = cv2.imread(image_path)

    # Rotar la imagen en diferentes ángulos
    for angle in [0, 30, 60, 90]:
        rotated = cv2.rotate(image, angle)
        cv2.imwrite(os.path.join(output_folder,
                    f"rotated_{angle}.jpg"), rotated)

    # Redimensionar la imagen a diferentes tamaños
    for scale in [0.5, 0.8, 1.2, 1.5]:
        resized = cv2.resize(
            image, (int(image.shape[1]*scale), int(image.shape[0]*scale)))
        cv2.imwrite(os.path.join(output_folder,
                    f"resized_{scale}.jpg"), resized)


augment_image("love.jpg", "fotos")
