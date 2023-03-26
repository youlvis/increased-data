from PIL import Image
import cv2
import random
import numpy as np
import tkinter as tk
from tkinter import filedialog


def augment_image(image):
    augmented_images = []

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
        if random.choice([True, False]):
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


# Seleccionar las imágenes a procesar
root = tk.Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames(title='Seleccionar imágenes', filetypes=[
                                         ('Imágenes', '*.jpg;*.jpeg;*.png')])

# Procesar cada imagen seleccionada
for file_path in file_paths:
    # Cargar la imagen original
    img = Image.open(file_path)

    # Aumentar la imagen y guardar todas las imágenes resultantes
    augmented_images = augment_image(img)
    for i, image in enumerate(augmented_images):
        file_extension = file_path.split('.')[-1]
        file_name = f'{file_path[:-len(file_extension)-1]}_augmentado_{i}.{file_extension}'
        image.save(file_name)
