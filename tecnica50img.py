from PIL import Image
import cv2
import random
import numpy as np


def augment_image(image):
    augmented_images = []

    flip_applied = False

    for i in range(2):
        # Rotación
        angle = random.randint(-45, 45)
        rotated_image = image.rotate(angle)

        # Cambio de tamaño
        scale = random.uniform(0.5, 2)
        width, height = image.size
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_image = image.resize((new_width, new_height))

        # Cambio de iluminación
        brightness = random.randint(-50, 50)
        contrast = random.uniform(0.5, 1.5)
        img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        adjusted_image = cv2.convertScaleAbs(
            img_array, beta=brightness, alpha=contrast)
        adjusted_image = Image.fromarray(
            cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB))

        # Espejo
        if i == 4 and not flip_applied:
            flip_applied = True
            mirrored_image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
        else:
            mirrored_image = rotated_image.transpose(
                method=Image.FLIP_LEFT_RIGHT)

        # Recorte
        crop_x1 = random.randint(0, int(width/4))
        crop_y1 = random.randint(0, int(height/4))
        crop_x2 = random.randint(int(width/2), width)
        crop_y2 = random.randint(int(height/2), height)
        cropped_image = image.crop((crop_x1, crop_y1, crop_x2, crop_y2))

        # Agregar cada imagen resultante a la lista de imágenes aumentadas
        augmented_images.extend(
            [rotated_image, resized_image, adjusted_image, mirrored_image, cropped_image])

    # Devolver la lista con todas las imágenes aumentadas
    return augmented_images


# Cargar la imagen original
img = Image.open('love.jpg')

# Aumentar la imagen y guardar todas las imágenes resultantes
augmented_images = augment_image(img)
for i, image in enumerate(augmented_images):
    image.save(f'love_augmentado_{i}.jpg')
